class PlayerScore():

    def __init__(self):

        self.data = {}
        self.updates = {}

        ## two letter keywords will be used throughout rest of game implementation
        for i, t, f in (zip(['1s', '2s', '3s', '4s', '5s', '6s', '3k', '4k', 'ss', 'ls', 'fh', 'ch', 'po', 'ep'],
                            ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', '3 of a Kind', '4 of a Kind',
                             'Small\nStraight', 'Large\nStraight', 'Full\nHouse', 'Chance', 'Ponzti!', 'Extra\nPonzti'],
                            [self.score_1s, self.score_2s, self.score_3s, self.score_4s, self.score_5s, self.score_6s,
                             self.score_3k,
                             self.score_4k, self.score_ss, self.score_ls, self.score_fh, self.score_ch, self.score_po,
                             self.score_ep])):
            # Permanent layout
            self.data[i] = {'title': t, 'score': 0, 'locked': False, 'funct': f}

    def sendRoll(self, roll):
        self.updates = self.getScoreUpdates(roll)

    # returns hashmap of updates to unlocked scores
    def getScoreUpdates(self, roll):
        updates = {}
        for key, value in self.data.items():
            if not value.get('locked'):
                updates[key] = value.get('funct')(roll)
        return updates


    # simply sums and returns the scores of 1s to 6s and adds bonus if necessary
    def getUpperTotal(self, updateKey):
        runTot = 0
        for key in ['1s', '2s', '3s', '4s', '5s', '6s']:
            runTot += self.data[key].get('score')
            if key == updateKey:
                runTot += self.updates[updateKey]
        if runTot >= 63:
            runTot += 35

        return runTot

    # simply sums and returns 3k to ep
    def getLowerTotal(self, updateKey):
        runTot = 0
        for key in ['3k', '4k', 'ss', 'ls', 'fh', 'ch', 'po', 'ep']:
            runTot += self.data[key].get('score')
            if key == updateKey:
                runTot += self.updates[updateKey]

        return runTot

    ## a wrapper method to return the upper score, lower score, and their sum as a list. Can be unpacked and displayed in windows later
    def getTotalsUBT(self, updateKey):

        upper = self.getUpperTotal(updateKey)
        lower = self.getLowerTotal(updateKey)

        return [upper, lower, upper + lower]

    ## all scoring methods accept a hashmap of the occurrence of numbers 1-6 in a random set of 5 numbers in the range 1 - 6
    ## scoring conditions explains in Yahtzee rules

    @staticmethod
    def score_1s(occ):  ## Good
        return occ[1]

    @staticmethod
    def score_2s(occ):  ## Good
        return occ[2] * 2

    @staticmethod
    def score_3s(occ):  ## Good
        return occ[3] * 3

    @staticmethod
    def score_4s(occ):  ## Good
        return occ[4] * 4

    @staticmethod
    def score_5s(occ):  ## Good
        return occ[5] * 5

    @staticmethod
    def score_6s(occ):  ## Good
        return occ[6] * 6

    @staticmethod
    def score_3k(occ):  ## Good
        for i, n in enumerate(occ.values()):
            if n >= 3:
                runTot = 0
                for i, n in enumerate(occ.values()):
                    runTot += n * (i + 1)
                return runTot
        return 0;

    @staticmethod
    def score_4k(occ):  ## Good
        for i, n in enumerate(occ.values()):
            if n >= 4:
                runTot = 0
                for i, n in enumerate(occ.values()):
                    runTot += n * (i + 1)
                return runTot
        return 0;

    @staticmethod
    def score_ss(occ):

        search = 1

        if occ[1] == 0:
            search += 1
        if occ[2] == 0:
            search += 1

        for i in range(search, search + 4):

            if occ[i] == 0:
                return 0

        return 30

    @staticmethod
    def score_ls(occ):  ## Good

        search = 1
        if occ[1] == 0:
            search += 1

        for i in range(search, search + 5):

            if occ[i] == 0:
                return 0

        return 40

    @staticmethod
    def score_fh(occ):  ## Good
        if ((2 in occ.values()) and (3 in occ.values())):
            return 25
        return 0

    @staticmethod
    def score_ch(occ):  ## Good
        runTot = 0
        for i, n in enumerate(occ.values()):
            runTot += n * (i + 1)
        return runTot

    @staticmethod  ## Good
    def score_po(occ):

        if 5 in occ.values():
            return 50

        return 0

    def score_ep(self, occ):
        if self.data['po'].get('score') > 0:
            if 5 in occ.values():
                return 50

        return 0
