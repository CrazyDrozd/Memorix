from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from time import sleep as cd
from icecream import ic
import keyboard

console = Console()

ic.disable()

def _clear(): # Функция очистки консоли
    import platform, os
    if platform.system() == 'Mac' or platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

class Replic:
    '''Этот класс предназначен для вывода реплики персонажа
:param str nameCh: Имя персонажа
:param str talk: Текст персонажа
:param float speed: Скорость печатания текста'''
    def __init__(self, nameCh: str, talk: str, speed: float = 0.010):
        global start, end, lendelay
        talk_print = ''
        lendelay = 0
        Frame = Panel(talk_print, expand=False, title=nameCh)
        for n in range(len(talk)):
            if talk[n] == '^':
                start = n + 1
                end = talk.find('/', n)
                delayCd = int(talk[start:end])
                lendelay = len(str(delayCd))
                console.print(Frame)
                if talk[n+lendelay+1] == '/':
                    cd(delayCd)
                    _clear()
                    continue
            elif talk[n] == '/' and talk[n-lendelay-1] == '^':
                continue
            elif n in range(talk.find('^', n-lendelay), talk.find('/', n-lendelay)+1):
                pass
            else:
                talk_print += talk[n]
                Frame = Panel(talk_print, expand=False, title=nameCh)
                console.print(Frame)
                cd(speed)
                _clear()
        console.print(Frame)

class Plot:
    '''Этот класс предназначен для вывода последовательных фраз несколький героев

Оформление сюжета:

">Name Hero

Replic1

Replic2

Name Hero2<Replic"

>Name Hero - имя героя, а его реплики при символе > определяются построчно

Name Hero2< - имя второго героя. При символе < герой имеет одну реплику и она определяется сразу после < (пробелов лучше не ставить)

:param str plot: основной параметр, содержащий все реплики героев (оформление выше)
'''
    def __init__(self, plot: str):
        self.plot = plot
    def start(self, dialog_delay: float, speed: float = 0.010):
        '''Эта функция отвечает за сам вывод сценария
:param float dialog_delay: Задержка между репликами
:param float speed: Скорость печатания текста
'''
        list_plot = self.plot.split('\n')
        for n in list_plot:
            if n[0] == '>':
                name = n[1:]
                replics = []
                for i in list_plot[list_plot.index(n)+1:]:
                    if '<' not in i and '>' not in i: replics.append(i)
                    else: break
                ic(name, replics)
                for q in replics:
                    Replic(name, q, speed)
                    cd(dialog_delay)
                    _clear()
            elif '<' in n:
                wp = n.index('<')
                name = n[:wp]
                replic = n[wp+1:]
                ic(name, replic)
                Replic(name, replic, speed)
                cd(dialog_delay)
                _clear()

