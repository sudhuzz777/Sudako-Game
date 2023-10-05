import random
import tkinter as tk

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def is_valid_move(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    num_to_remove = random.randint(30, 45)  # Adjust the range as desired
    
    for _ in range(num_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
    
    return board

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = generate_sudoku_board()
        self.create_board()

    def create_board(self):
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                if self.board[i][j] == 0:
                    entry = tk.Entry(self.root, width=3)
                else:
                    entry = tk.Label(self.root, text=str(self.board[i][j]), width=3)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            self.entries.append(row_entries)

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4)

    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    value = self.entries[i][j].get()
                    if value.isdigit() and 1 <= int(value) <= 9:
                        self.board[i][j] = int(value)
                    else:
                        return

        if solve_sudoku(self.board):
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].config(text=str(self.board[i][j]))
        else:
            tk.messagebox.showinfo("Invalid Sudoku", "This Sudoku has no solution.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
