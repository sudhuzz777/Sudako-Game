import random

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

def main():
    print("Welcome to Sudoku!")
    sudoku_board = generate_sudoku_board()
    
    while True:
        print("\nCurrent Sudoku board:")
        print_board(sudoku_board)
        
        row = int(input("\nEnter row (1-9, 0 to quit): "))
        if row == 0:
            print("Thanks for playing!")
            break
        
        col = int(input("Enter column (1-9): "))
        num = int(input("Enter a number (1-9): "))
        
        if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9):
            print("Invalid input. Please enter valid values.")
            continue
        
        if is_valid_move(sudoku_board, row - 1, col - 1, num):
            sudoku_board[row - 1][col - 1] = num
        else:
            print("Invalid move. Try again.")

    if solve_sudoku(sudoku_board):
        print("\nCongratulations! You solved the Sudoku!")
        print_board(sudoku_board)
    else:
        print("\nSorry, the Sudoku has no solution. Better luck next time!")

if __name__ == "__main__":
    main()
