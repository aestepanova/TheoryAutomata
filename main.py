from parsers import parserSMC, parserRegex, parserLeX

from stringGenerator import generate as generator

import time

data = [[], [], []]
file_paths = []

msgs = {" 0. Exit": 0, " 1. Read strings from terminal": 1, " 2. Read strings from file": 2, " 3. Generate strings": 3,
        " 4. Statistics": 4, " 5. Save statistics in a file": 5, " 6. Timing": 6}

NMsgs = len(msgs)

parsers = {" 0. Exit": 0, " 1. SMC": 1, " 2. Regex": 2, " 3. LeX ": 3}

NParsers = len(parsers)

PATH_Tests = "./tests/"
PATH_Stats = "./stats/"
PATH_TimingTESTS = "./timing"

EXTENSION = '.txt'

statCommands = set()


def dialog(_msgs, numOfMessages):
    retCode = -1
    flag = 0
    while retCode > numOfMessages or retCode < 0:
        errmsg = "You are wrong. Repeat, please\n"
        if flag:
            print(errmsg)
        for key in _msgs:
            print(key)
        print("Make your choice: --> ")
        flag = 1
        try:
            retCode = int(input())
        except ValueError:
            print(errmsg)
            retCode = -1
    return retCode


def chooseParser():
    print("What parser do you want to use?\n")
    parser = dialog(parsers, NParsers)
    return parser


def checkString(s: str, chooseParserFlag=True, parser=1):
    if chooseParserFlag:
        parser = chooseParser()
    if parser == 1:
        check = parserSMC.lab1()
    elif parser == 2:
        check = parserRegex.Regex()
    elif parser == 3:
        check = parserLeX.ParserLeX()
    else:
        check = parserSMC.lab1()

    acceptedFlag, stat1 = check.CheckString(s)

    exist = 0
    if acceptedFlag:
        if len(statCommands) > 0:
            for each in statCommands:
                if each.command == stat1.command:
                    each.keys.update(stat1.keys)
                    exist = 1
        if not exist:
            statCommands.add(stat1)
        return True
    return False


def readTerminal():
    print("\nEnter strings --->")
    print("(If you want to stop checking strings, print 'q')")
    s = str(input("Your string: "))
    while s != 'q':
        if checkString(s):
            print(s + " is acceptable")
        else:
            print(s + " is not acceptable")
        s = str(input("Your string: "))
    return 1


def readFile():
    filename = input("Please, input filename: ")
    try:
        with open(PATH_Tests + filename, "r") as file1:
            for line in file1:
                s = line.strip()
                if checkString(s, chooseParserFlag=False):
                    print(s.strip() + " is acceptable")
                else:
                    print(s.strip() + " is not acceptable")
    except FileNotFoundError:
        print("No such file! Go back to the menu...")

    return 1


def generate():
    parser = chooseParser()
    print("Please, choose number of strings: ")
    nStr = int(input())
    print("Input a max length of string: ")
    maxLen = int(input())
    # path = generator(PATH_Tests, N=1000, maxLen=40)
    path = generator(PATH_Tests, nStr, maxLen)
    handler = open(path, 'r')
    text = handler.read()

    for s in text.split('\n'):
        if checkString(s, parser=parser):
            print(s.strip() + " is acceptable")
        else:
            print(s.strip() + " is not acceptable")

    return 1


def stat():
    num = len(statCommands)
    if not bool(num):
        print("There is no any commands.")
    for each in statCommands:
        if len(each.keys) == 0:
            eachKeys = ''
        else:
            eachKeys = each.keys
        print("command: " + each.command + " - keys: " + str(eachKeys))
    return 1


def save():
    num = len(statCommands)
    if not bool(num):
        print("There is no any commands.")
    else:
        fileName = input("Please, input a filename: ")
        f = open(PATH_Stats + fileName + EXTENSION, 'w')
        for each in statCommands:
            if len(each.keys) == 0:
                eachKeys = ''
            else:
                eachKeys = each.keys
            f.write(str(each.command) + " " + str(eachKeys) + "\n")
        f.close()

    return 1


def timing():
    # for i in range(0, 1001, 100):
    for i in range(0, 100, 10):
        path = generator(PATH_TimingTESTS, N=i, maxLen=100)
        file_paths.append(path)

    for path in file_paths:
        handler = open(path, 'r')
        text = handler.read()
        start = time.time_ns()
        for s in text:
            parser = parserSMC.lab1()
            parser.CheckString(s)
        end = time.time_ns()
        data[0].append(end - start)

        start = time.time_ns()
        for s in text:
            parser = parserRegex.Regex()
            parser.CheckString(s)
            print('[Lex is working...]')
        end = time.time_ns()
        data[1].append(end - start)

        start = time.time_ns()
        for s in text:
            parser = parserLeX.ParserLeX()
            parser.build()
            parser.CheckString(s)
            print('[Lex is working...]')
        end = time.time_ns()
        data[2].append(end - start)
        handler.close()
    print(data)
    return 1


def d_exit():
    print("Goodbye! :)")
    return 0


func_arr = [d_exit, readTerminal, readFile, generate, stat, save, timing]

if __name__ == "__main__":
    f = 1
    while f:
        f = dialog(msgs, NMsgs)
        func_arr[f]()
