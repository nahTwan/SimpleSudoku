import pygame
import sys
from sudoku_generator import generate_sudoku



#LUCAS AND SALIM REVAMPED CODE
#Changed the following -
#BUG FIXES
#POLISHED FUNCTIONS
#COMPLETE REDO ON FORMATTING
#MADE IT SMOOTHER AND TOOK ALL TEMPS AWAY
#REWROTE TO FIT ASSIGNMENT NEEDS/ASKS
#BEFORE OUR CODE DID NOT WORK AS INTENDED
#BASICALLY FLESHED ENTIRE CODE OUT and made it working



SCREEN_W = 576
SCREEN_H = 704
CELL = 64
SIZE = 9

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (30, 100, 200)
LIGHT_BLUE = (200, 220, 255)
BG = (255, 255, 255)


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.original = value != 0
    def set_value(self, val):
        self.value = val
    def set_sketch(self, val):
        self.sketched = val
    def draw(self):
        x = self.col * CELL
        y = self.row * CELL
        if self.selected:
            pygame.draw.rect(self.screen, LIGHT_BLUE, (x, y, CELL, CELL))
        big_font = pygame.font.SysFont("Arial", 40)
        small_font = pygame.font.SysFont("Arial", 20)
        if self.value != 0:
            color = BLACK if self.original else BLUE
            txt = big_font.render(str(self.value), True, color)
            self.screen.blit(txt, txt.get_rect(center=(x + CELL // 2, y + CELL // 2)))
        elif self.sketched != 0:
            txt = small_font.render(str(self.sketched), True, GRAY)
            self.screen.blit(txt, (x + 5, y + 5))








class Board:
    DIFF_MAP = {"easy": 30, "medium": 40, "hard": 50}
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        removed = self.DIFF_MAP[difficulty]
        puzzle, self.solution = generate_sudoku(SIZE, removed)
        self.og_board = [row[:] for row in puzzle]
        self.cells = []
        for r in range(SIZE):
            row = []
            for c in range(SIZE):
                row.append(Cell(puzzle[r][c], r, c, screen))
            self.cells.append(row)
        self.selected = None
    def draw(self):
        for r in range(SIZE):
            for c in range(SIZE):
                self.cells[r][c].draw()
        for i in range(SIZE + 1):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            if i % 3 == 0:

                color = BLACK
            else:


                color = GRAY
            pygame.draw.line(self.screen, color, (0, i * CELL), (SCREEN_W, i * CELL), thick)
            pygame.draw.line(self.screen, color, (i * CELL, 0), (i * CELL, SIZE * CELL), thick)
    def select(self, row, col):
        if self.selected:
            pr, pc = self.selected
            self.cells[pr][pc].selected = False
        self.selected = (row, col)
        self.cells[row][col].selected = True
    def click(self, x, y):
        if 0 <= x < SCREEN_W and 0 <= y < SIZE * CELL:
            return y // CELL, x // CELL
        return None
    def clear(self):
        if self.selected:
            r, c = self.selected
            if not self.cells[r][c].original:
                self.cells[r][c].set_value(0)
                self.cells[r][c].set_sketch(0)


    def sketch(self, val):
        if self.selected:
            r, c = self.selected
            if not self.cells[r][c].original:
                self.cells[r][c].set_sketch(val)
    def place_number(self, val):
        if self.selected:
            r, c = self.selected
            if not self.cells[r][c].original:
                self.cells[r][c].set_value(val)
                self.cells[r][c].set_sketch(0)
    def reset(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if not self.cells[r][c].original:
                    self.cells[r][c].set_value(0)
                    self.cells[r][c].set_sketch(0)
    def is_full(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r][c].value == 0:
                    return False
        return True




    def update_board(self):
        self.underlying = []
        for r in range(SIZE):
            row = []
            for c in range(SIZE):
                row.append(self.cells[r][c].value)
            self.underlying.append(row)
    def find_empty(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r][c].value == 0:


                    return r, c
        return None
    def check_board(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r][c].value != self.solution[r][c]:
                    return False
        return True
def main():
    try:
        #Set everything ever
        #this looks evil but i dont think it can get cleaned up at all
        pygame.init()
        #font is unused?
        font = pygame.font.SysFont("Arial", 40)
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Sudoku")
        buttons = [1,1]
        sudoku_reset = pygame.image.load("sudoku_reset.png")
        sudoku_restart = pygame.image.load("sudoku_restart.png")
        sudoku_exit = pygame.image.load("sudoku_exit.png")
        screen.blit(sudoku_reset, sudoku_reset.get_rect(topleft=(buttons[0] * 64, buttons[1] * 2 * 64)))
        screen.blit(sudoku_restart, sudoku_restart.get_rect(topleft=(buttons[0] * 64, buttons[1] * 9 * 64)))
        screen.blit(sudoku_exit, sudoku_exit.get_rect(topleft=(buttons[0] * 64, buttons[1] * 9 * 64)))
        clock = pygame.time.Clock()
        running = True
        sudoku_start = pygame.image.load("sudoku_start.png")
        sudoku_win = pygame.image.load("sudoku_win.png")
        sudoku_lose = pygame.image.load("sudoku_lose.png")
        x = 0
        y = 0
        #what is this variable?????????
        #unused so its okay its just getting left alone
        select23 = (x, y)
        mode = 0
        #i think screenSet is select23? possibly
        screenSet = (0, 0)
        completed = False

        while running:  # games start screen
            easyButton = [.6,.7,.8,.9,1.0,1,1.1,1.2,1.3,1.4,1.5,1.6]
            mediumButton = [1.8,1.9,2,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8]
            hardButton = [3.0,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.0]
            screen.fill(BG)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 8 == round(event.pos[1] / 64) and round(event.pos[0] / 128, 1) in easyButton:
                        mode = "easy"
                        print(mode)
                        running = False
                    elif 8 == round(event.pos[1] / 64) and round(event.pos[0] / 128, 1) in mediumButton:
                        mode = "medium"
                        print(mode)
                        running = False
                    elif 8 == round(event.pos[1] / 64) and round(event.pos[0] / 128, 1) in hardButton:
                        mode = "hard"
                        print(mode)
                        running = False
            screen.blit(sudoku_start, sudoku_start.get_rect(topleft=(screenSet[0] * 64, screenSet[1] * 64)))
            screen.blit(sudoku_reset, sudoku_reset.get_rect(topleft=(0, buttons[1] * 9 * 64)))
            screen.blit(sudoku_restart, sudoku_restart.get_rect(topleft=(192, buttons[1] * 9 * 64)))
            screen.blit(sudoku_exit, sudoku_exit.get_rect(topleft=(384, buttons[1] * 9 * 64)))
            pygame.display.flip()
            clock.tick(60)

        running = True
        board = Board(SCREEN_W, SCREEN_H, screen, mode)

        while running:  # game

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #these are unused
                    (x,y) = (event.pos[0] // 64, event.pos[1] // 64)
                    select23 = (event.pos[0] // 64, event.pos[1] // 64)

                    # reset button logic
                    if 0 <= event.pos[0] <= 192 and 576 <= event.pos[1] <= 704:
                        board.reset()

                    # restart button logic
                    if 192 <= event.pos[0] <= 384 and 576 <= event.pos[1] <= 704:
                        main()
                        running = False

                    # exit button logic
                    if (384 <= event.pos[0] <= 576) and (576 <= event.pos[1] <= 704):
                        pygame.quit()
                        sys.exit()

                    # select cell on gamesboard
                    if event.pos[1] < SIZE * CELL:
                        result = board.click(event.pos[0], event.pos[1])
                        if result:
                            board.select(result[0], result[1])

                elif event.type == pygame.KEYDOWN:
                    if board.selected:
                        r, c = board.selected
                        if event.key in range(pygame.K_1, pygame.K_9 + 1):
                            board.sketch(event.key - pygame.K_0)
                        elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                            board.clear()
                        elif event.key == pygame.K_RETURN:
                            sv = board.cells[r][c].sketched
                            if sv != 0:
                                board.place_number(sv)

                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT]:
                            if c > 0:
                                board.select(r, c - 1)
                        if keys[pygame.K_RIGHT]:
                            if c < SIZE - 1:
                                board.select(r, c + 1)
                        if keys[pygame.K_UP]:
                            if r > 0:
                                board.select(r - 1, c)
                        if keys[pygame.K_DOWN]:
                            if r < SIZE - 1:
                                board.select(r + 1, c)

            if board.is_full():
                if board.check_board():
                    completed = True
                running = not board.is_full()

            screen.fill(BG)
            board.draw()
            screen.blit(sudoku_reset, sudoku_reset.get_rect(topleft=(0, buttons[1] * 9 * 64)))
            screen.blit(sudoku_restart, sudoku_restart.get_rect(topleft=(192, buttons[1] * 9 * 64)))
            screen.blit(sudoku_exit, sudoku_exit.get_rect(topleft=(384, buttons[1] * 9 * 64)))
            pygame.display.flip()
            clock.tick(60)

        running = True
        if not completed:  # losing screen
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if 3 == round(event.pos[1] / 128) and round(event.pos[0] / 250) == 1:
                            main()
                            running = False
                screen.blit(sudoku_lose, sudoku_lose.get_rect(topleft=(screenSet[0] * 64, screenSet[1] * 64)))
                pygame.display.flip()
                clock.tick(60)

        elif completed:  # winning screen
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if 3 == round(event.pos[1] / 128) and round(event.pos[0] / 250) == 1:
                            print("you win!!!")
                            running = False
                screen.blit(sudoku_win, sudoku_win.get_rect(topleft=(screenSet[0] * 64, screenSet[1] * 64)))
                pygame.display.flip()
                clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
