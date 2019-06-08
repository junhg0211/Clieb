import socket
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import unquote_plus

import sys

sys.path.append('/'.join(__file__.split('\\')[:-1] if '\\' in __file__ else __file__.split('/')[:-1]))

from dictionary import search_for_keys, get_dictionary


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


# noinspection SpellCheckingInspection
def parse_query(query):
    dictionary = {}

    dictionar = query.split('&')
    for dictiona in dictionar:
        if dictiona == '':
            continue
        diction = dictiona.split('=')
        dictionary[diction[0]] = diction[1]
        dictionary[diction[0]] = unquote_plus(dictionary[diction[0]])

    return dictionary


language_name = ''
search = ''
there_is_amount_of_words = ''


def reload_strings():
    global language_name, search, there_is_amount_of_words

    with open('./res/info.txt', 'r', encoding='utf-8') as file:
        data = '\n'.join(file.readlines()).split('\n')

        while '' in data:
            data.remove('')

        language_name = data[0]
        search = data[1]
        there_is_amount_of_words = data[2]


def get_language_name():
    return language_name


def get_search_string():
    return search


def get_there_is_amount_of_words_string():
    return there_is_amount_of_words


def get_search(query):
    keyword = parse_query(query)['keyword']

    words = search_for_keys(keyword)

    result = open('./res/pages/search.html', 'r', encoding='utf-8').read() \
        .replace('[|KEYWORD|]', keyword)

    meanings = ''

    dictionary = get_dictionary()
    for word in words:
        meaning = dictionary[word].split('\n')
        for i in range(len(meaning)):
            meaning[i] = f'<p>{meaning[i]}</p>\n'
        meaning = ''.join(meaning)

        meanings += open('./res/pages/word_template.html', 'r', encoding='utf-8').read().replace('[|WORD|]',
                                                                                                 word).replace(
            '[|MEANING|]', meaning) + '\n'

    result = result.replace('[|RESULT|]', meanings)

    return result


# noinspection PyPep8Naming
# noinspection SpellCheckingInspection
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = self.path.split('/')[-1].split('?')[-1]

        if self.path != '/':
            filepath = self.path.split("?")[0]
        else:
            filepath = '/index'

        if self.path.split('?')[0] == '/search':
            response = get_search(body)
        else:
            try:
                response = open(f'./res/pages{filepath}.html', 'r', encoding='utf-8').read()
            except FileNotFoundError:
                response = "<h1>404 Not Found"

        reload_strings()

        response = response.replace('[|LANGUAGE_NAME|]', get_language_name()) \
            .replace('[|SEARCH|]', get_search_string()) \
            .replace('[|THERE_IS_AMOUNT_OF_WORDS|]', get_there_is_amount_of_words_string()) \
            .replace('[|AMOUNT|]', str(len(get_dictionary())))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        response = 'hi.'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())


print('Listen requests on http://localhost:35536/')
host = socket.gethostbyname(socket.getfqdn())
ThreadingServer(('', 35536), RequestHandler).serve_forever()
