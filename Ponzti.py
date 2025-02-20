import tkinter as tk

from ScoreCard import PlayerScore, ScoreSheet, ScoreSheetCell

from Slot import Slot

NESW = tk.N + tk.E + tk.S + tk.W


class Ponzti():

    def spinClick(self):  ## Finished

        ## decrement spinsLeft
        self.spinsLeft.set(self.spinsLeft.get() - 1)

        self.spinsCountdown.config(text=self.spinsLeft.get())

        ## newNum() function to roll new number.
        ## package roll into hash map

        roll = {1: 0, 2: 0, 3: 0,
                4: 0, 5: 0, 6: 0}

        for slot in self.slots:
            slot.newNum()
            number = int(slot.getNumber())
            roll[number] += 1


            ## update scorecard with a new roll
        self.playerCards[self.turn.get()].sendRoll(roll)

        ## special case: this is last spin
        if self.spinsLeft.get() == 0:
            self.spinButton.config(state='disabled')

    def beginClick(self):  ## Finished

        ## unlock spin button
        self.spinButton.config(state='normal')

        ## lock the control button and prime it to end turn
        self.controlButton.config(state='disabled')
        self.controlButton.config(bg='red', text='End Turn')
        self.controlButton.config(command=self.endClick)

        ## remove last players card and add new
        t = self.turn.get()
        self.playerCards[t - 1].grid_remove()
        self.playerCards[t].grid(row=0, column=1, rowspan=2, stick=NESW)

        ## set spins left to 3
        self.spinsLeft.set(3)

        ## update spins text
        self.spinsCountdown.config(text=self.spinsLeft.get())

    def endClick(self):  ## Finished
        ## lock spin button
        self.spinButton.config(state='disabled')

        ## prime the control button to begin turn
        self.controlButton.config(bg='green', text='Begin Turn')
        self.controlButton.config(command=self.beginClick)

        for slot in self.slots:
            slot.reset()

        ## finalize current player card

        t = self.turn.get()
        self.playerCards[t].finalize()

        ## increment turn
        self.turn.set((t + 1) % len(self.players))

    def __init__(self, playerNames):

        self.players = playerNames

        self.root = tk.Tk()

        self.turn = tk.IntVar()
        self.turn.set(0)

        self.spinsLeft = tk.IntVar()

        ####################################

        self.DIMENSION_SCALE = .7

        self.W_HEIGHT = self.root.winfo_screenheight() * self.DIMENSION_SCALE

        self.W_WIDTH = self.root.winfo_screenwidth() * self.DIMENSION_SCALE

        self.W_OFFSET = '+' + str(int((self.root.winfo_screenwidth() - self.W_WIDTH) / 2)) + '+' + str \
            (int((self.root.winfo_screenheight() - self.W_HEIGHT) / 2))

        self.SCREEN_DIMENSIONS = str(int(self.W_WIDTH)) + 'x' + str(int(self.W_HEIGHT)) + str(self.W_OFFSET)

        ####################################

        ## ROOT CONFIGURATION

        self.root.config(bg='black')
        self.root.geometry(self.SCREEN_DIMENSIONS)
        self.root.title('Ponzti!')

        for i, j in zip([0, 1],  # index
                        [1, 5]):  # weight
            self.root.rowconfigure(i, weight=j)

        for i, j in zip([0, 1],  # index
                        [5, 4]):  # weight
            self.root.columnconfigure(i, weight=j)

        ####################################

        ## SPINNER WINDOW

        self.slotsFrame = tk.Frame(self.root, bg='purple')
        self.slotsFrame.grid(row=1, column=0, sticky=NESW)

        self.slotsFrame.rowconfigure(0, weight=1)

        for i, j in zip([0, 1, 2, 3, 4, 5],  # index
                        [1, 1, 1, 1, 1, 1]):  # weight
            self.slotsFrame.columnconfigure(i, weight=j)

        self.slots = []

        for i in ([0, 1, 2, 3, 4]):
            self.slots.append(Slot(self.slotsFrame))
            self.slots[i].grid(row=0, column=i, padx=10, pady=5, sticky=NESW)

        self.spinButton = tk.Button(self.slotsFrame, bg='yellow', width=10, height=10, text='SPIN',
                                    command=self.spinClick, state='disabled')

        self.spinButton.grid(row=0, column=5, rowspan=2)

        ####################################

        ## CONTROL WINDOW

        self.controlFrame = tk.Frame(self.root, bg='cyan')
        self.controlFrame.grid(row=0, column=0, sticky=NESW)

        self.controlFrame.columnconfigure(0, weight=1)
        self.controlFrame.columnconfigure(1, weight=1)
        self.controlFrame.columnconfigure(2, weight=2)

        self.controlFrame.rowconfigure(0, weight=1)

        self.turnsLeft = tk.Label(self.controlFrame, text='Turns\nLeft: ', height=5, width=15)
        self.turnsLeft.grid(row=0, column=0)

        self.spinsCountdown = tk.Label(self.controlFrame, text='', height=5, width=15)
        self.spinsCountdown.grid(row=0, column=1)

        self.controlButton = tk.Button(self.controlFrame, bg='green', text='BEGIN TURN', height=5, width=20,
                                       command=self.beginClick)
        self.controlButton.grid(row=0, column=2)

        ####################################

        ## PLAYER CARDS

        self.playerCards = []

        for t in range(0, len(playerNames)):
            self.playerCards.append(
                ScoreSheet(self.root, ('Player ' + str(t + 1) + ': ' + playerNames[t]), self.controlButton))






