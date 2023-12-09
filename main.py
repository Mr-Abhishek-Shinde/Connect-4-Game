import pygame
from connect4_logic.two_player import start_human_vs_human_game
from connect4_logic.alpha_beta import start_alpha_beta_game

def display_menu(screen):
    font = pygame.font.Font(None, 36)
    text1 = font.render("1. Human vs Human", True, (255, 255, 255))
    text2 = font.render("2. AI vs Human (Mini-Max)", True, (255, 255, 255))
    text3 = font.render("3. AI vs Human (Alpha-Beta Pruning)", True, (255, 255, 255))
    text4 = font.render("4. AI vs Human (Monte Carlo Tree Search)", True, (255, 255, 255))
    text5 = font.render("5. Quit", True, (255, 255, 255))

    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))
    screen.blit(text3, (50, 150))
    screen.blit(text4, (50, 200))
    screen.blit(text5, (50, 250))

def main():
    print("Welcome to Connect 4!")

    ROWS = 6
    COLS = 7
    SQUARESIZE = 100

    width = COLS * SQUARESIZE
    height = (ROWS + 1) * SQUARESIZE
    size = (width, height)

    pygame.init()

    screen = pygame.display.set_mode(size)
    my_font = pygame.font.SysFont("monospace", 75)

    pygame.display.set_caption("Connect 4 Menu")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting the game. Goodbye!")
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 < x < 350:
                    choice = (y - 50) // 50 + 1
                    if 1 <= choice <= 5:
                        if choice == 1:
                            start_human_vs_human_game(screen, my_font)
                        elif choice == 2:
                            start_alpha_beta_game(screen, my_font)
                        elif choice == 3:
                            # ai vs human (alpha beta)
                            pass
                        elif choice == 4:
                            # ai vs human (Monte Carlo Tree Search)
                            pass
                        elif choice == 5:
                            print("Exiting the game. Goodbye!")
                            pygame.quit()
                            return

        screen.fill((0, 0, 0))
        display_menu(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
