__author__ = 'bob'
import Yahtzee_Score_Sheet
import Five_Dice
import itertools
import logging



MOVE_OPTIONS = [tuple(), (1,), (2,), (3,), (4,), (5,), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5),
                (3, 4), (3, 5), (4, 5), (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5),
                (2, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 5), (1, 2, 3, 4), (1, 2, 3, 5), (1, 2, 4, 5),
                (1, 3, 4, 5), (2, 3, 4, 5), (1, 2, 3, 4, 5)]
SCORE_TEMPLATE = {'ones': (0, (1,)), 'twos': (0, (2,)), 'threes': (0, (3,)), 'fours': (0, (4,)),
                  'fives': (0, (5,)), 'sixes': (0, (6,)), 'three of a kind': (0, (1, 2, 3, 4, 5, 6)),
                  'four of a kind': (0, (1, 2, 3, 4, 5, 6)), 'full house': (25, (0, 0)),
                  'short straight': (30, (0,)), 'long straight': (40, (0,)),
                  'yahtzee': (50, (0,)), 'chance': (0, (1, 2, 3, 4, 5, 6))}
FACE_STRINGS = {1: 'ones', 2: 'twos', 3: 'threes', 4: 'fours', 5: 'fives', 6: 'sixes'}
PREFS = {'chance': 50, 'three of a kind': 40, 'four of a kind': 30, 'sixes': 35,
         'fives': 36, 'fours': 37, 'threes': 45, 'twos': 46, 'ones': 47,
         'full house': 29, 'yahtzee': 10}

def set_up_logging(level='info'):
    level = getattr(logging, level.upper())
    logging.basicConfig(filename='yahtzee.log',level=level,
                        format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: sorted tuple representing a full Yahtzee hand

    Returns a set of sorted tuples, where each tuple is dice to hold
    """
    if len(hand) == 0:
        return set([()])
    else:
        holds = set()
        face = hand[-1]
        hand = tuple(hand[:-1])
        for hold in gen_all_holds(hand):
            holds.add(hold)
            _hold = list(hold) + [face]
            holds.add(tuple(_hold))
        return holds

def possible_lines(faces, score_sheet):
    """
    returns a list (or None) of the possible lines that this throw
    could complete
    :type faces: tuple
    :type score_sheet: Yahtzee_Score_Sheet.YahtzeeScoreSheet
    :return: list
    """
    yahtzee = score_sheet.get_yahtzee()

    possibles = ['chance']
    faces_freq = {}
    for face in range(1,7):
        faces_freq[face] = 0
    for face in faces:
        faces_freq[face] += 1
    for face in (1, 2, 3, 4, 5, 6):
        if faces_freq[face] >= 2:
            possibles.append(FACE_STRINGS[face])
    freq_list = sorted(faces_freq.itervalues(), reverse=True)
    if freq_list[0] == 5:
        possibles.append('yahtzee')
        possibles.append('full house')
        if yahtzee:
            possibles.append('short straight')
            possibles.append('long straight')
    if freq_list[0] >= 4:
        possibles.append('four of a kind')
    if freq_list[0] == 3:
        if freq_list[1] == 2:
            possibles.append('full house')
    if freq_list[0] >= 3:
        possibles.append('three of a kind')
    face_list = sorted(set(faces))
    straight_length = 1
    max_straight_length = 1
    previous_face = -1
    for face in face_list:
        if face == previous_face + 1:
            straight_length += 1
            if straight_length > max_straight_length:
                max_straight_length = straight_length
        else:
            straight_length = 1
        previous_face = face
    if max_straight_length >= 4:
        possibles.append('short straight')
    if max_straight_length == 5:
        possibles.append('long straight')
    logging.debug('%s are the possible lines using %s', str(possibles), str(faces))
    return possibles

def score_dice(dice, line, score_sheet):
    """
    calculate the total score of the sheet.
    """
    temp_sheet = Yahtzee_Score_Sheet.YahtzeeScoreSheet(sheet=score_sheet)
    score = SCORE_TEMPLATE[line][0]
    for die in dice:
        if die in SCORE_TEMPLATE[line][1]:
            score += die
    logging.debug('%s is the score for %s with %s dice', str(score), line, str(dice))
    temp_sheet.update_line(line, score)
    result = temp_sheet.get_total()
    return result

def best_line(possibles, dice, score_sheet):

    best_score = 0
    best_move = None
    scores = score_sheet.get_scores()
    for line in possibles:
        if scores[line] == -1:
            score = score_dice(dice, line, score_sheet)
            logging.debug('score sheet total is %s using %s with dice %s', str(score), line, str(dice))
            if score > best_score:
                best_move = line
                best_score = score
                logging.debug('making %s the best line so far', line)
            elif score == best_score:
                if PREFS[line] < PREFS[best_move]:
                    best_move = line
                    best_score = score
                    logging.debug('making %s the best line so far', line)
    logging.info('%s is best line from %s using %s dice', best_move, str(possibles), str(dice))
    return best_move


def evaluate_move(hold, dice, scores):
    """
    Take a move (tuple of dice faces to re-throw), and a set of dice (tuple of the
    faces of 5 dice), and a Yahtzee score sheet. Calculates a representation
    of the expected value of the move. This is the sum of the scores of all
    possible results of the re-throw, unified as if there were all 7776 options.
    :param hold: tuple
    :param dice: tuple
    :param scores: YahtzeeScoreSheet
    :return: int
    """
    total_score = 0
    for new_faces in itertools.product((1, 2, 3, 4, 5, 6), repeat=len(hold)):
        _dice = dice.temp_swap_dice(hold, new_faces)
        if _dice in score_cache:
            total_score += score_cache[_dice]
        else:
            possibles = possible_lines(_dice, scores)
            best_move = best_line(possibles, _dice, scores)
            if best_move is not None:
                total_score += score_dice(_dice, best_move, scores)
                score_cache[_dice] = score_dice(_dice, best_move, scores)
            else:
                score_cache[_dice] = 0
    logging.debug('calculated %s for move %s', str(total_score), str(hold))
    return total_score * (7776, 1296, 216, 36, 6, 1)[len(hold)]

def strategy(dice, yss):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.
    """
    best_hold = None
    best_score = 0
    for hold in gen_all_holds(dice.get_dice()):
        this_score = evaluate_move(hold, dice, yss)
        if this_score > best_score:
            best_score = this_score
            best_hold = hold
    result = (best_score, best_hold)
    return result


set_up_logging('info')
yss = Yahtzee_Score_Sheet.YahtzeeScoreSheet()
evaluation = {}
score_cache = {}
dice = Five_Dice.FiveDice((5, 2, 3, 6, 5))
yss.update_line('chance', 20)
#yss.update_line('three of a kind', 20)
yss.update_line('sixes', 18)
yss.update_line('fives', 15)

print strategy(dice, yss)