import pygame
import random
import copy

def get_number_color(board, player_board, row, col):
    num = player_board[row][col]
    if num == 0:
        return None

    # check if placement is valid
    valid = True
    # check row
    for c in range(9):
        if c != col and (board[row][c] == num or player_board[row][c] == num):
            valid = False
    # check col
    for r in range(9):
        if r != row and (board[r][col] == num or player_board[r][col] == num):
            valid = False
    # check 3x3 box
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if (r != row or c != col) and (board[r][c] == num or player_board[r][c] == num):
                valid = False

    if not valid:
        return "red"

    # check if row is complete and correct
    row_nums = [board[row][c] if board[row][c] != 0 else player_board[row][c] for c in range(9)]
    if sorted(row_nums) == list(range(1, 10)):
        return "green"

    # check if col is complete and correct
    col_nums = [board[r][col] if board[r][col] != 0 else player_board[r][col] for r in range(9)]
    if sorted(col_nums) == list(range(1, 10)):
        return "green"

    # check if 3x3 box is complete and correct
    box_nums = []
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            box_nums.append(board[r][c] if board[r][c] != 0 else player_board[r][c])
    if sorted(box_nums) == list(range(1, 10)):
        return "green"

    return "blue"

def draw_grid(screen):
    for i in range(9):
        if i == 0 or i == 3 or i == 6 or i == 9:
            pygame.draw.line(screen, "black", (i * 64, 0), (i * 64, 576))
        else:
            pygame.draw.line(screen,"grey", (i*64,0), (i*64,576))

    for i in range(9):
        if i == 0 or i == 3 or i == 6 or i == 9:
            pygame.draw.line(screen, "black", (0, i * 64), (576, i * 64))
        else:
            pygame.draw.line(screen, "grey", (0,i*64), (576, i*64))
#////////////////
def draw_board(screen, board, player_board, font):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            player_num = player_board[row][col]
            if num != 0:  # pre-filled, always black
                text = font.render(str(num), True, "black")
                screen.blit(text, (col * 64 + 20, row * 64 + 12))
            elif player_num != 0:
                color = get_number_color(board, player_board, row, col)
                text = font.render(str(player_num), True, color)
                screen.blit(text, (col * 64 + 20, row * 64 + 12))
#///////////////
def is_valid(board, row, col, num):
    # check row
    if num in board[row]:
        return False
    # check column
    if num in [board[r][col] for r in range(9)]:
        return False
    # check 3x3 box
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if board[r][c] == num:
                return False
    return True




def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def fill_board(board):
    nums = list(range(1, 10))
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_solved_board():
    board = [[0] * 9 for _ in range(9)]
    fill_board(board)
    return board



def generate_puzzle(difficulty):
    board = generate_solved_board()

    if difficulty == "easy":
        removals = 35
    elif difficulty == "medium":
        removals = 45
    else:
        removals = 55

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    removed = 0
    for row, col in cells:
        if removed >= removals:
            break
        backup = board[row][col]
        board[row][col] = 0
        test = copy.deepcopy(board)
        if solve(test):
            removed += 1
        else:
            board[row][col] = backup  # put it back if unsolvable

    return board

def check_win(board, player_board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                if player_board[row][col] == 0:
                    return False
                if get_number_color(board, player_board, row, col) != "green" and get_number_color(board, player_board, row, col) != "blue":
                    return False
    # check all rows, cols, boxes are complete
    for i in range(9):
        row_nums = [board[i][c] if board[i][c] != 0 else player_board[i][c] for c in range(9)]
        col_nums = [board[r][i] if board[r][i] != 0 else player_board[r][i] for r in range(9)]
        if sorted(row_nums) != list(range(1, 10)):
            return False
        if sorted(col_nums) != list(range(1, 10)):
            return False
    for box_r in range(0, 9, 3):
        for box_c in range(0, 9, 3):
            box_nums = []
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    box_nums.append(board[r][c] if board[r][c] != 0 else player_board[r][c])
            if sorted(box_nums) != list(range(1, 10)):
                return False
    return True

#/////////////
def main():
    try:
        pygame.init()
        #////////////////
        font = pygame.font.SysFont("Arial", 40)



        #/////////////////
        screen = pygame.display.set_mode((576, 576))
        clock = pygame.time.Clock()
        running = True
        test_block = pygame.image.load("test_block.png")
        sudoku_start  = pygame.image.load("sudoku_start.png")
        sudoku_win = pygame.image.load("sudoku_win.png")
        sudoku_lose = pygame.image.load("sudoku_lose.png")
        select23 = (0,0)
        mode = 0
        screenSet = (0,0)
        completed = False # win or lose
        while running: #start screen
            easyButton = [.6,.7,.8,.9,1.0,1,1.1,1.2,1.3,1.4,1.5,1.6]
            mediumButton = [1.8,1.9,2,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8]
            hardButton = [3.0,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.0]
            screen.fill("white")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 8 == round(event.pos[1] / 64) and round(event.pos[0] / 128,1) in easyButton:  #.6 1.6
                        mode = "easy"
                        print(mode)  #remove me once done
                        running = False
                        # use to set the select position of the start buttons recode
                        # the numbers to set the area of each button
                    elif  8 == round(event.pos[1] / 64) and round(event.pos[0] / 128,1) in mediumButton: # 1.8 2.8
                        mode = "medium"
                        print(mode)  #remove me once done
                        running = False
                    elif 8 == round(event.pos[1] / 64) and round(event.pos[0] / 128,1) in hardButton: # 3 4
                        mode = "hard"
                        print(mode)  #remove me once done
                        running = False
            screen.blit(
                sudoku_start,
                sudoku_start.get_rect(topleft=(screenSet[0] * 64, screenSet[1] * 64))
            )
            pygame.display.flip()
            clock.tick(60)
        running = True
        board = generate_puzzle(mode)
        player_board = [[0] * 9 for _ in range(9)]


        while running: #game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    select23 = (event.pos[0] // 64, event.pos[1] // 64)
                elif event.type == pygame.KEYDOWN:
                    col, row = select23
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        num = event.key - pygame.K_0
                        if board[row][col] == 0:  # don't overwrite pre-filled cells
                            player_board[row][col] = num
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        if board[row][col] == 0:  # only erase player-placed numbers
                            player_board[row][col] = 0
                    test_block = pygame.image.load("test_block.png")
            if check_win(board, player_board):
                completed = True
                running = False
            screen.fill("white")
            draw_grid(screen)
            draw_board(screen, board, player_board, font)
            screen.blit(
                test_block,
                test_block.get_rect(topleft=(select23[0]*64,select23[1]*64))
            )
            pygame.display.flip()
            clock.tick(60)

        running = True
        if completed == False: ## game lose // 45 8   354 // 116 3

            while running:
                hightLose = [ 1]
                for event in pygame.event.get():  #lose and restart
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if 3 == round(event.pos[1] / 128) and round(event.pos[0] / 250) == 1:
                            main()
                            running = False
                screen.blit(
                    sudoku_lose,
                    sudoku_lose.get_rect(topleft=(screenSet[0] * 64, screenSet[1] * 64))
                )
                pygame.display.flip()
                clock.tick(60)

        elif completed == True: # game win
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if 3 == round(event.pos[1] / 128) and round(event.pos[0] / 250) == 1:
                            print("you win!!!") #remove me once done
                            running = False
                screen.blit(
                    sudoku_win,
                    sudoku_win.get_rect(topleft=(screenSet[0] * 64, screenSet[1] * 64))
                )
                pygame.display.flip()
                clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
