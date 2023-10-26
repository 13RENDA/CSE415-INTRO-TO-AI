'''
shiyuc9KInARow.py
Author: Shiyu Chen
An agent for playing "K-in-a-Row with Forbidden Squares"
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

import time

# Global variables to hold information about the opponent and game version:
INITIAL_STATE = None
OPPONENT_NICKNAME = 'Not yet known'
OPPONENT_PLAYS = 'O' # Update this after the call to prepare.

# Information about this agent:
MY_LONG_NAME = 'Templatus Skeletus'
MY_NICKNAME = 'Tea-ess'
I_PLAY = 'X' # Gets updated by call to prepare.

 
# GAME VERSION INFO
M = 0
N = 0
K = 0
TIME_LIMIT = 0
 
 
############################################################
# INTRODUCTION
def introduce():
    intro = '\nMy name is BrendaHereToChill.\n'+\
            '"Shiyuc9" made me.\n'+\
            'Somebody please turn me into a real game-playing agent!\n' 
    return intro
 
def nickname():
    return 'BrenBren'
 
############################################################

# Receive and acknowledge information about the game from
# the game master:
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    # Write code to save the relevant information in either
    # global variables.
    INITIAL_STATE=initial_state
    K=k
    I_PLAY=what_side_I_play
    OPPONENT_NICKNAME=opponent_nickname
    
    return "OK"
 
############################################################
 
def makeMove(currentState, currentRemark, timeLimit=10000):
    print("makeMove has been called")

    # Use minimax to decide the move
    best_move = minimax_decision(currentState)

    # Apply the chosen move to get the new state
    new_state = apply_move(currentState, best_move)
    # Check for a winning condition
    # if check_winner(new_state[0], I_PLAY):
    #     newRemark = "I won! Game over."
    #     return [[best_move, new_state], newRemark]

    newRemark = "I made my move at {}. Your turn!".format(best_move)

    print("Returning from makeMove")
    return [[best_move, new_state], newRemark]

# Helper function to make the move decision using minimax
def minimax_decision(state):
    result = minimax(state, depthRemaining=3)  # Set the desired depth
    return result[1]  # The second element is the best move

##########################################################################
 
# The main adversarial search function:
def minimax(state, depthRemaining, pruning=True, alpha=float('-inf'), beta=float('inf'), zHashing=True):
    # Base case: If depthRemaining is zero, return the static evaluation
    if depthRemaining == 0:
        return [staticEval(state)]

    best_value = float('-inf') if state[1] == 'X' else float('inf')
    best_move = None

    for move in generate_legal_moves(state):
        # Apply the move to get the new state
        new_state = apply_move(state, move)

        # Recursive call to minimax with reduced depth
        result = minimax(new_state, depthRemaining - 1, pruning, alpha, beta, zHashing)

        # Extract the numeric value from the result
        value = result[0]


        # Update best value and move based on the player
        if state[1] == 'X':
            if value > best_value:
                best_value = value
                best_move = move
            # Update alpha for pruning
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            # Update beta for pruning
            beta = min(beta, best_value)

        # Pruning: break out of the loop if the condition is met
        if pruning and alpha >= beta:
            break

    # Optional: You can return additional information if needed
    return [best_value, best_move]

# Helper function to generate legal moves based on the current state
def generate_legal_moves(state):
    legal_moves = []
    for i in range(len(state[0])):
        for j in range(len(state[0][0])):
            if state[0][i][j] == ' ':
                legal_moves.append([i, j])
    return legal_moves

# Helper function to apply a move to the state
def apply_move(state, move):
    # Create a new list for the board
    new_board = [row[:] for row in state[0]]
    new_board[move[0]][move[1]] = state[1]
    # Create a new state with the copied board and player
    new_state = [new_board, 'O' if state[1]=='X' else 'X']
    return new_state

# Helper function to check if a square is forbidden
# def is_forbidden_square(state, move):
#     return state[move[0]][move[1]] == '-'

# Helper function to check if the game is over
def game_over(state):
    return check_winner(state, 'X') or check_winner(state, 'O') or not generate_legal_moves(state)

##########################################################################
    
# Helper function to check for a winning condition
def check_winner(state, player):
    # Check rows, columns, and diagonals for K in a row
    for i in range(len(state)):
        for j in range(len(state[0][0])):
            if state[i][j] == player:
                if check_line(state, i, j, player, 1, 0) or \
                   check_line(state, i, j, player, 0, 1) or \
                   check_line(state, i, j, player, 1, 1) or \
                   check_line(state, i, j, player, 1, -1):
                    return True
    return False

# Helper function to check a line for K in a row
def check_line(state, row, col, player, row_increment, col_increment):
    K = max(M, N)
    for _ in range(K):
        if not (0 <= row < M and 0 <= col < N) or state[row][col] != player:
            return False
        row += row_increment
        col += col_increment
    return True
 
##########################################################################
def staticEval(state):
    # Assuming 'X' is the maximizing player and 'O' is the minimizing player
    x_score = count_winning_lines(state[0], 'X')
    o_score = count_winning_lines(state[0], 'O')

    # Return the difference in scores (higher is better for 'X', lower is better for 'O')
    return x_score - o_score

def count_winning_lines(state, player):
    # Count the number of potential winning lines for the given player

    # Initialize count
    count = 0

    # Check rows
    count += count_winning_lines_in_directions(state, player, 1, 0, K)
    # Check columns
    count += count_winning_lines_in_directions(state, player, 0, 1, K)
    # Check diagonals
    count += count_winning_lines_in_directions(state, player, 1, 1, K)
    count += count_winning_lines_in_directions(state, player, 1, -1, K)

    return count

def count_winning_lines_in_directions(state, player, delta_row, delta_col, k):
    # Count winning lines in a given direction
    count = 0

    for i in range(len(state)):
        for j in range(len(state[0])):
            # Check if the current position can be the start of a winning line
            if state[i][j] == player:
                # Check in the specified direction
                win_line = True
                for step in range(1, k):
                    row = i + step * delta_row
                    col = j + step * delta_col

                    # Check if the position is within the bounds and has the player's token
                    if 0 <= row < len(state) and 0 <= col < len(state) and state[row][col] == player:
                        continue
                    else:
                        win_line = False
                        break

                if win_line:
                    count += 1

    return count
