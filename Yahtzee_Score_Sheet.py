__author__ = 'bob'

LINES = ('ones', 'twos', 'threes', 'fours', 'fives', 'sixes',
         'three of a kind', 'four of a kind', 'full house', 'yahtzee bonus',
         'short straight', 'long straight', 'yahtzee', 'chance', 'bonus',
         'above the line total', 'below the line total', 'total')
ABOVE_LINE = ('ones', 'twos', 'threes', 'fours', 'fives', 'sixes')
BELOW_LINE = ('three of a kind', 'four of a kind', 'full house', 'yahtzee bonus',
              'short straight', 'long straight', 'yahtzee', 'chance')
PRINT_LIST = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes', 'above the line total', 'bonus',
              'three of a kind', 'four of a kind', 'full house', 'short straight', 'long straight',
              'yahtzee', 'chance', 'yahtzee bonus', 'below the line total', 'total']

class YahtzeeScoreSheet:
    """
    Class to implement a score sheet for the Yahtzee Game
    """
    def __init__(self, sheet=None):
        """

        :type sheet: YahtzeeScoreSheet
        """
        self.sheet_lines = {}
        self.yahtzee = False
        if sheet is None:
            for line in LINES:
                self.sheet_lines[line] = -1
            for line in ('above the line total', 'below the line total', 'total',
                         'bonus', 'yahtzee bonus'):
                self.sheet_lines[line] = 0
        else:
            self.yahtzee = sheet.get_yahtzee()
            for line in LINES:
                self.sheet_lines[line] = sheet.sheet_lines[line]


    def clone(self):
        """

        :type sheet: YahtzeeScoreSheet
        """
        return YahtzeeScoreSheet(sheet=self)

    def get_yahtzee(self):
        return self.yahtzee

    def get_scores(self):
        """
        returns a dictionary of all the lines on the score sheet.
        :return: dict
        """
        output_dict = {}
        for line in LINES:
            output_dict[line] = self.sheet_lines[line]
        return output_dict

    def get_total(self):
        return self.sheet_lines['total']

    def __str__(self):
        a = ''
        for line in PRINT_LIST:
            a = a + ''.join((line, ' ' * (25 - len(line) - len(str(self.sheet_lines[line]))),
                             str(self.sheet_lines[line]), '\n'))
        return a

    def update_totals(self):
        self.sheet_lines['above the line total'] = self.sheet_lines['below the line total'] = self.sheet_lines['total'] = 0
        for line in [dummy for dummy in ABOVE_LINE if self.sheet_lines[dummy] > 0]:
            self.sheet_lines['above the line total'] += self.sheet_lines[line]
        if self.sheet_lines['above the line total'] >= 63:
            self.sheet_lines['bonus'] = 35
#            self.sheet_lines['above the line total'] += 35
        for line in [dummy for dummy in BELOW_LINE if self.sheet_lines[dummy] > 0]:
            self.sheet_lines['below the line total'] += self.sheet_lines[line]
        self.sheet_lines['total'] = self.sheet_lines['above the line total'] + \
                                    self.sheet_lines['below the line total'] + \
                                    self.sheet_lines['bonus']

    def update_line(self, line, score):
        self.sheet_lines[line] = score
        if line == 'yahtzee' and score == 50:
            self.yahtzee = True
        self.update_totals()



