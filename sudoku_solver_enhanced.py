class Board:
    def __init__(self, board):
        # Validate the input board
        if not self.is_valid_board(board):
            raise ValueError("Invalid board: Must be a 9x9 grid with numbers between 0 and 9")
        self.board = board

    @staticmethod
    def is_valid_board(board):
        """Check if the input board is a valid 9x9 Sudoku grid."""
        if len(board) != 9 or any(len(row) != 9 for row in board):
            return False
        for row in board:
            if any(not (0 <= cell <= 9) for cell in row):
                return False
        return True

    def __str__(self):
        """Create a string representation of the Sudoku board."""
        board_str = ''
        for row in self.board:
            # Replace zeros with '*' for better visualization
            row_str = [str(i) if i else '*' for i in row]
            # Join items in the row with a space and add to board_str
            board_str += ' '.join(row_str) + '\n'
        return board_str

    def find_empty_cell(self):
        """Find the first empty cell (marked as 0). Return its row and column."""
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col
            except ValueError:
                pass
        return None

    def valid_in_row(self, row, num):
        """Check if the number is not present in the given row."""
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        """Check if the number is not present in the given column."""
        return all(self.board[row][col] != num for row in range(9))

    def valid_in_square(self, row, col, num):
        """Check if the number is not present in the 3x3 square."""
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
                if self.board[row_no][col_no] == num:
                    return False
        return True

    def is_valid(self, empty, num):
        """Check if placing a number in the empty cell is valid."""
        row, col = empty
        valid_in_row = self.valid_in_row(row, num)
        valid_in_col = self.valid_in_col(col, num)
        valid_in_square = self.valid_in_square(row, col, num)
        return all([valid_in_row, valid_in_col, valid_in_square])

    def solver(self):
        """Solve the Sudoku puzzle using backtracking."""
        # Find the next empty cell
        if (next_empty := self.find_empty_cell()) is None:
            return True  # Puzzle is solved

        # Unpack the row and column of the empty cell
        row, col = next_empty

        # Try placing numbers 1-9 in the empty cell
        for guess in range(1, 10):
            if self.is_valid((row, col), guess):
                self.board[row][col] = guess  # Tentatively place the number

                if self.solver():
                    return True  # If successful, stop further backtracking

                self.board[row][col] = 0  # Undo the placement (backtrack)

        return False  # Trigger backtracking if no numbers work


def solve_sudoku(board):
    """Solve a Sudoku puzzle and print the results."""
    try:
        gameboard = Board(board)
    except ValueError as e:
        print(e)
        return False, None

    print(f'Puzzle to solve:\n{gameboard}')
    if gameboard.solver():
        print(f'Solved puzzle:\n{gameboard}')
        return True, gameboard.board
    else:
        print('The provided puzzle is unsolvable.')
        return False, None


# Test Cases
if __name__ == "__main__":
    puzzles = [
        # Example puzzle to solve
        [
            [0, 0, 2, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 7, 6, 2],
            [4, 3, 0, 0, 0, 0, 8, 0, 0],
            [0, 5, 0, 0, 3, 0, 0, 9, 0],
            [0, 4, 0, 0, 0, 0, 0, 2, 6],
            [0, 0, 0, 4, 6, 7, 0, 0, 0],
            [0, 8, 6, 7, 0, 4, 0, 0, 0],
            [0, 0, 0, 5, 1, 9, 0, 0, 8],
            [1, 7, 0, 0, 0, 6, 0, 0, 5]
        ],
        # Edge case: Already solved puzzle
        [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ],
        # Edge case: Unsolvable puzzle
        [
            [1, 1, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    ]

    for i, puzzle in enumerate(puzzles, 1):
        print(f"\n--- Solving Puzzle {i} ---")
        solve_sudoku(puzzle)