class Choose:
    def __init__(self,
                 options: list[str],
                 descs: list[str],
                 title: str,
                 *,
                 digitalKeys: bool = False,
                 select: int = 1,
                 infinityScroll: bool = False,
                 end_clear: bool = True,
                 selectKey: str = 'space',
                 enterKey: str = 'enter',
                 confirmation: bool = False,
                 colorKeys: str = 'purple',
                 colorFocus: str = 'purple',
                 colorSelected: str = 'yellow',
                 colorNotSelected: str = 'cyan',
                 padding: int = 4):
        '''Параметры:
:param list options: Список вариантов выбора
:param list descs: Список описаний вариантов выбора (Поставьте "" для варианта без описания)
:param str title: Название меню выбора
:param bool digitalKeys: Активатор переключения вариантов с помощью клавиш 1-9 (не рекомендуется при кол-ве варинтов больше чем 9)
:param int select: Номер варианта, выбранный изначально
:param bool infinityScroll: Активация бесконечной прокрутки
:param bool end_clear: Очистить ли консоль после выбора
:param bool confirmation: Подтверждение выбора (при True для подтверждения и выбора разные клавиши, при False одна)
:param str selectKey: Клавиша для выбора варианта (работает при confirmation = True)
:param str enterKey: Клавиша для выбора и подтверждения (при confirmation = False) или просто подтверждения (при confirmation = True)
:param str colorKeys: Цвет выделения клавиш в подсказках ("↑ или ↓" и других)
:param str colorFocus: Цвет выделения заголовка при предварительном выборе варианта
:param str colorSelected: Цвет выделения выбранного варианта
:param str colorNotSelected: Цвет выделения вариантов, не выбранных предварительно
:param int padding: Отступ от края в не выбранных предварительно вариантов
        '''
        self.chose = select - 1
        self.selected = select - 1
        self.options = options
        self.descs = descs
        self.title = title
        self.dKeys = digitalKeys
        self.IS = infinityScroll
        self.endCl = end_clear
        self.sK = selectKey
        self.eK = enterKey
        self.con = confirmation
        self.clKs = colorKeys
        self.clNS = colorNotSelected
        self.clS = colorSelected
        self.clF = colorFocus
        self.tab = padding
    def __returnChose(self):
        _clear()
        console.print(Markdown(f'## {self.title}'))
        descsNew = []
        for n in range(len(self.options)):
            name = self.options[n]
            if self.descs[n] != "" and self.chose == n:
                descsNew.append(Panel(self.descs[n],
                                      title=
                                            f'[bold {self.clS}]{name} (Выбрано)[/]'
                                            if self.con == True and self.selected == n
                                            else f'[bold {self.clF}]{name}[/]',
                                      expand=False))
            else:
                if n == self.selected and self.con == True:
                    descsNew.append(f'{' ' * self.tab}> [bold {self.clS}]{name} (Выбрано)[/]\n')
                elif n == self.chose and self.selected != n:
                    descsNew.append(f'{' ' * self.tab}> [italic {self.clF}]{name}[/]\n')
                elif n != self.chose:
                    descsNew.append(f'{' ' * self.tab}> [{self.clNS}]{name}[/]\n')
        console.print(*descsNew)
        console.print(Panel(f'[bold {self.clKs}]↑ or ↓[/] to switch\n[bold {self.clKs}]{self.sK}[/] to select\n[bold {self.clKs}]{self.eK}[/] to confirm')
                            if self.con == True
                            else f'[bold {self.clKs}]↑ or ↓[/] to switch\n[bold {self.clKs}]{self.eK}[/] to select')
        cd(0.2)
    def __flush_input(self):  # Очистка буфера ввода
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            import sys, termios  # for linux/unix
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    def start(self) -> int:
        # Первый вывод меню выбора
        self.__returnChose()
        # Переключение и последующие выводы таблицы выбора
        while True:
            if keyboard.is_pressed('up'):
                self.chose -= 1
                if self.chose < 0:
                    if self.IS == True:
                        self.chose = len(self.options) - 1
                    else:
                        self.chose = 0
                self.__returnChose()
            elif keyboard.is_pressed('down'):
                self.chose += 1
                if self.chose > len(self.options) - 1:
                    if self.IS == True:
                        self.chose = 0
                    else:
                        self.chose = len(self.options) - 1
                self.__returnChose()
            elif keyboard.read_key().isdigit() and self.dKeys == True:
                self.chose = int(keyboard.read_key()) - 1
                self.__returnChose()
            elif keyboard.is_pressed(self.sK) and self.con == True:
                self.selected = self.chose
                self.__returnChose()
            elif keyboard.is_pressed(self.eK):
                if self.con == False: self.selected = self.chose
                if self.endCl == True: _clear()
                self.__q = self.selected + 1
                self.__flush_input()
                break
    def getOptionInfo(self):
        '''Получение полной информации о выбранном варианте'''
        return {'name': self.options[self.__q-1], 'desc': self.descs[self.__q-1], 'number': self.__q}
    def getNumberOption(self):
        '''Получение номера выбранного варианта'''
        return self.__q
    def getOptionName(self):
        '''Получение выбранного варианта'''
        return self.options[self.__q-1]
    def getOptionDesc(self):
        '''Получение описания выбранного варианта'''
        return self.descs[self.__q-1]
    def editOption(self, option: str|int, new_option: str):
        '''Изменение варианта'''
        if type(option) == int:
            self.options[option-1] = new_option
        elif type(option) == str:
            self.options[self.options.index(option)] = new_option
    def delOption(self, option: str|int):
        '''Удаление варианта'''
        if type(option) == int:
            del self.options[option-1]
        elif type(option) == str:
            del self.options[self.options.index(option)]

class List:
    def __init__(self,
                 lists_titles: list[str],
                 lists_contents: list[str],
                 width: int,
                 key_end: str = 'space'):
        '''Параметры:
:param list titles: Список названия вариантов
:param list contents: Список описания вариантов
:param int width: Ширина панелей опций
:param str key_end: Клавиша подтверждения выбора 
'''
        self.lists_titles = lists_titles
        self.lists_contents = lists_contents
        self._index = 0
        self.width = width
        self.key_end = key_end
    def _output(self):
        listL = self.lists_contents[self._index].splitlines()
        listLens = list(map(lambda x: len(x), listL))
        len1 = max(listLens) // 2
        if self.width % 2 == 0:
            len2 = self.width // 2 - 1
        else:
            len2 = self.width // 2
        if self._index != 0:
            console.print(" " * len2, "↑")
        else:
            console.print()
        console.print(Panel(self.lists_contents[self._index], title=self.lists_titles[self._index], expand=True, width = self.width))
        if self._index != len(self.lists_contents)-1: console.print(" " * len2, "↓")
        console.print(Panel(f'Вы можете переключаться с помощью [purple]↑ и ↓[/]\nНажмите [bold purple]{self.key_end}[/] для отправки назад', expand=False))
    def start(self):
        self._output()
        while True:
            if keyboard.is_pressed("Up") and self._index != 0:
                self._index -= 1
                _clear()
                self._output()
                cd(0.1)
            elif keyboard.is_pressed("Down") and self._index != len(self.lists_contents)-1:
                self._index += 1
                _clear()
                self._output()
                cd(0.1)
            elif keyboard.is_pressed(self.key_end):
                break


if __name__ == "__main__":
    lists = ['[purple]УКРЫТИЕ[/]', '[red]КАПКАН[/]', '[red]ПРЫЖОК[/]']
    listsC = ['В укрытии можно спрятаться и монстр пройдет мимо, не увидев вас. Также вы восстановите немного энергии',
              "При попадании в капкан вы не сможете двигаться. Пытайтесь выбраться. Неудачные попытки заканчиваются тратой энергии",
              'Во время бега монстр может сильно сократить дистанцию, сделав прыжок']
    List(lists, listsC, 70).start()
