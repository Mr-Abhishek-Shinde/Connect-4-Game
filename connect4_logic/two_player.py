import pygame
import numpy as np
import math
from threading import Timer


ROWS = 6
COLS = 7

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SQUARESIZE = 100
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)

size = (width, height)

# pygame.init()
# screen = pygame.display.set_mode(size)
# my_font = pygame.font.SysFont("monospace", 75)

class Connect4Game:
    def __init__(self):
        self.board = self.create_board()
        self.game_over = False
        self.not_over = True
        self.turn = 0

    def create_board(self):
        board = np.zeros((ROWS, COLS))
        return board

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        # Checking horizontal locations for win
        for c in range(COLS-3):
            for r in range(ROWS):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Checking vertical locations for win
        for c in range(COLS):
            for r in range(ROWS-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Checking positively sloped diagonals for win
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

        # Checking negatively sloped diagonals for win
        for c in range(3, COLS):
            for r in range(3, ROWS):
                if self.board[r][c] == piece and self.board[r-1][c-1] == piece and self.board[r-2][c-2] == piece and self.board[r-3][c-3] == piece:
                    return True

        return False

    def end_game(self):
        self.game_over = True
        print("Game Over")

def draw_board(game):
    board = game.board
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else:
                pygame.draw.circle(screen, GREEN, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()

def run_pygame_ui(game):
    draw_board(game)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION and game.not_over:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                xpos = pygame.mouse.get_pos()[0]

                if game.turn == 0:
                    pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius)
                else:
                    pygame.draw.circle(screen, GREEN, (xpos, int(SQUARESIZE/2)), circle_radius)

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and game.not_over:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                xpos = event.pos[0]

                # ask for player input
                col = int(math.floor(xpos/SQUARESIZE))

                if game.is_valid_location(col):
                    row = game.get_next_open_row(col)
                    game.drop_piece(row, col, game.turn + 1)

                    if game.winning_move(game.turn + 1):
                        print(f"PLAYER {game.turn + 1} WON!")
                        label = my_font.render(f"PLAYER {game.turn + 1} WON!", 1, BLACK if game.turn == 0 else BLACK)
                        screen.blit(label, (40, 10))
                        game.not_over = False
                        t = Timer(3.0, game.end_game)
                        t.start()

                    draw_board(game)

                    game.turn = 1 - game.turn

    game.end_game()
    pygame.quit()
    quit()

def start_human_vs_human_game(scr, fnt):
    global screen, my_font
    screen = scr
    my_font = fnt

    game = Connect4Game()
    run_pygame_ui(game)

