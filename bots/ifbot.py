"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
from api import util
import random


class Bot:

    def __init__(self):
        pass

    def reasoning_strategy(self, state):

        opponents_card = state.get_opponents_played_card()

        # If the opponent has played a card
        if opponents_card is not None:

            moves = state.moves()

            """Case: following suit with higher card"""
            moves_same_suit = []
            # Get all moves of the same suit as the opponent's played card
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(opponents_card):
                    moves_same_suit.append(move)

            if len(moves_same_suit) > 0:
                highest_move = moves_same_suit[0]
                for index, move in enumerate(moves_same_suit):
                    if move[0] is not None and move[0] % 5 <= highest_move[0] % 5:
                        highest_move = move

                if highest_move[0] % 5 < opponents_card % 5:
                    return highest_move

            """Case: play trump"""
            moves_trump_suit = []
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    moves_trump_suit.append(move)

            if len(moves_trump_suit) > 0:
                lowest_trump_move = moves_trump_suit[0]
                for index, move in enumerate(moves_trump_suit):
                    if move[0] is not None and move[0] % 5 <= lowest_trump_move[0] % 5:
                        lowest_trump_move = move
                return lowest_trump_move

            """Case: play lowest card"""

            lowest_card = moves[0]
            for index, move in enumerate(moves):
                if move[0] is not None and move[0] % 5 >= lowest_card[0] % 5:
                    lowest_card = move
            return lowest_card

        # If we lead
        else:
            moves = state.moves()

            '''Checks for marriage'''
            for move in moves:

                if move[0] is not None and move[1] is not None:
                    # print('################################################################ MARRIAGE')
                    for card in moves:
                        if card[0] == move[0] + 1:

                            return card

            '''Checks for jack exchange'''
            for move in moves:
                if move[0] is None and move[1] is not None:
                    # print('################################################################ JACK EXCHANGE')

                    return move

            '''Play jack'''
            for move in moves:
                if move[0] is 4 or move[0] is 9 or move[0] is 14 or move[0] is 19:
                    trump_suit = state.get_trump_suit()
                    card_suit = Deck.get_suit(move[0])

                    if not(trump_suit == card_suit):
                        # print('################################################################ JACK PLAY')

                        return move

            '''Play non trump 10 if available'''
            for move in moves:
                if move[0] is 1 or move[0] is 6 or move[0] is 11 or move[0] is 16:
                    if Deck.get_suit(move[0]) != state.get_trump_suit():
                        return move

            '''Play non trump Ace if available'''
            for move in moves:
                if move[0] is 0 or move[0] is 5 or move[0] is 10 or move[0] is 15:
                    if Deck.get_suit(move[0]) != state.get_trump_suit():
                        return move

            """Case: play lowest non trump card"""

            while True:
                lowest_card = moves[0]
                for index, move in enumerate(moves):
                    if move[0] is not None and move[0] % 5 >= lowest_card[0] % 5:
                        lowest_card = move
                if Deck.get_suit(lowest_card[0]) != state.get_trump_suit():
                    break
                else:
                    if len(moves) == 1:
                        return lowest_card
                    moves.remove(lowest_card)
            return lowest_card


    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        move = self.reasoning_strategy(state)

        return move
