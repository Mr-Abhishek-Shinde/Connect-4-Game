import numpy as np
import pygame
import sys
import math
from threading import Timer
import random


ROWS = 6
COLS = 7

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


PLAYER_TURN = 0
AI_TURN = 1

PLAYER_PIECE = 1
AI_PIECE = 2


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

    def get_valid_locations(self):
        valid_locations = []
        
        for column in range(COLS):
            if self.is_valid_location(column):
                valid_locations.append(column)

        return valid_locations


def draw_board(game):
    board = game.board
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, GREEN, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()





def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE

    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 

    return score    





def score_position(game, piece):
    board = game.board

    score = 0

    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(game):
    return game.winning_move(PLAYER_PIECE) or game.winning_move(AI_PIECE) or len(game.get_valid_locations()) == 0


def minimax(game, depth, maximizing_player):
    board = game.board
    valid_locations = game.get_valid_locations()
    is_terminal = is_terminal_node(game)

    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winning_move(AI_PIECE):
                return (None, 10000000)
            elif game.winning_move(PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(game, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = game.get_next_open_row(col)
            game_copy = Connect4Game()
            game_copy.board = np.copy(game.board)
            game_copy.drop_piece(row, col, AI_PIECE)

            new_score = minimax(game_copy, depth-1, False)[1]

            if new_score > value:
                value = new_score
                column = col

        return column, value
    
    else:
        value = math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = game.get_next_open_row(col)
            game_copy = Connect4Game()
            game_copy.board = np.copy(game.board)
            game_copy.drop_piece(row, col, PLAYER_PIECE)

            new_score = minimax(game_copy, depth-1, True)[1]

            if new_score < value:
                value = new_score
                column = col

        return column, value



def run_pygame_ui(game):
    draw_board(game)

    game_over = False
    not_over = True

    game.turn = random.randint(PLAYER_TURN, AI_TURN)

    while not game_over:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION and not_over:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                xpos = pygame.mouse.get_pos()[0]
                if game.turn == PLAYER_TURN:
                    pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius )

            if event.type == pygame.MOUSEBUTTONDOWN and not_over:
                pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))

                if game.turn == PLAYER_TURN:

                    xpos = event.pos[0] 
                    col = int(math.floor(xpos/SQUARESIZE)) 

                    if game.is_valid_location(col):
                        row = game.get_next_open_row(col)
                        game.drop_piece(row, col, PLAYER_PIECE)
                        if game.winning_move(PLAYER_PIECE):
                            print("YOU WON!")
                            label = my_font.render("YOU WON!", 1, BLACK)
                            screen.blit(label, (40, 10))
                            not_over = False
                            t = Timer(3.0, game.end_game)
                            t.start()
                    
                    draw_board(game) 

                    game.turn = 1 - game.turn


            pygame.display.update()

                        
        if game.turn == AI_TURN and not game_over and not_over:

            col, minimax_score = minimax(game, 5, True)

            if game.is_valid_location(col):
                pygame.time.wait(500)
                row = game.get_next_open_row(col)
                game.drop_piece(row, col, AI_PIECE)
                if game.winning_move(AI_PIECE):
                    print("AI WON!")
                    label = my_font.render("AI WON!", 1, BLACK)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, game.end_game)
                    t.start()
            draw_board(game)    

            game.turn = 1 - game.turn


    game.end_game()
    pygame.quit()
    quit()



def start_mini_max_game(scr, fnt):
    global screen, my_font
    screen = scr
    my_font = fnt

    game = Connect4Game()
    run_pygame_ui(game)
