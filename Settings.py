import os, platform

def clear(): # Функция очистки консоли
    if platform.system() == 'Mac' or platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')
