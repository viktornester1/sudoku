import random
import copy


def generate_sudoku(difficulty):
    """
    Generates a Sudoku puzzle with the specified difficulty level.
    Returns the initial board and the solution.
    """
    # Generate a solved Sudoku board
    board = [[0 for _ in range(9)] for _ in range(9)]
    solved_board = fill_board(board)
    solution_board = copy.deepcopy(solved_board)

    # Remove cells based on the difficulty level
    if difficulty == 'easy':
        remove_cells(solved_board, 45)
    elif difficulty == 'medium':
        remove_cells(solved_board, 55)
    else:
        remove_cells(solved_board, 65)

    print("SOLVEEEEED:", solution_board)
    return solved_board, solution_board  # Return the initial board and the solution


def fill_board(board):
    """
    Fills the Sudoku board using an iterative backtracking algorithm.
    Returns the solved board.
    """
    row, col = find_unassigned_location(board, 0, 0)
    if row == -1 and col == -1:
        return board  # All cells are filled

    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for num in numbers:
        if is_safe(board, row, col, num):
            board[row][col] = num

            solved_board = fill_board(board)
            if solved_board is not False:
                return solved_board

            board[row][col] = 0

    return False


def find_unassigned_location(board, row, col):
    """
    Find the next unassigned cell.
    """
    for r in range(row, 9):
        for c in range(col if r == row else 0, 9):
            if board[r][c] == 0:
                return r, c
    return -1, -1


def is_safe(board, row, col, num):
    """
    Checks if the given number can be placed in the specified cell.
    """
    # Check the row
    if num in board[row]:
        return False

    # Check the column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    if num in [board[box_row + i][box_col + j] for i in range(3) for j in range(3)]:
        return False

    return True


def remove_cells(board, num_cells):
    """
    Removes the specified number of cells from the Sudoku board.
    """
    cells = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(cells)

    for row, col in cells[:num_cells]:
        board[row][col] = 0
