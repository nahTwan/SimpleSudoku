import random


class SudokuGenerator:

    # Sets up board
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = 3
        self.board = [[0] * row_length for _ in range(row_length)]

    # Returns board
    def get_board(self):
        return self.board

    # Prints board
    def print_board(self):
        for row in self.board:
            print(row)

    # Checks row
    def valid_in_row(self, row, num):
        return num not in self.board[row]

    # Checks column
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    # Checks 3x3 box
    def valid_in_box(self, row_start, col_start, num):
        for r in range(row_start, row_start + self.box_length):
            for c in range(col_start, col_start + self.box_length):
                if self.board[r][c] == num:
                    return False
        return True

    # Checks if move valid
    def is_valid(self, row, col, num):
        row_start = (row // self.box_length) * self.box_length
        col_start = (col // self.box_length) * self.box_length
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row_start, col_start, num))

    # Fills one box
    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        idx = 0
        for r in range(row_start, row_start + self.box_length):
            for c in range(col_start, col_start + self.box_length):
                self.board[r][c] = nums[idx]
                idx += 1

    # Fills diagonal boxes
    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    # Fills remaining cells
    def fill_remaining(self, row=0, col=0):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == (row // self.box_length) * self.box_length:
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    # Builds solution
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    # Removes cells
    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1


# Generates puzzle
def generate_sudoku(size, removed):
    gen = SudokuGenerator(size, removed)
    gen.fill_values()
    solution = [row[:] for row in gen.get_board()]
    gen.remove_cells()
    return gen.get_board(), solution
