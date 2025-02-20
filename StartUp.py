import tkinter as tk
from threading import Thread

NESW = tk.N + tk.E + tk.S + tk.W
from Ponzti import Ponzti

from ScoreCard import PlayerScore, ScoreSheet, ScoreSheetCell

from Slot import Slot

class Start:


    def __init__(self):


        self.root = tk.Tk()

        self.playerNames = []

        # use a stack to keep order and to help add and remove players
        self.playerCards = []

        self.entryVars = []

        self.root.config(bg = 'black')

        self.DIMENSION_SCALE = .4

        self.W_HEIGHT = self.root.winfo_screenheight() * self.DIMENSION_SCALE

        self.W_WIDTH = self.root.winfo_screenwidth() * self.DIMENSION_SCALE

        self.W_OFFSET = '+' + str(int((self.root.winfo_screenwidth() - self.W_WIDTH) / 2)) + '+' + str \
            (int((self.root.winfo_screenheight() - self.W_HEIGHT) / 2))

        self.SCREEN_DIMENSIONS = str(int(self.W_WIDTH)) + 'x' + str(int(self.W_HEIGHT)) + str(self.W_OFFSET)

        self.root.geometry(self.SCREEN_DIMENSIONS)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)


        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight = 1)
        self.root.rowconfigure(2, weight = 1)
        self.root.rowconfigure(3, weight = 1)

        ## Title
        self.title = tk.Label(self.root, text= 'Ponzti!', font=('roboto', 18), bg = 'light grey')
        self.title.grid(row = 0, column = 0, columnspan = 2 , sticky = NESW)

        self.playerCounts = [1, 2, 3, 4, 5]

        ## Drop menu
        self.countLabel = tk.Label(self.root, text = 'Number of players:', font=('roboto', 16), bg = 'light grey')
        self.countLabel.grid(row = 1, column = 0, sticky = NESW)

        self.currentNumPlayers = 0
        self.numPlayers = tk.IntVar()
        self.dropDown = tk.OptionMenu(self.root, self.numPlayers,
                                      command = self.changePlayerCount, *self.playerCounts)
        self.dropDown.config(font = ('roboto', 16), bg = 'light grey')
        self.root.nametowidget(self.dropDown.menuname).configure(font = ('roboto', 12))
        self.dropDown.grid(row = 2, column = 0, sticky = NESW)


        self.entryTitle = tk.Label(self.root, bg = 'light grey', text = "Character Names")
        self.entryTitle.grid(row = 1, column = 1, sticky = NESW)
        ##
        self.entryFrame = tk.Frame(self.root, bg = 'light grey')
        self.entryFrame.grid(row = 2, column = 1, sticky = NESW)

        self.startButton = tk.Button(self.root, text = 'BEGIN GAME', command = self.beginGame, bg = 'light grey')
        self.startButton.grid(row = 3, column = 0, columnspan = 2, sticky = NESW)

        self.root.mainloop()

    def changePlayerCount(self, *args):
        requested = self.numPlayers.get()
        print(requested)

        while requested != self.currentNumPlayers:
            if requested > self.currentNumPlayers:
                v = tk.StringVar(self.root)
                c = tk.Entry(self.entryFrame, textvariable =  v, font = ('roboto', 12), bg = 'light grey')
                c.pack(side = "top", fill = "x")
                self.playerCards.append(c)
                self.entryVars.append(v)
                self.currentNumPlayers += 1
            else:
                c = self.playerCards.pop()
                c.destroy()
                self.entryVars.pop()
                self.currentNumPlayers -= 1



    def addPlayerCard(self, turn):
        pass

    def beginGame(self):

        if len(self.playerCards) < 1:
            return
        else:
            for var in self.entryVars:
                self.playerNames.append(var.get())

        self.root.destroy()

        w = Ponzti(self.playerNames)
        w.root.mainloop()





w = Start()
