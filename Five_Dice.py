__author__ = 'bob'
import random


class FiveDice:

    def __init__(self, dice=None):
        """
        create a FiveDice instance from the dice provided or randomised
        :param dice: tuple
        :return: FiveDice
        """
        if dice is None:
            self.dice = [1, 1, 1, 1, 1]
            self.throw((1, 2, 3, 4, 5))
        else:
            assert len(dice) == 5
            self.dice = list(dice)

    def clone(self):
        """
        Clones the dice
        :return: FiveDice
        """
        return FiveDice(self.dice)

    def throw(self, move):
        """
        replace the face of the dice in move with a new random face
        :param move: tuple
        :return: None
        """
        for dice_index in move:
            self.dice[dice_index - 1] = random.randint(1,6)

    def get_dice(self):
        """
        return the faces of the dice as a tuple
        :return: tuple
        """
        return tuple(sorted(self.dice))

    def temp_swap_dice(self, move, new_faces):
        """
        Takes the faces from new_dice and replaces the faces in current dice with
        faces indicated in move.
        Returns a tuple, does not change dice.
        :type move: tuple
        """
        assert len(move) == len(new_faces)
        output = list(self.dice)
        for face in move:
            output.remove(face)
        for face in new_faces:
            output.append(face)
        return tuple(sorted(output))


    def __str__(self):
        """
        return a human readable string of the five dice
        :return:string
        """
        out_string = ''
        for die in self.dice:
            out_string = out_string + str(die) + ', '
        return out_string[:-2]


