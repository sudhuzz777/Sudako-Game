import random
import tkinter as tk
from tkinter import messagebox
import time

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def is_valid_move(board, row, col, num):
    n = len(board)
    root_n = int(n ** 0.5)
    for i in range(n):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = root_n * (row // root_n), root_n * (col // root_n)
    for i in range(root_n):
        for j in range(root_n):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

def solve_sudoku(board):
    n = len(board)
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:
                for num in range(1, n + 1):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku_board(grid_size):
    n = grid_size
    board = [[0 for _ in range(n)] for _ in range(n)]
    solve_sudoku(board)
    num_to_remove = random.randint(n * n // 2, n * n - 1)
    
    for _ in range(num_to_remove):
        row, col = random.randint(0, n - 1), random.randint(0, n - 1)
        while board[row][col] == 0:
            row, col = random.randint(0, n - 1), random.randint(0, n - 1)
        board[row][col] = 0
    
    return board

class SudokuGUI:
    def __init__(self, root, grid_size):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grid_size = grid_size
        self.board = generate_sudoku_board(grid_size)
        self.entries = []
        self.timer_label = tk.Label(root, text="Time: 0 s")
        self.timer_label.grid(row=grid_size, column=0, columnspan=2)
        self.start_time = time.time()
        self.create_board()

    def create_board(self):
        for i in range(self.grid_size):
            row_entries = []
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    entry = tk.Entry(self.root, width=3)
                    entry.bind("<FocusOut>", self.check_entry)
                else:
                    entry = tk.Label(self.root, text=str(self.board[i][j]), width=3)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            self.entries.append(row_entries)

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=self.grid_size, column=3)
        reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        reset_button.grid(row=self.grid_size, column=4)
        self.timer()
        
    def timer(self):
        elapsed_time = round(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time} s")
        self.root.after(1000, self.timer)
        
    def check_entry(self, event):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.entries[i][j] == event.widget:
                    value = event.widget.get()
                    if value.isdigit() and 1 <= int(value) <= self.grid_size:
                        if is_valid_move(self.board, i, j, int(value)):
                            event.widget.config(fg="green")
                        else:
                            event.widget.config(fg="red")
                    else:
                        event.widget.config(fg="black")

    def solve(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    value = self.entries[i][j].get()
                    if value.isdigit() and 1 <= int(value) <= self.grid_size:
                        self.board[i][j] = int(value)

        if solve_sudoku(self.board):
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.entries[i][j].config(text=str(self.board[i][j]), fg="black")
        else:
            messagebox.showinfo("Invalid Sudoku", "This Sudoku has no solution.")
            
    def reset(self):
        self.start_time = time.time()
        self.timer_label.config(text="Time: 0 s")
        self.board = generate_sudoku_board(self.grid_size)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    self.entries[i][j].config(text="", fg="black")
                else:
                    self.entries[i][j].config(text=str(self.board[i][j]), fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    grid_size = int(input("Enter the grid size (6 to 16): "))
    if 6 <= grid_size <= 16:
        app = SudokuGUI(root, grid_size)
        root.mainloop()
    else:
        print("Invalid grid size. Please enter a value between 6 and 16.")
