"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

class IllegalMoveError(Exception):
    pass

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state() or terminal(board):
        return X
    num_x, num_o, _ = count_symbol(board)

    if num_x > num_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()

    width = len(board[0])
    height = len(board)

    for i in range(height):
        for j in range (width):
            if board[i][j] == None:
                possible_moves.add((i, j))
    
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] != None:
        raise IllegalMoveError

    current_player = player(board)
    new_board[action[0]][action[1]] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][0] != None:
        return board[0][0]
    elif board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][0] != None:
        return board[1][0]
    elif board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][0] != None:
        return board[2][0]
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] != None:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] != None:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] != None:
        return board[0][2]
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != None:
        return board[0][2]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    _, _, num_none = count_symbol(board)

    if winner(board) != None or num_none == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_ = winner(board)

    if winner_ == X:
        return 1
    elif winner_ == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    states_searched = 0

    def max_value(board, current_min = float('inf')):
        """
        Takes the current board state and current minimum value of the state resulting from doing one of the possible actions (This is given as 
        input to implement alpha-beta pruning)
        This function should return the value of the current state and all the actions that can be taken in the current state (for the max player), 
        such that the value of the board obtained by doing this action is maximum
        """
        nonlocal states_searched

        if terminal(board):
            return (utility(board), None)
        
        value = float('-inf')
        current_max = float('-inf')
        value_dictionary = dict()
        
        for action in actions(board):
            states_searched += 1
            action_value, _ = min_value(result(board, action), current_max)
            current_max = max(current_max, action_value)
            value_dictionary.update({action : action_value})
            value = max(value, action_value)

            if action_value > current_min:
                return (value, None)
        
        optimal_actions = [k for k,v in value_dictionary.items() if v == value]
        return (value, optimal_actions)

    def min_value(board,  current_max = float('-inf')):
        """
        Takes the current board state and current maximum value of the state resulting from doing one of the possible actions (This is given as 
        input to implement alpha-beta pruning)
        This function should return the value of the current state and  all the actions that can be taken in the current state (for the min player), 
        such that the value of the board obtained by doing this action is minimum
        """
        nonlocal states_searched

        if terminal(board):
            return (utility(board), None)
        
        value = float('inf')
        current_min = float('inf')
        value_dictionary = dict()
        
        for action in actions(board):
            states_searched += 1
            action_value, _ = max_value(result(board, action), current_min)
            current_min = min(current_min, action_value)
            value_dictionary.update({action : action_value})
            value = min(value, action_value)

            if action_value < current_max:
                return (value, None)
        
        optimal_actions = [k for k,v in value_dictionary.items() if v == value]
        return (value, optimal_actions)
    

    if terminal(board):
        return None
    
    current_player = player(board)

    # We choose a random optimal move

    if current_player == X:
        _, optimal_actions = max_value(board)
        print(f"{states_searched} states searched")
        return random.choice(optimal_actions)
    elif current_player == O:
        _, optimal_actions = min_value(board)
        print(f"{states_searched} states searched")
        return random.choice(optimal_actions)
    
def count_symbol(board):
    """
    Returns the number of times X and O occurs in the current board configuration
    """
    num_x, num_o, num_none = 0, 0, 0
    width = len(board[0])
    height = len(board)

    for i in range(height):
        for j in range(width):
            if board[i][j] == X:
                num_x += 1
            elif board[i][j] == O:
                num_o += 1
            elif board[i][j] == None:
                num_none += 1
            
    
    return (num_x, num_o, num_none)