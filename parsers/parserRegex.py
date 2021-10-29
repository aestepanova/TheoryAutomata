import re

Pattern = r" *(?P<command>(\.{1,2}\/{1})*[A-Za-z0-9]+(\.[A-Za-z0-9]+)?)(?P<keys>((\s{1,}\-{1}[A-Za-z0-9]{1})*))"


class GoodCommands(object):
    command: str
    keys: set

    def __init__(self, command, keys=None):
        if keys is None:
            keys = set()
        self.command = command
        self.keys = keys


class Regex:
    statistic: GoodCommands

    def __init__(self):
        self.acceptable = False
        self.statistic = GoodCommands("")

    def CheckString(self, text):
        result = re.match(Pattern, text)
        if result:
            command = result.group('command')
            command = re.sub(r'\s+', '', command)
            self.statistic.command = command

            keys = result.group('keys')
            keys = re.sub(r'\s+', ' ', keys)  # change space symbols to one space
            keysList = keys.split('-')
            if '' in keysList:
                keysList.remove('')
            if ' ' in keysList:
                keysList.remove(' ')
            self.statistic.keys |= set(keysList)

            self.acceptable = True
            return self.acceptable, self.statistic
        else:
            self.acceptable = False
            return self.acceptable, self.statistic
