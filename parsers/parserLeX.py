import ply.lex as lex
from ply.lex import Lexer


class GoodCommands(object):
    command: str
    keys: set

    def __init__(self, command, keys=None):
        if keys is None:
            keys = set()
        self.command = command
        self.keys = keys


class ParserLeX:
    statistic: GoodCommands
    tokens = (
        'COMMAND',
        'SPACE',
        'DASH',
        'KEYS'
    )

    tokens_list = []

    t_SPACE = r'\s+'
    t_DASH = r'\-'

    def t_COMMAND(self, t):
        r'(\.{1,2}\/{1})*[A-Za-z0-9]+(\.[A-Za-z0-9]+)?'
        return t

    def t_KEYS(self, t):
        r'(\s{1,}\-{1}[A-Za-z0-9]{1})+'
        return t

    def __init__(self):
        self.lexer: Lexer = lex.lex(self)
        self.statistic = GoodCommands("")

    def t_error(self, t):
        return False

    def build(self, **kwargs):
        return self

    def genTokens(self, inp):
        self.lexer.input(inp)
        while True:
            try:
                tok = self.lexer.token()
            except lex.LexError:
                self.clear()
                return False
            if not tok:
                break
            self.tokens_list.append(tok)
        return self.tokens_list

    def check(self):
        if len(self.tokens_list) != 0:
            token = self.tokens_list.pop(0)

            if token.type != 'SPACE' and token.type != 'COMMAND':
                return False, self.statistic

            if token.type == 'SPACE' and len(self.tokens_list) != 0:
                token = self.tokens_list.pop(0)

            if token.type == 'COMMAND':
                self.statistic.command = token.value
                if len(self.tokens_list) == 0:
                    return True, self.statistic
                token = self.tokens_list.pop(0)
                if token.type == 'KEYS':
                    keysList = token.value.split('-')
                    if '' in keysList:
                        keysList.remove('')
                    if ' ' in keysList:
                        keysList.remove(' ')
                    self.statistic.keys |= set(keysList)
                    return True, self.statistic
            return False, self.statistic

            # flag = 0
            # while len(self.tokens_list) != 0:
            #     token = self.tokens_list.pop(0)
            #     if token == 'SPACE' and flag == 0:
            #         if len(self.tokens_list) == 0:
            #             return True, self.statistic
            #         flag = 1
            #     if token == 'DASH' and flag == 1:
            #         if len(self.tokens_list) == 0:
            #             return False, self.statistic
            #         flag = 2
            #     if token == 'KEYS' and flag == 2:
            #         if len(self.tokens_list) == 0:
            #             self.statistic.keys.add(token.value)
        return False, self.statistic

    def CheckString(self, string: str):
        self.clear()
        self.genTokens(string)
        return self.check()

    def clear(self):
        self.tokens_list.clear()
