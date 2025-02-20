import tkinter as tk

from PlayerData import PlayerScore

NESW = tk.N + tk.E + tk.S + tk.W


class ScoreSheetCell(tk.Frame):
    def __init__(self, root, title, method):
        self.amount = tk.StringVar()
        self.amount.set('')

        tk.Frame.__init__(self, root, bg='grey')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.label = tk.Label(self, width=1, bg='light grey', text=title, font=('roboto', 12), textvariable=title)
        self.label.grid(row=0, column=0, pady=1, padx=1, sticky=NESW)

        self.points = tk.Label(self, width=1, bg='light grey', fg='black', textvariable=self.amount)
        self.points.grid(row=0, column=1, pady=1, padx=1, sticky=NESW)

        self.points.bind('<Button-1>', self.click)

        ## this is a method inhereted from the score card object. It will call with itself as the parameter.
        ## will handle the updating of other cells in relation to its current state

        self.parentMethod = method

    def disable(self):
        self.points.unbind('<Button-1>')

    def click(self, event):
        if self.amount.get() == '':
            return
        self.parentMethod(self)

    def suggest(self, new):
        self.amount.set(str(new))
        self.points.config(bg='yellow')

    def predict(self, prediction):
        self.amount.set(str(prediction))
        self.points.config(bg='light blue')

    def reset(self):
        self.points.config(bg='light grey')


class SpecialScoreCell(ScoreSheetCell):

    def __init__(self, root, title):
        ScoreSheetCell.__init__(self, root, title, None)

        self.progressText = tk.StringVar()
        self.progressText.set('')
        self.columnconfigure(2, weight=1)

        self.progress = tk.Label(self, width=1, bg='light grey', textvariable=self.progressText)
        self.progress.grid(row=0, column=2, padx=1, pady=1, sticky=NESW)

    def predict(self, prediction):

        if prediction >= 63:
            self.amount.set('+35')
            self.points.config(bg='light blue')
            self.progressText.set(str(prediction - 35) + '/63')
        else:
            self.amount.set('')
            self.points.config(bg='light grey')
            self.progressText.set(str(prediction) + '/63')

    def reset(self):

        self.points.config(bg='light grey')
        self.progress.config(bg='light grey')


class ExtraPonztiCell(ScoreSheetCell):
    def __init__(self, root, title):
        ScoreSheetCell.__init__(self, root, title, None)

    def click(self, event):
        amount = self.amount.get()
        if amount == '' or amount == '0':
            return
        self.parentMethod(self)


