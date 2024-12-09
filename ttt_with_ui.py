import tkinter as tk
from tkinter import messagebox
import random

# Constants
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

class TicTacToeGame:
    def __init__(self, root, board_size=3):
        self.root = root
        self.board_size = board_size
        self.board = [[EMPTY] * board_size for _ in range(board_size)]
        self.current_player = random.choice([PLAYER_X, PLAYER_O])
        self.first_player = self.current_player
        self.buttons = []
        self.game_mode = None  # Game mode: "Human vs AI", "AI vs AI", or "Human vs Human"
        self.create_ui()
    
    def create_ui(self):
        self.root.title("Tic Tac Toe")
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                btn = tk.Button(self.root, text=EMPTY, font=("Arial", 24), width=3, height=1,
                                command=lambda x=i, y=j: self.make_human_move(x, y))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        self.status_label = tk.Label(self.root, text="Choose a game mode", font=("Arial", 16))
        self.status_label.grid(row=self.board_size, column=0, columnspan=self.board_size)

        self.human_vs_ai_btn = tk.Button(self.root, text="Human vs AI", command=self.start_human_vs_ai)
        self.human_vs_ai_btn.grid(row=self.board_size + 1, column=0)

        self.ai_vs_ai_btn = tk.Button(self.root, text="AI vs AI", command=self.start_ai_vs_ai)
        self.ai_vs_ai_btn.grid(row=self.board_size + 1, column=1)

        self.human_vs_human_btn = tk.Button(self.root, text="Human vs Human", command=self.start_human_vs_human)
        self.human_vs_human_btn.grid(row=self.board_size + 1, column=2)

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=self.board_size + 2, column=0, columnspan=self.board_size)

    def start_human_vs_ai(self):
        self.game_mode = "Human vs AI"
        self.status_label.config(text=f"Your turn ({self.current_player})")
    
    def start_ai_vs_ai(self):
        self.game_mode = "AI vs AI"
        self.status_label.config(text="AI vs AI mode started")
        self.root.after(500, self.ai_vs_ai_turn)

    def start_human_vs_human(self):
        self.game_mode = "Human vs Human"
        self.status_label.config(text=f"{self.current_player}'s turn")

    def make_human_move(self, row, col):
        if self.game_mode not in ["Human vs AI", "Human vs Human"]:
            return
        if self.board[row][col] == EMPTY:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_game_over():
                return
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            if self.game_mode == "Human vs AI" and self.current_player == PLAYER_O:
                self.status_label.config(text="Computer's turn")
                self.root.after(500, self.make_computer_move)
            else:
                self.status_label.config(text=f"{self.current_player}'s turn")
        else:
            messagebox.showwarning("Invalid Move", "That spot is already taken!")

    def ai_vs_ai_turn(self):
        if self.game_mode != "AI vs AI":
            return
        self.make_computer_move()
        if not self.check_game_over():
            self.root.after(500, self.ai_vs_ai_turn)

    def make_computer_move(self):
        self.ai_move(self.current_player)
        if self.check_game_over():
            return
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        self.status_label.config(text=f"{self.current_player}'s turn (AI)")

    import random

    def ai_move(self, player, depth=3):
        best_score = float('-inf')
        best_moves = []
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == EMPTY:
                    # Simulate the move
                    self.board[i][j] = player
                    score = self.minimax(self.board, depth - 1, float('-inf'), float('inf'), False, player)
                    self.board[i][j] = EMPTY
                    
                    if score > best_score:
                        best_score = score
                        best_moves = [(i, j)]
                    elif score == best_score:
                        best_moves.append((i, j))

        # Randomly choose among the best moves
        if best_moves:
            best_move = random.choice(best_moves)
            i, j = best_move
            self.board[i][j] = player
            self.buttons[i][j].config(text=player)


    def minimax(self, board, depth, alpha, beta, maximizing, player):
        winner = self.check_winner()
        if winner or depth == 0:
            return self.evaluate_board(player)
        
        opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
        if maximizing:
            max_eval = float('-inf')
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == EMPTY:
                        board[i][j] = player
                        eval = self.minimax(board, depth - 1, alpha, beta, False, player)
                        board[i][j] = EMPTY
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == EMPTY:
                        board[i][j] = opponent
                        eval = self.minimax(board, depth - 1, alpha, beta, True, player)
                        board[i][j] = EMPTY
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval
    
    def evaluate_board(self, player):
        winner = self.check_winner()
        if winner == player:
            return 10
        elif winner == (PLAYER_X if player == PLAYER_O else PLAYER_O):
            return -10
        return 0
    
    def check_winner(self):
        # Check rows, columns, and diagonals
        for row in self.board:
            if row[0] != EMPTY and all(cell == row[0] for cell in row):
                return row[0]
        
        for col in range(self.board_size):
            if self.board[0][col] != EMPTY and all(self.board[row][col] == self.board[0][col] for row in range(self.board_size)):
                return self.board[0][col]
        
        if self.board[0][0] != EMPTY and all(self.board[i][i] == self.board[0][0] for i in range(self.board_size)):
            return self.board[0][0]
        if self.board[0][self.board_size - 1] != EMPTY and all(self.board[i][self.board_size - i - 1] == self.board[0][self.board_size - 1] for i in range(self.board_size)):
            return self.board[0][self.board_size - 1]
        
        # Check for draw
        if all(cell != EMPTY for row in self.board for cell in row):
            return "Draw"
        
        return None

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            if winner == "Draw":
                messagebox.showinfo("Game Over", "It's a draw!")
            else:
                messagebox.showinfo("Game Over", f"{winner} wins!")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.board = [[EMPTY] * self.board_size for _ in range(self.board_size)]
        self.current_player = random.choice([PLAYER_X, PLAYER_O])
        self.first_player = self.current_player
        for row_buttons in self.buttons:
            for btn in row_buttons:
                btn.config(text=EMPTY)
        self.status_label.config(text="Choose a game mode")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
