from utils import parserSMC_sm


class GoodCommands(object):
    command: str
    keys: set

    def __init__(self, command, keys=None):
        if keys is None:
            keys = set()
        self.command = command
        self.keys = keys


class lab1:

    statistic: GoodCommands

    def __init__(self):
        self.buff = ""
        self._fsm = parserSMC_sm.CommandClass_sm(self)
        self._is_acceptable = False
        self.statistic = GoodCommands("")

    # Uncomment to see debug output.
    # self._fsm.setDebugFlag(True)

    def CheckString(self, string):
        self._fsm.enterStartState()
        for c in string:
            # TODO: соотнести состояния в см файле относительно символов
            if c == '.':
                self._fsm.Point(c)
            elif c == '/':
                self._fsm.Slash(c)
            elif c == ' ':
                self._fsm.Space()
            elif c == '-':
                self._fsm.Dash()
            elif c.isalpha() or c.isdigit():
                self._fsm.LetterOrDigit(c)
            else:
                self._fsm.Unknown()
        self._fsm.EOS()
        return self._is_acceptable, self.statistic

    def Acceptable(self):
        self._is_acceptable = True

    def Unacceptable(self):
        self._is_acceptable = False

    def AddKey(self, c: str):
        self.statistic.keys.add(c)

    def AddCommand(self):
        command = self.buff
        self.statistic.command = command
        self.buff = ""

    def FormCommand(self, c: str):
        self.buff = self.buff + c
