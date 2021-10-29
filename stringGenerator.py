import datetime
import os
import random

import rstr

TEST_ENDING = '.txt'

COMMAND = r"(\.{1,2}\/{1})*[A-Za-z0-9]+(\.[A-Za-z0-9]+)?"
WRONG_COMMAND = r"(\.\/[a-zA-Z\d]+)*\/\/[a-zA-Z\d]"

KEY = r"( {1,3}\-{1}[A-Za-z0-9]{1})+"
WRONG_KEYS = r" *\-*[A-Za-z0-9]{2,}"
NOISE = r"[\da-zA-Z \-\t]"
CPATTERN = r" *((\.{1,2}\/{1})*[A-Za-z0-9]+(\.[A-Za-z0-9]+)?)+((( {1,}\-{1}[A-Za-z0-9]{1})*))"


_ACC = .6
_TRASH = .2
_NACC = .5


def genStr(maxLen):

    if random.random() <= _ACC:  # генерация правильных строк
        tmp = rstr.xeger(COMMAND)
        tmp += rstr.xeger(KEY)
        tmp = tmp[:maxLen]
        return tmp
    elif random.random() <= _TRASH:  # генерация мусора длиной {maxLen/2, maxLen}
        tmp = NOISE + '{' + str(maxLen // 2) + ',' + str(maxLen) + '}'
        return rstr.xeger(tmp)
    else:  # генерация некорректных строк
        wrong = ""
        if random.random() <= _NACC:  # неправильный тип команд 1
            wrong += WRONG_COMMAND
            wrong += KEY + '{0,' + str(min(15, maxLen // 2 - 1 - len(wrong))) + '}'
        elif random.random() <= _NACC:  # неправильные ключи
            wrong += COMMAND
            wrong += ' ' + WRONG_KEYS + '{0,' + str(min(15, maxLen // 2 - 1 - len(wrong))) + '}'
        else:  # неправильное всё
            wrong += WRONG_COMMAND
            wrong += WRONG_KEYS + '{0,' + str(min(15, maxLen // 2 - 1 - len(wrong))) + '}'

        tmp = wrong

        tmp = tmp[:-3]

        return rstr.xeger(tmp)


def generate(testDir: str = "./", N: int = 10, maxLen: int = 30):
    tmp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + f"__N{N}__L{maxLen}{TEST_ENDING}"
    path = os.path.join(testDir, tmp)
    with open(path, 'w+', encoding='UTF-8') as out:
        for i in range(N):
            out.write(genStr(maxLen) + '\n')
    return path
