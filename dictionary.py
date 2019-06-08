# coding=utf-8
import unicodedata
from tkinter import *

with open('./res/info.txt', encoding='utf-8') as file:
    data = ''.join(file.readlines()).split('\n')

    while '' in data:
        data.remove('')

    language_name = data[0]

database = './res/database.txt'


class MainWindow:
    def __init__(self):
        self.core = Tk()

        self.core.bind('<Return>', self.search)
        self.core.bind('<KP_Enter>', self.search)
        self.core.bind('<Escape>', self.shutdown)

        self.main_frame = Frame(self.core)

        Label(self.main_frame, text=language_name, font=('Times New Roman Bold Italic', 24)) \
            .grid(row=0, column=0, columnspan=2)

        self.word_entry = Entry(self.main_frame, width=40)
        self.word_entry.grid(row=2, column=0)
        self.word_entry.focus_force()

        Button(self.main_frame, text='검색', width=10, command=self.search).grid(row=2, column=1)

        Button(self.main_frame, text='단어 수정 및 추가', command=self.add).grid(row=3, column=0, columnspan=2)

        self.main_frame.master.title(language_name)
        self.main_frame.pack(padx=20, pady=10)

    def center(self):
        width = self.core.winfo_screenmmwidth()
        height = self.core.winfo_screenmmheight()

        self.core.geometry(f'+{width}+{height}')

    def start(self):
        self.center()

        self.core.mainloop()

    def shutdown(self, _):
        self.core.destroy()

    def search(self, *_):
        word = self.word_entry.get()
        self.word_entry.delete(0, END)

        r = ResultWindow(word)
        r.start()

    @staticmethod
    def add():
        add_window = AddWindow()
        add_window.start()


def dump_dictionary(dictionary):
    with open(database, 'w', encoding='utf-8') as file:
        file.write(str(dictionary))


def get_dictionary():
    start = -1
    while True:
        with open(database, 'r', encoding='utf-8') as file:
            try:
                start += 1
                return eval(file.read()[start:])
            except SyntaxError as e:
                print(e, start)


def no_accent(string):
    return unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode('utf-8')


def search_for_keys(word):
    dictionary = get_dictionary()

    keys = []

    for key in dictionary.keys():
        value = dictionary[key]

        a = no_accent(word.lower())
        if a != '':
            word = a
        key = key.lower()
        value = value.lower()

        if word in no_accent(key) or word in value:
            keys.append(key)

    keys.sort()

    return keys


def search(word):
    keys = search_for_keys(word)

    dictionary = get_dictionary()
    result = ''

    for key in keys:
        value = dictionary[key]

        result += f'{key.upper()}\n{value}\n\n'

    return result


class ResultWindow:
    def __init__(self, word):
        self.word = word

        self.core = Tk()

        self.core.bind('<Return>', self.shutdown)
        self.core.bind('<KP_Enter>', self.shutdown)
        self.core.bind('<Escape>', self.shutdown)

        self.main_frame = Frame(self.core)

        Label(self.main_frame, text=f'\'{word}\'에 대한 검색 결과').grid(row=0, column=0)

        result = search(self.word)

        result_textbox = Text(self.main_frame, font=('맑은 고딕', 10))
        result_textbox.insert(END, result)
        result_textbox.config(state=DISABLED)
        result_textbox.grid(row=1, column=0)

        result_scrollbar = Scrollbar(self.main_frame, command=result_textbox.yview)
        result_scrollbar.grid(row=1, column=0, sticky=N + S + E)

        result_textbox.config(yscrollcommand=result_scrollbar.set)

        self.main_frame.master.title(f'{language_name}: {word}')
        self.main_frame.pack(padx=20, pady=10)

    def center(self):
        width = self.core.winfo_screenmmwidth()
        height = self.core.winfo_screenmmheight()

        self.core.geometry(f'+{width}+{height}')

    def start(self):
        self.center()
        self.core.focus_force()
        self.core.mainloop()

    def shutdown(self, _):
        self.core.destroy()


class AddWindow:
    def __init__(self):
        self.core = Tk()

        self.core.bind('<Escape>', self.shutdown)

        self.main_frame = Frame(self.core)

        Label(self.main_frame, text=language_name).grid(row=1, column=0)
        Label(self.main_frame, text='뜻').grid(row=2, column=0)

        self.conlang_entry = Entry(self.main_frame)
        self.conlang_entry.grid(row=1, column=1)

        self.unconlang_entry = Text(self.main_frame, width=20, height=6)
        self.unconlang_entry.grid(row=2, column=1)

        Button(self.main_frame, text='불러오기', width=15, command=self.get).grid(row=3, column=0)
        Button(self.main_frame, text='추가', width=15, command=self.add).grid(row=3, column=1)

        self.main_frame.master.title(language_name)
        self.main_frame.pack(padx=20, pady=10)

    def center(self):
        width = self.core.winfo_screenmmwidth()
        height = self.core.winfo_screenmmheight()

        self.core.geometry(f'+{width}+{height}')

    def start(self):
        self.center()
        self.core.focus_force()
        self.core.mainloop()

    def shutdown(self, *_):
        self.core.destroy()

    def get(self):
        dic = get_dictionary()
        word = self.conlang_entry.get().lower()
        if word in dic.keys():
            self.unconlang_entry.delete(1.0, END)
            self.unconlang_entry.insert(END, dic[word])
            print(dic[word])

    def add(self):
        tmp = get_dictionary()
        a = self.unconlang_entry.get(1.0, END)
        while len(a) > 0:
            if a[-1] in ('\n', ' '):
                a = a[:-1]
            else:
                break

        if a:
            tmp[self.conlang_entry.get().lower()] = a
            dump_dictionary(tmp)

            self.shutdown()


if __name__ == '__main__':
    w = MainWindow()

    if len(sys.argv) <= 1:
        w.start()
    else:
        print(search(' '.join(sys.argv[1:])))
