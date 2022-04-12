import time
import pyfiglet
from colorama import init, Fore, Style
from .pero_fx import *
import json

class Wordle():
    def __init__(self, hidden: list, max: int, name: str = "wordle", allowed: str = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN", hard: bool = False, colors: str = "text"):
        init()
        self.color_options = [
            "light", "dark", "colorblind", "colorblinddark",
            "text", "nerdle", "nerdlelight", "queerdle_accessible",
            "queerdle_light", "queerdle2", "canuckle", "jewdle",
            "byrdle", "bts", "kovet"
        ]
        if colors not in self.color_options:
            raise ValueError("colors: string must be one of %r" % self.color_options)
        self.color_demos = [
            ["⬜","🟨","🟩"], ["⬛","🟨","🟩"], ["⬜","🟦","🟧"], ["⬛","🟦","🟧"],
            ["-","y","G"], ["⬛","🟪","🟩"], ["⬜","🟪","🟩"], ["🎱","🍑","💦"],
            ["🥥","🍌","🐍"], ["🎱","🍌","🐍"], ["⬛","🟨","🟥"], ["⬜","🟧","🟩"],
            ["⚪","🟡","🟢"], ["⬛️","🟨","🟪"], ["⬜","🟨","🟦"]
        ]
        self.FORES = [Fore.WHITE, Fore.YELLOW, Fore.GREEN]
        self.secret = hidden
        for _à_ in range(len(self.secret)):
            self.secret[_à_] = self.secret[_à_].lower()
        self.wordcount = len(hidden)
        self.maxguesses = max
        self.allowed = allowed
        self.mode = hard
        self.name = name
        for i in range(len(self.color_options)):
            if self.color_options[i] == colors:
                self.colors = self.color_demos[i]

        f = pyfiglet.Figlet(font='big')
        print(f.renderText(name))
        print("Please enter your first guess. y = incorrect spot, G = correct spot, - = not in guess")
        print()
        if self.mode == True:
            self.name += " HARD"
            print("You are playing hard mode, meaning you're required to use letters you used before, and in the correct spot if it was earlier.")
            print("To change this, go to your file you're running this from (probably \"wordle.py\") and change the following line:")
            print("`hard = True` to `hard = False`")
        print()
        if self.wordcount == 1:
            print("1 word of length " + str(len(self.secret[0])))
        else:
            print(str(len(self.secret)) + " words of length " + str(len(self.secret[0])))
        print()

    def getGuess(self, epsilon, guesslist):
        flagChar = False
        flagLen = False
        flagDict = False
        flagDeja = False
        flagHard = False
        word = input()

        while flagChar == False or flagLen == False or flagDict == False or flagDeja == False or flagHard == False:
            flagChar = False
            flagLen = False
            flagDict = False
            flagDeja = False
            flagHard = False
            length = len(self.secret[0])

            # flagLen

            if len(word) == length:
                flagLen = True
            else:
                l = list(word)
                flagLen = False
                if len(word) > length:
                    print("Guess is too long, please try again")
                    word = input()
                if len(word) < length:
                    print("Guess is too short, please try again")
                    word = input()

            # flagChar

            flag01 = True
            for p in range(len(word)):
                if word[p] not in self.allowed:
                    flag01 = False
            if flag01 == False:
                flagChar = False
                print("Guess contains invalid characters, please try again")
                word = input()
            else:
                flagChar = True

            # flagDict

            if word in epsilon:
                flagDict = True
            else:
                flagDict = False
                print("Invalid guess, please try again")
                word = input()

            # flagDeja

            if guesslist == []:
                flagDeja = True
            else:
                tempflagdeja = False
                for i in range(len(guesslist)):
                    if word == guesslist[i]:
                        tempflagdeja = True
                if tempflagdeja == False:
                    flagDeja = True
                else:
                    flagDeja = False
                    print("Already guessed this word")
                    word = input()

            # flagHard

            w, v = self.lastguess
            w = list(w)
            v = list(v)
            l = list(word)

            if self.mode == False:
                flagHard = True
            elif w == []:
                flagHard = True
            else:
                print(w)
                print(l)
                for i in range(len(w)):
                    vflagtemp = False
                    if v[i] == "G":
                        if w[i] != l[i]:
                            flagHard = False
                            vflagtemp = True
                            print("You are missing letters")
                            word = input()
                    elif w[i] not in word and v[i] != "-":
                        flagHard = False
                        print("You are missing letters")
                        word = input()
                    if vflagtemp == False:
                        flagHard = True

        return word

    def getColorOptions(self): print(self.color_options)

    def emojify(self, arr):
        e = []
        for p in range(len(arr)):
            g = list(arr[p])
            w = ""
            for k in range(len(g)):
                l = g[k]
                if l == "-":
                    w += self.colors[0]
                if l == "y":
                    w += self.colors[1]
                if l == "G":
                    w += self.colors[2]
                if l == " ":
                    w += " "
            e.append(w)
        print()
        print()
        print(self.name + " " + str(self.guesses) + "/" + str(self.maxguesses) + "   " + str(self.timespent) + " s")
        print(ArrToStrSpaces(self.guessnums, "/"))
        for n in range(len(e)):
            print(e[n])
        print("Try for yourself at <https://github.com/saperoi/misc/tree/main/python/wordle>")

    def getVerdict(self, guess, seca):
        sec = seca
        guessl = list(guess)
        verdict = []
        colorverdict = []
        arrverdict = []

        for _ in range(self.wordcount):
            sect = sec[_]
            secl = list(sect)
            tempverdict = nCopies(len(sect), "")
            tempcolorverdict = nCopies(len(sect), "")
            greens = nCopies(len(sect), False)

            for j in range(len(sect)):
                if guessl[j] == secl[j]:
                    tempcolorverdict[j] = self.FORES[2] + "G" + Style.RESET_ALL
                    tempverdict[j] = "G"
                    secl[j] = "-"
                    greens[j] = True
            for j in range(len(sect)):
                if greens[j] == True:
                    continue
                elif guessl[j] in sect:
                    for k in range(len(sect)):
                        if guessl[j] == secl[k]:
                            tempcolorverdict[j] = self.FORES[1] + "y" + Style.RESET_ALL
                            tempverdict[j] = "y"
                            secl[k] = "-"
                            sect, secl = copyfix(secl)
            for j in range(len(sect)):
                if tempverdict[j] == "":
                    tempcolorverdict[j] = self.FORES[0] + "-" + Style.RESET_ALL
                    tempverdict[j] = "-"
            arrverdict.append(copyfix(tempverdict, True))
            if _ != self.wordcount - 1:
                tempverdict.append(" ")
                tempcolorverdict.append(" ")
            tempverdict = copyfix(tempverdict, True)
            tempcolorverdict = copyfix(tempcolorverdict, True)
            verdict.append(tempverdict)
            colorverdict.append(tempcolorverdict)
        colorverdict = ArrToStrSpaces(colorverdict)
        verdict = ArrToStrSpaces(verdict)

        return verdict, colorverdict, arrverdict

    def wordle(self, epsilon):
        sec = []
        self.guessnums = []
        for _ in range(len(self.secret)):
            sec.append(self.secret[_])
            self.guessnums.append("X")
        starttime = time.time()
        lasttime = starttime
        i = 1
        SpecCorr = []
        Blanks = []
        for _ in range(self.wordcount):
            _____ = ""
            ______ = ""
            for ___ in range(len(self.secret[_])):
                _____ += "G"
                ______ += "-"
            SpecCorr.append(_____)
            Blanks.append(______)

        emojis = []
        self.lastguess = ("", "")
        guesslist = []
        while i <= self.maxguesses:
            print("Guess " + str(i) + "/" + str(self.maxguesses))
            print("--------------")
            word = self.getGuess(epsilon, guesslist)
            word = word.lower()
            guesslist.append(word)
            word = list(word)

            verdict, colorverdict, arrverdict = self.getVerdict(word, sec)
            emojis.append(verdict)
            self.lastguess = (word, verdict)
            print(colorverdict)
            self.vflag = False

            for j in range(len(arrverdict)):
                if arrverdict[j] == SpecCorr[j]:
                    sec[j] = copyfix(nCopies(len(sec[j]), "-"), True)
                    self.guessnums[j] = i

            if sec == Blanks:
                if self.wordcount != 1:
                    print("You won! The was were: " + ArrToStrSpaces(self.secret))
                else:
                    print("You won! The word was: " + ArrToStrSpaces(self.secret))
                self.timespent = round((time.time() - lasttime), 2)
                print("You guessed it in " + str(i) + " guesses, and took " + str(self.timespent) + " seconds.")
                self.vflag = True
                self.guesses = str(i)
                i = self.maxguesses
            i += 1
        if self.vflag == False:
            self.timespent = "/./"
            if self.wordcount != 1:
                print("You lost :( The was were: " + ArrToStrSpaces(self.secret))
            else:
                print("You lost :( The word was: " + ArrToStrSpaces(self.secret))
            self.guesses = "X"
        print()
        print("Share with your friends!")
        print("Emoji's might show up as  ⍰  but they're still copyable")
        self.emojify(emojis)

class Config():
    def JSon(f):
        f = json.loads(f.read())
        _a = f['name']
        _b = f['allowed_characters']
        _c = f['max_guesses']
        _d = f['num_words']
        _e = getList(f['puzzle_words'])
        if f['all_words'] == f['puzzle_words']:
            _f = _e
        else:
            _f = getList(f['all_words'])
        _g = f['colors']
        _h = f['hard_mode']
        if _h == "hard" or _h == "Hard" or _h == "HARD"  or _h == "TRUE" or _h == "true" or _h == "True" or _h == True:
            _h = True
        else:
            _h = False
        _i = []
        for i in range(int(_d)):
            _i.append(secretWord(_e, len(_e), False))
        game = Wordle(hidden = _i, max = _c, name = _a, allowed = _b, hard = _h, colors = _g)
        game.wordle(_f)