class ScoreSheet(tk.Frame):

    def __init__(self, root, name, button):

        ## create player score data object
        self.score = PlayerScore()

        ## parent button will control the position of the scoresheet based upon the internal conditions of the score sheet
        self.parentButton = button

        ## construct frame
        tk.Frame.__init__(self, root, bg='black')

        ## configure frame grid
        for i, j in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  # index
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]):  # weight
            self.rowconfigure(i, weight=j)

        for i, j in zip([0, 1],  # index
                        [1, 1]):  # weight
            self.columnconfigure(i, weight=j)

        ## hash map to store score component cells
        self.cells = {}

        ## holds reference to cell that is selected by player click
        self.selection = None

        ## initialize score component cells with corresponding titles and a method to interact with this object
        for key, point in self.score.data.items():
            self.cells[key] = ScoreSheetCell(self, point['title'], self.cellClick)

        ## simple title
        self.title = tk.Label(self, text=name)
        self.title.grid(column=0, row=0, columnspan=2, sticky=NESW)

        ## simple total sections that will be updated often
        self.upperTotal = ScoreSheetCell(self, 'UPPER TOTAL', None)
        self.upperTotal.disable()
        self.upperTotal.grid(column=0, row=5, columnspan=2, sticky=NESW)

        self.lowerTotal = ScoreSheetCell(self, 'LOWER TOTAL', None)
        self.lowerTotal.disable()
        self.lowerTotal.grid(column=0, row=10, columnspan=2, sticky=NESW)

        self.finalTotal = ScoreSheetCell(self, 'FINAL SCORE', None)
        self.finalTotal.disable()
        self.finalTotal.grid(column=0, row=11, columnspan=2, sticky=NESW)

        self.title.grid(column=0, row=0, columnspan=2, sticky=NESW)

        ## manually place all the cells

        self.cells['1s'].grid(row=1, column=0, sticky=NESW)
        self.cells['2s'].grid(row=1, column=1, sticky=NESW)
        self.cells['3s'].grid(row=2, column=0, sticky=NESW)
        self.cells['4s'].grid(row=2, column=1, sticky=NESW)
        self.cells['5s'].grid(row=3, column=0, sticky=NESW)
        self.cells['6s'].grid(row=3, column=1, sticky=NESW)

        self.extraCell = SpecialScoreCell(self, self.score.data['ep']['title'])
        self.extraCell.grid(row=4, column=0, columnspan=2, sticky=NESW)
        self.extraCell.disable()

        self.cells['3k'].grid(row=6, column=0, sticky=NESW)
        self.cells['4k'].grid(row=6, column=1, sticky=NESW)
        self.cells['ss'].grid(row=7, column=0, sticky=NESW)
        self.cells['ls'].grid(row=7, column=1, sticky=NESW)
        self.cells['fh'].grid(row=8, column=0, sticky=NESW)
        self.cells['ch'].grid(row=8, column=1, sticky=NESW)
        self.cells['po'].grid(row=9, column=0, sticky=NESW)
        self.cells['ep'].grid(row=9, column=1, sticky=NESW)

    def suggestCells(self, updates):
        self.upperTotal.reset()
        self.lowerTotal.reset()
        self.finalTotal.reset()
        self.selection = None
        ## suggest cells that correspond to unlocked score components
        for key, value in updates.items():
            self.cells[key].suggest(value)

            ## start of suggesting sequence, ending turn should not be allowed
            self.parentButton.config(state=tk.DISABLED)

    def sendRoll(self, roll):
        ## activate calculations in the player score object
        self.score.sendRoll(roll)
        ## light up the score sheet the newly calculated updates
        self.suggestCells(self.score.updates)

    def cellClick(self, clicked):
        if clicked.amount == '':
            return

        ## if there is a selection already, make sure it is yellow now
        if self.selection != None:
            self.selection.points.config(bg='yellow')
        ## change selected to green
        clicked.points.config(bg='green')
        ## change the reference the clicked cell
        self.selection = clicked
        ## ending turn is allowed now
        self.parentButton.config(state=tk.NORMAL)

        ## show predictions of final score based on selection.
        ## getTotalsUBT will return a list of length 3 containing [upper score, bottom score, total score]
        for key, value in self.cells.items():
            if value == self.selection:
                predictions = self.score.getTotalsUBT(key)
                self.upperTotal.predict(predictions[0])
                self.lowerTotal.predict(predictions[1])
                self.finalTotal.predict(predictions[2])
                self.extraCell.predict(predictions[0])

    def finalize(self):
        for key, cell in self.cells.items():
            cell.reset()
            ## search by comparing instances in cell set against selection instance
            if cell == self.selection:
                ## disable the selected cell
                cell.disable()
                ## grab the score data corresponding to the cell
                dataSection = self.score.data.get(key)
                ## update the score value and lock the score
                dataSection['score'] = self.score.updates[key]
                dataSection['locked'] = True
            else:
                ## clear the potential value from the unselected boxes
                if not self.score.data[key].get('locked'):
                    cell.amount.set('')
        ## values in total sections will already be correct from predictions
        self.upperTotal.reset()
        self.lowerTotal.reset()
        self.finalTotal.reset()
        self.extraCell.reset()
        self.selection = None


