import pygame
import random
import copy


class Board:
    def __init__(self, difficulty):
        self.board = self._generate_puzzle(difficulty)
        self.player_board = [[0] * 9 for _ in range(9)]

    def _is_valid(self, board, row, col, num):
        if num in board[row]:
            return False
        if num in [board[r][col] for r in range(9)]:
            return False
        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False
        return True

    def _solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self._is_valid(board, row, col, num):
                            board[row][col] = num
                            if self._solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def _fill_board(self, board):
        nums = list(range(1, 10))
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    random.shuffle(nums)
                    for num in nums:
                        if self._is_valid(board, row, col, num):
                            board[row][col] = num
                            if self._fill_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def _generate_solved_board(self):
        board = [[0] * 9 for _ in range(9)]
        self._fill_board(board)
        return board

    def _generate_puzzle(self, difficulty):
        board = self._generate_solved_board()
        removals = {"easy": 30, "medium": 40, "hard": 50}.get(difficulty, 30)

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        removed = 0
        for row, col in cells:
            if removed >= removals:
                break
            backup = board[row][col]
            board[row][col] = 0
            test = copy.deepcopy(board)
            if self._solve(test):
                removed += 1
            else:
                board[row][col] = backup
        return board


    def place(self, row, col, num):
        if self.board[row][col] == 0:
            self.player_board[row][col] = num

    def erase(self, row, col):
        if self.board[row][col] == 0:
            self.player_board[row][col] = 0

    def get_number_color(self, row, col, what = 0):
        what = what
        num = self.player_board[row][col]
        if num == 0:
            return None

        valid = True
        for c in range(9):
            if c != col and (self.board[row][c] == num or self.player_board[row][c] == num):
                valid = False
        for r in range(9):
            if r != row and (self.board[r][col] == num or self.player_board[r][col] == num):
                valid = False
        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        if what == 1:
            return "green"
        return "blue"

    def check_win(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    if self.player_board[row][col] == 0:
                        return False
                    color = self.get_number_color(row, col)
                    if color not in ("green", "blue"):
                        return False
        for i in range(9):
            row_nums = [self.board[i][c] if self.board[i][c] != 0 else self.player_board[i][c] for c in range(9)]
            col_nums = [self.board[r][i] if self.board[r][i] != 0 else self.player_board[r][i] for r in range(9)]
            if sorted(row_nums) != list(range(1, 10)):
                return False
            if sorted(col_nums) != list(range(1, 10)):
                return False
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                box_nums = []
                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):
                        box_nums.append(self.board[r][c] if self.board[r][c] != 0 else self.player_board[r][c])
                if sorted(box_nums) != list(range(1, 10)):
                    return False
        return True


    def draw_grid(self, screen):
        for i in range(9):
            color = "black" if i % 3 == 0 else "grey"
            pygame.draw.line(screen, color, (i * 64, 0), (i * 64, 576))
            pygame.draw.line(screen, color, (0, i * 64), (576, i * 64))

    def draw(self, screen, font):
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                player_num = self.player_board[row][col]
                if num != 0:
                    text = font.render(str(num), True, "black")
                    screen.blit(text, (col * 64 + 20, row * 64 + 12))
                elif player_num != 0:
                    color = self.get_number_color(row, col)
                    text = font.render(str(player_num), True, color)
                    screen.blit(text, (col * 64 + 20, row * 64 + 12))


def main():
    try:
        pygame.init()
        font = pygame.font.SysFont("Arial", 40)
        screen = pygame.display.set_mode((576, 704))
        buttons = [1,1]
        sudoku_reset = pygame.image.load("sudoku_reset.png")
        sudoku_restart = pygame.image.load("sudoku_restart.png")
        sudoku_exit = pygame.image.load("sudoku_exit.png")
        screen.blit(sudoku_reset, sudoku_reset.get_rect(topleft=(buttons[0] * 64, buttons[1] * 2 * 64)))
        screen.blit(sudoku_restart, sudoku_restart.get_rect(topleft=(buttons[0] * 64, buttons[1] * 9 * 64)))
        screen.blit(sudoku_exit, sudoku_exit.get_rect(topleft=(buttons[0] * 64, buttons[1] * 9 * 64)))
        clock = pygame.time.Clock()
        running = True
        test_block = pygame.image.load("test_block.png")
        sudoku_start = pygame.image.load("sudoku_start.png")
        sudoku_win = pygame.image.load("sudoku_win.png")
        sudoku_lose = pygame.image.load("sudoku_lose.png")
        x = 0
        y = 0
        select23 = (x, y)
        mode = 0
        screenSet = (0, 0)
        completed = False

        while running:  # start screen
            easyButton = [.6,.7,.8,.9,1.0,1,1.1,1.2,1.3,1.4,1.5,1.6]
            mediumButton = [1.8,1.9,2,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8]
            hardButton = [3.0,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.0]
            screen.fill("white")
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
        game = Board(mode)

        while running:  # game

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = (event.pos[0] // 64, event.pos[1] // 64)
                    select23 = (event.pos[0] // 64, event.pos[1] // 64)

                    if 192 <= event.pos[0] <= 192+192 and 576 <= event.pos[1] <= 704:
                        main()
                        running = False

                elif event.type == pygame.KEYDOWN:
                    col, row = select23
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        game.place(row, col, event.key - pygame.K_0)
                    elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                        game.erase(row, col)
                    test_block = pygame.image.load("test_block.png")
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        if x >= 0:
                            x -= 1
                            select23 = (x,y)
                    if keys[pygame.K_RIGHT]:
                        if x <= 9:
                            x +=1
                            select23 = (x,y)
                    if keys[pygame.K_UP]:
                        if x <= 9:
                            y -= 1
                            select23 = (x,y)
                    if keys[pygame.K_DOWN]:
                        if x >= 0:
                            y += 1
                            select23 = (x,y)
                    if keys[pygame.K_RETURN]:
                        what = 1
                        Board.get_number_color(row,col,what)
                        what = 0

            if game.check_win():
                completed = True
                running = False
            screen.fill("white")
            game.draw_grid(screen)
            game.draw(screen, font)
            screen.blit(test_block, test_block.get_rect(topleft=(select23[0] * 64, select23[1] * 64)))
            screen.blit(sudoku_reset, sudoku_reset.get_rect(topleft=(0, buttons[1] * 9 * 64)))
            screen.blit(sudoku_restart, sudoku_restart.get_rect(topleft=(192, buttons[1] * 9 * 64)))
            screen.blit(sudoku_exit, sudoku_exit.get_rect(topleft=(384, buttons[1] * 9 * 64)))
            pygame.display.flip()
            clock.tick(60)

        running = True
        if not completed:  # lose screen
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

        elif completed:  # win screen
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
