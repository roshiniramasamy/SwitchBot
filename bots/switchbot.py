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

    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=6):
        self.__randomize = randomize
        self.__max_depth = depth

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

    def heuristic_strategy(self, state):

        phase = state.get_phase()
        opponents_card = state.get_opponents_played_card()

        if phase == 1:
            moves = state.moves()

        # If the opponent has played a card
            if opponents_card is not None:

                """Case: play lowest card"""

                lowest_card = moves[0]
                for index, move in enumerate(moves):
                    if move[0] is not None and move[0] % 5 >= lowest_card[0] % 5:
                        lowest_card = move
                return lowest_card

            # We lead
            else:

                """Case: play highest card"""

                highest_card = moves[0]
                for index, move in enumerate(moves):
                    if move[0] is not None and move[0] % 5 <= highest_card[0] % 5:
                        highest_card = move
                return highest_card


        else:
            val, move = self.value(state)

            return move

        moves = state.moves()
        move = moves[1]

        return move

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        decide_strategy = random.randint(1,2)

        if decide_strategy == 1:
            move = self.reasoning_strategy(state)

        else:
            move = self.heuristic_strategy(state)

        return move

    def value(self, state, depth = 0):
        # type: (State, int) -> tuple[float, tuple[int, int]]
        """
        Return the value of this state and the associated move
        :param state:
        :param depth:
        :return: A tuple containing the value of this state, and the best move for the player currently to move
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == self.__max_depth:
            return heuristic(state)

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a recursive function call so that 'value' will contain the
            # mini max value of 'next_state'
            value, _ = self.value(next_state)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move


def maximizing(state):
    # type: (State) -> bool
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1


def heuristic(state):
    # type: (State) -> float
    """
    Estimate the value of this state: -1.0 is a certain win for player 2, 1.0 is a certain win for player 1

    :param state:
    :return: A heuristic evaluation for the given state (between -1.0 and 1.0)
    """
    return util.ratio_points(state, 1) * 2.0 - 1.0, None


def eval_points(opponents_card, move):

    if opponents_card is None or move is None:
        raise RuntimeError("An incomplete trick was attempted to be evaluated.")

    # If the two cards of the trick have the same suit
    if Deck.get_suit(opponents_card[0]) == Deck.get_suit(move[0]):
        # We only compare indices since the convention we defined in Deck
        # puts higher rank cards at lower indices, when considering the same color.
        return 1 if opponents_card < move else 2

    if Deck.get_suit(opponents_card[0]) == self.__deck.get_trump_suit():
        return 1

    if Deck.get_suit(move[0]) == self.__deck.get_trump_suit():
        return 2
