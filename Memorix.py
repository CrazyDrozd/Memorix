'''Memorix'''
'''Last Update: 01.08.2024'''

import time, keyboard, os, platform, colorama, sys, threading, json
from datetime import date
from rich.panel import Panel
from rich.console import Console
from getpass import getpass
import TextEngine as TextIR

languageList = ['English', 'Russian']
languageDescs = ['en-EN', 'ru-RU']

formats = ['24-hour format', '12-hour format']
descs = []
current_date = date.today()

language = 'en'

with open('data/localization.json', 'r', encoding='UTF-8') as local_file:
    Localization = json.load(local_file)


colors = {
    'end': '\033[0m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'gray': '\033[37m'
}
colorsBG = {
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43m',
    'blue': '\033[44m',
    'purple': '\033[45m',
    'cyan': '\033[46m',
    'gray': '\033[47m'
}

def flush_input():  # Очистка буфера ввода
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios  # for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
         
def clear(): # Функция очистки консоли
    if platform.system() == 'Mac' or platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

def timeFormatting(): # Обновление реального времени
    global current_time, current_date, formatted_time, formatted_time_am_pm
    while True:
        current_date = date.today()
        current_time = time.localtime()
        formatted_time = time.strftime("%H:%M:%S", current_time)
        formatted_time_am_pm = time.strftime("%I:%M:%S %p", current_time)
        time.sleep(1)
    
def mainCode(): # Основная часть прототипа
    cmdBool = False
    notesList = []
    coloredNotesList = []
    lastNoteIndex = 0
    threading.Thread(target=timeFormatting).start()
    notesList.append(f'[ {current_date} ]')
    while True: # Основной цикл
        cmdBool = False
        note = input()
        sys.stdout.write("\033[F")
        if note.startswith('/save'): # cmd: /save {file_name: optional}
            cmdBool = True
            file_name = 'Notes.txt'
            if len(note) > 6:
                file_name = note[6:].strip()
                file_name = file_name + '.txt'
            with open(file_name, 'w') as notes_txt:
                for item in notesList:
                    notes_txt.write(item + '\n')
                if len(notesList) == 1:print(f"{colors['red']}{clear_text}{colors['end']}")
                else: print(f"{colors['green']}{save_text}{colors['end']}")
        if note.startswith('/head'):  # cmd: /head {text: optional}, {color: optional}
            cmdBool = True
            headName = '                '
            colorName = 'yellow'  # default color
            parts = note[6:].split(', ')
            if len(parts) > 0:
                headName = parts[0].strip()
            if len(parts) > 1:
                colorName = parts[1].strip().lower()
            if colorName in colors:  # check if color is valid
                print(f"{colors[colorName]}[   {headName}   ]{colors['end']}")
                notesList.append(f'[ {headName} ]')
                coloredNotesList.append(f"{colors[colorName]}[   {headName}   ]{colors['end']}")
                clear()
                print(f"{colors['red']}{start_text}{colors['end']}")
                print(f"{colors['yellow']}[ {current_date} ]{colors['end']}")
                for everyNote in coloredNotesList:
                    print(everyNote)
            else:
                print(f"{colors['red']}[    Invalid color!    ]{colors['end']}")
        match note: # cmds
            case '/colors':
                cmdBool = True
                print(f'{colors['yellow']}{colors_cmd}{colors['end']}')
                print(f'''{colors['red']}red{colors['end']}
{colors['green']}green{colors['end']}
{colors['yellow']}yellow{colors['end']}
{colors['blue']}blue{colors['end']}
{colors['purple']}purple{colors['end']}
{colors['cyan']}cyan{colors['end']}
{colors['gray']}gray{colors['end']}''')
            case '/clear':
                cmdBool = True
                lastNoteIndex = 0
                notesList.clear()
                notesList.append(f'[ {current_date} ]')
                coloredNotesList.clear()
                sys.stdout.write("\033[F")
                clear()
                print(f"{colors['red']}{start_text}{colors['end']}")
                print(f"{colors['yellow']}[ {current_date} ]{colors['end']}")
            case '/help':
                cmdBool = True
                print(f"{colors['yellow']}[ ALL CMDS ]{colors['end']}")
                print(help_cmd)
            case '/del':
                if len(coloredNotesList) != 0:
                    cmdBool = True
                    if any(coloredNotesList[-1].startswith(color + '[   ') for color in colors.values()):
                        notesList.pop()
                        coloredNotesList.pop()
                    else:
                        lastNoteIndex -= 1
                        notesList.pop()
                        coloredNotesList.pop()
                    clear()
                    print(f"{colors['red']}{start_text}{colors['end']}")
                    print(f"{colors['yellow']}[ {current_date} ]{colors['end']}")
                    for everyNote in coloredNotesList:
                        print(everyNote)
                else:
                    cmdBool = True
                    flush_input()
                    pass
        flush_input()
        if cmdBool != True:
            if timeFormat == '24-hour format':
                print(f"{colors['yellow']}[{lastNoteIndex}][ {formatted_time} ]{colors['end']} {note}")
                notesList.append(f"[{lastNoteIndex}][ {formatted_time} ] {note}")
                coloredNotesList.append(f"{colors['yellow']}[{lastNoteIndex}][ {formatted_time} ]{colors['end']} {note}")
                lastNoteIndex += 1
            elif timeFormat == '12-hour format':
                print(f"{colors['yellow']}[{lastNoteIndex}][ {formatted_time_am_pm} ]{colors['end']} {note}")
                notesList.append(f"[{lastNoteIndex}][ {formatted_time_am_pm} ] {note}")
                coloredNotesList.append(f"{colors['yellow']}[{lastNoteIndex}][ {formatted_time_am_pm} ]{colors['end']} {note}")
                lastNoteIndex += 1

#console = Console()
#console.print(Panel("[yelllow]Memorix[/] — это мини-программа, в которую можно писать свои заметки и они будут сохраняться с их индексом и временем написания.", title = '[bold yellow][ Memorix ][/]', expand = False))
#console.print(Panel('Нажмите [bold magenta]пробел[/] для продолжения', expand = False))
#keyboard.wait('space')
#clear()

# Выбор языка
languageChoose = TextIR.Choose(languageList, languageDescs, "LANGUAGE", infinityScroll = True, colorKeys = 'yellow', colorFocus = 'yellow')
languageChoose.start()
languageC = languageChoose.getNumberOption()
match languageC:
    case 1:
        language = 'en'
    case 2:
        language = 'ru'

# Загрузка текста
text_24hour = Localization[language][0]['time_format']['24-hour format']
text_12hour = Localization[language][0]['time_format']['12-hour format']
start_text = Localization[language][1]['start_text']
save_text = Localization[language][2]['save_text']
clear_text = Localization[language][3]['clear_text']
help_cmd = Localization[language][4]['help_cmd']
colors_cmd = Localization[language][5]['colors_cmd']

# Добавление описания временных форматов в список
descs.append(text_24hour)
descs.append(text_12hour)

# Выбор формата часов и старт
timeFormatChoose = TextIR.Choose(formats, descs, "TIME FORMAT", infinityScroll = True, colorKeys = 'yellow', colorFocus = 'yellow')
timeFormatChoose.start()
timeFormat = timeFormatChoose.getNumberOption()
match timeFormat:
    case 1:
        timeFormat = '24-hour format'
    case 2:
        timeFormat = '12-hour format'

print(f"{colors['red']}{start_text}{colors['end']}")
print(f"{colors['yellow']}[ {current_date} ]{colors['end']}")
mainCode()
