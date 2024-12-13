import tkinter as tk
import math

# Constants for representing the players and empty cells
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"

# The game board
board = [PLAYER_X, PLAYER_X, PLAYER_O,
         EMPTY, PLAYER_O, EMPTY,
         PLAYER_X, PLAYER_O, EMPTY]

# Function to check if a player has won
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != EMPTY:
            return board[combination[0]]
    
    if EMPTY not in board:
        return "tie"
    
    return None

# Function to evaluate the game board
def evaluate(board):
    winner = check_winner(board)
    
    if winner == PLAYER_X:
        return 1
    elif winner == PLAYER_O:
        return -1
    else:
        return 0

# Minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    winner = check_winner(board)
    if winner is not None or depth == 0:
        return evaluate(board)
    
    if maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                eval_score = minimax(board, depth - 1, alpha, beta, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                eval_score = minimax(board, depth - 1, alpha, beta, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval

# Function to find the best move using minimax with alpha-beta pruning
def find_best_move(board):
    best_score = -math.inf
    best_move = None
    
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER_X  # Assuming PLAYER_X is the human and PLAYER_O is the AI
            move_score = minimax(board, 9, -math.inf, math.inf, False)
            board[i] = EMPTY
            
            if move_score > best_score:
                best_score = move_score
                best_move = i
    
    return best_move

# Function to handle button click
def on_button_click(index):
    global board
    if board[index] == EMPTY:
        board[index] = PLAYER_X
        buttons[index].config(text=PLAYER_X, state=tk.DISABLED)
        winner = check_winner(board)
        
        if winner is None:
            ai_move = find_best_move(board)
            board[ai_move] = PLAYER_O
            buttons[ai_move].config(text=PLAYER_O, state=tk.DISABLED)
            winner = check_winner(board)
        
        if winner:
            end_game(winner)

# Function to end the game and display the result
def end_game(winner):
    if winner == "tie":
        result_text.set("It's a tie!")
    else:
        result_text.set(f"Player {winner} wins!")
    for button in buttons:
        button.config(state=tk.DISABLED)

# Function to reset the game
def reset_game():
    global board
    board = [EMPTY] * 9
    result_text.set("")
    for button in buttons:
        button.config(text="", state=tk.NORMAL)

# Creating the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Creating the game board buttons
buttons = []
for i in range(9):
    button = tk.Button(root, text=board[i] if board[i] != EMPTY else "", font=("Helvetica", 20), width=5, height=2,
                       command=lambda i=i: on_button_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Game result label
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Helvetica", 16))
result_label.grid(row=3, column=0, columnspan=3)

# Reset button


# Start the main loop
root.mainloop()
