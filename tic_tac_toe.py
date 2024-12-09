import random

# Constants for player symbols
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

# Function to print the game board with coordinates
def print_board(board):
    board_size = len(board)
    print("   " + "   ".join(map(str, range(board_size))))
    for idx, row in enumerate(board):
        print(f"{idx}  " + " | ".join(row))
        if idx < board_size - 1:
            print("  " + "-" * (4 * board_size - 1))

# Function to check if the game is over
def is_game_over(board):
    board_size = len(board)
    # Check rows and columns
    for i in range(board_size):
        if board[i][0] != EMPTY and all(board[i][j] == board[i][0] for j in range(board_size)):
            return board[i][0]
        if board[0][i] != EMPTY and all(board[j][i] == board[0][i] for j in range(board_size)):
            return board[0][i]

    # Check diagonals
    if board[0][0] != EMPTY and all(board[i][i] == board[0][0] for i in range(board_size)):
        return board[0][0]
    if board[0][board_size - 1] != EMPTY and all(board[i][board_size - i - 1] == board[0][board_size - 1] for i in range(board_size)):
        return board[0][board_size - 1]

    # Check for draw
    if all(cell != EMPTY for row in board for cell in row):
        return "Draw"

    return None

# Function to get the opponent's symbol
def get_opponent(player):
    return PLAYER_O if player == PLAYER_X else PLAYER_X

# Minimax algorithm with memoization and Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player, player, memo={}):
    board_tuple = tuple(tuple(row) for row in board)
    if (board_tuple, depth, maximizing_player) in memo:
        return memo[(board_tuple, depth, maximizing_player)]

    winner = is_game_over(board)
    if winner or depth == 0:
        score = evaluate_board(board, player)
        memo[(board_tuple, depth, maximizing_player)] = score
        return score

    board_size = len(board)
    if maximizing_player:
        max_eval = float('-inf')
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == EMPTY:
                    board[i][j] = player
                    eval = minimax(board, depth - 1, alpha, beta, False, player, memo)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        memo[(board_tuple, depth, maximizing_player)] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        opponent = get_opponent(player)
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == EMPTY:
                    board[i][j] = opponent
                    eval = minimax(board, depth - 1, alpha, beta, True, player, memo)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        memo[(board_tuple, depth, maximizing_player)] = min_eval
        return min_eval

# Function to evaluate the board for the AI player
def evaluate_board(board, player):
    winner = is_game_over(board)
    if winner == player:
        return 10
    elif winner == get_opponent(player):
        return -10
    return 0  # Neutral if no immediate winner

# Function to make the AI's move
def make_ai_move(board, player, depth):
    best_score = float('-inf')
    best_move = None
    board_size = len(board)
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == EMPTY:
                board[i][j] = player
                score = minimax(board, depth - 1, float('-inf'), float('inf'), False, player)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = player
        print(f"Computer ({player}) placed at {best_move[0]}, {best_move[1]}")

# Main game loop
def play_game():
    board_size = 3
    # board_size = int(input("Enter the board size (e.g., 3 for 3x3): "))
    board = [[EMPTY] * board_size for _ in range(board_size)]
    current_player = random.choice([PLAYER_X, PLAYER_O])
    first_player = current_player
    game_mode = input("Choose game mode:\n1. Human vs Computer\n2. Computer vs Computer\nEnter 1 or 2: ")
    
    if game_mode == "1":
        while True:
            print_board(board)
            result = is_game_over(board)
            if result:
                break
            
            if current_player == PLAYER_X:
                print("\nHuman's turn:")
                try:
                    move = input("Enter your move (row and column): ")
                    row, col = map(int, move.split())
                    if not (0 <= row < board_size and 0 <= col < board_size) or board[row][col] != EMPTY:
                        raise ValueError
                    board[row][col] = PLAYER_X
                except ValueError:
                    print("Invalid move. Try again.")
                    continue
            else:
                print("\nComputer's turn:")
                make_ai_move(board, PLAYER_O, 3)

            current_player = get_opponent(current_player)
    elif game_mode == "2":
        depth_x = int(input("Enter search depth for PLAYER_X: "))
        depth_o = int(input("Enter search depth for PLAYER_O: "))
        while True:
            print_board(board)
            result = is_game_over(board)
            if result:
                break

            if current_player == PLAYER_X:
                print("\n")
                make_ai_move(board, PLAYER_X, depth_x)
            else:
                print("\n")
                make_ai_move(board, PLAYER_O, depth_o)

            current_player = get_opponent(current_player)
    else:
        print("Invalid game mode.")
        return

    print("\n")
    print_board(board)
    result = is_game_over(board)
    if result == "Draw":
        print("The game is a draw!")
    else:
        print(f"{result} wins!")
    print(f"The first player was: {first_player}")

# Run the game
if __name__ == "__main__":
    play_game()
