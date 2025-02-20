import tkinter as tk

import random, time


class Slot(tk.Frame):
    def __init__(self, root):

        self.locked = False

        self.value = tk.StringVar()
        self.value.set('')

        tk.Frame.__init__(self, root, bg='orange')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.label = tk.Label(self, bg='white', width=10, height=5, textvariable=self.value)
        self.label.grid(row=0, column=0)

        self.button = tk.Button(self, bg='green', width=10, height=5, command=self.lockClick)
        self.button.grid(row=1, column=0)

    ## used after a turn is over to convert slots to default state
    def reset(self):
        self.locked = False
        self.button.config(bg='green')
        self.value.set('')

    ## method switches state of locked boolean and alternates the color
    def lockClick(self):
        ## no need to lock a slot if you are not saving a roll
        if self.value.get() == '':
            return

        if self.locked:
            self.locked = False
            self.button.config(bg='green')
        elif not self.locked:
            self.locked = True
            self.button.config(bg='red')

    ## method simply returns value displayed in slot
    def getNumber(self):
        return self.value.get()

    ## updates number displayed in slot if it is unlocked
    def newNum(self):

        if not self.locked:
            self.value.set(str(self.get1To6()))

    @staticmethod
    ## static method returns random number in range 1-6.

    ## uses system time as seed for generator.
    ## however, it generates too fast to change the time float value
    ## so, generate an additional number using the previous seed to change it in a unique way, and then add it to the next seed

    def get1To6():
        random.seed(time.time() + random.random())

        return random.randint(1, 6)


