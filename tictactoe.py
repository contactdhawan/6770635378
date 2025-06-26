import tkinter as tk
from tkinter import simpledialog, messagebox
import random, os, json, time

try:
    import winsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

LEADERBOARD_FILE = "leaderboard.json"

class UltimateTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic Tac Toe")
        self.mode = "PvP"  # PvP or PvC
        self.theme = "light"
        self.winning_score = 3
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.last_moves = []
        self.current_player = "X"
        self.player_names = {"X": "Player X", "O": "Player O"}

        self.setup_menu()
        self.setup_ui()

        self.ask_game_mode()
        self.ask_player_names()
        self.ask_tournament_goal()
        self.update_ui()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light Mode", command=lambda: self.set_theme("light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.set_theme("dark"))
        menubar.add_cascade(label="Theme", menu=theme_menu)
        menubar.add_command(label="Replay", command=self.replay_last)
        menubar.add_command(label="Leaderboard", command=self.show_leaderboard)
        self.root.config(menu=menubar)

    def setup_ui(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                b = tk.Button(self.root, text="", font=("Helvetica", 32), width=5, height=2,
                              command=lambda row=r, col=c: self.make_move(row, col))
                b.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = b

        self.status = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.status.grid(row=3, column=0, columnspan=3, pady=10)

    def ask_game_mode(self):
        mode = simpledialog.askstring("Game Mode", "Type '1' for Single Player, '2' for Two Player:")
        if mode == "1":
            self.mode = "PvC"
            self.player_names["O"] = "CPU"
        else:
            self.mode = "PvP"

    def ask_player_names(self):
        self.player_names["X"] = simpledialog.askstring("Player X", "Enter name for Player X:") or "Player X"
        if self.mode == "PvP":
            self.player_names["O"] = simpledialog.askstring("Player O", "Enter name for Player O:") or "Player O"

    def ask_tournament_goal(self):
        goal = simpledialog.askinteger("Tournament Goal", "First to how many points wins?", minvalue=1, maxvalue=20)
        self.winning_score = goal or 3

    def make_move(self, row, col):
        if self.buttons[row][col]["text"] or self.check_winner() or self.is_tie():
            return

        self.set_cell(row, col, self.current_player)
        self.last_moves.append((row, col, self.current_player))
        self.play_sound("click")

        if self.check_winner():
            winner = self.current_player
            self.scores[winner] += 1
            self.play_sound("win")
            self.update_ui()
            if self.scores[winner] >= self.winning_score:
                self.end_tournament(winner)
            else:
                messagebox.showinfo("Round Over", f"{self.player_names[winner]} wins this round!")
                self.reset_board()
            return
        elif self.is_tie():
            self.scores["draws"] += 1
            self.play_sound("draw")
            self.update_ui()
            messagebox.showinfo("Round Over", "It's a draw!")
            self.reset_board()
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_ui()

        if self.mode == "PvC" and self.current_player == "O":
            self.root.after(400, self.computer_move)

    def computer_move(self):
        move = self.best_move() if self.winning_score > 1 else self.random_move()
        if move:
            self.make_move(*move)

    def best_move(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "O"
                    if self.check_winner():
                        self.board[r][c] = ""
                        return (r, c)
                    self.board[r][c] = ""
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "X"
                    if self.check_winner():
                        self.board[r][c] = ""
                        return (r, c)
                    self.board[r][c] = ""
        return self.random_move()

    def random_move(self):
        options = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        return random.choice(options) if options else None

    def set_cell(self, r, c, symbol):
        self.board[r][c] = symbol
        self.buttons[r][c].config(text=symbol, disabledforeground="#000" if self.theme == "light" else "#fff")
        self.buttons[r][c].config(state="disabled")

    def update_ui(self):
        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                self.buttons[r][c].config(
                    bg="#ffffff" if self.theme == "light" else "#333333",
                    fg="#000000" if self.theme == "light" else "#ffffff"
                )
                if cell:
                    self.buttons[r][c].config(text=cell, state="disabled")
                else:
                    self.buttons[r][c].config(text="", state="normal")

        self.status.config(text=(
            f"{self.player_names['X']} (X): {self.scores['X']}  |  "
            f"{self.player_names['O']} (O): {self.scores['O']}  |  "
            f"Draws: {self.scores['draws']}  |  First to {self.winning_score} wins"
        ))

    def check_winner(self):
        b = self.board
        lines = [b[i] for i in range(3)] + [[b[r][i] for r in range(3)] for i in range(3)] + \
                [[b[i][i] for i in range(3)], [b[i][2 - i] for i in range(3)]]
        return [line[0] for line in lines if line[0] != "" and all(cell == line[0] for cell in line)]

    def is_tie(self):
        return all(cell != "" for row in self.board for cell in row) and not self.check_winner()

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.last_moves.clear()
        self.update_ui()

    def end_tournament(self, winner):
        name = self.player_names[winner]
        messagebox.showinfo("🏆 Tournament Winner", f"{name} wins the tournament!")
        self.save_leaderboard(name)
        self.reset_game()

    def reset_game(self):
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.reset_board()
        self.ask_tournament_goal()
        self.update_ui()

    def set_theme(self, theme):
        self.theme = theme
        self.root.configure(bg="#eeeeee" if theme == "light" else "#222222")
        self.status.configure(bg=self.root["bg"], fg="#000000" if theme == "light" else "#ffffff")
        self.update_ui()

    def replay_last(self):
        self.reset_board()
        for r, c, sym in self.last_moves:
            self.set_cell(r, c, sym)

    def show_leaderboard(self):
        if not os.path.exists(LEADERBOARD_FILE):
            messagebox.showinfo("Leaderboard", "No tournament winners yet.")
            return
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
        board = "\n".join(f"{i+1}. {name} - {score} wins" for i, (name, score) in enumerate(data))
        messagebox.showinfo("🏅 Leaderboard", board)

    def save_leaderboard(self, winner_name):
        data = {}
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
        data[winner_name] = data.get(winner_name, 0) + 1
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(dict(sorted_data), f, indent=2)

    def play_sound(self, event):
        if not SOUND_ENABLED:
            return
        try:
            if event == "click":
                winsound.Beep(400, 100)
            elif event == "win":
                winsound.Beep(800, 300)
            elif event == "draw":
                winsound.Beep(300, 300)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTicTacToe(root)
    root.mainloop()
