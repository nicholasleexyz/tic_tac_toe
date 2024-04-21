import pygame
import sys


square_size: int = 400
resolution: tuple[int, int] = (square_size * 3, square_size * 3)

background_color = (0, 0, 0)
foreground_color = (127, 127, 127)


# pygame setup
pygame.init()

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
running = True

squares: list[pygame.Rect] = []

for y in range(3):
    for x in range(3):
        _x = x * square_size
        _y = y * square_size
        _rect = pygame.Rect(_x, _y, square_size, square_size)
        squares.append(_rect)

win_conditions: list[list[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

x_moves: list[int] = []
o_moves: list[int] = []

game_over: bool = False
is_x_turn: bool = False

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_over:
                for i, _square in enumerate(squares):
                    mouse_pos = pygame.mouse.get_pos()
                    if _square.collidepoint(mouse_pos):
                        print(f"Collided at: {i}")

                        if is_x_turn:
                            x_moves.append(i)
                            print(f"x's turn: {x_moves}")
                        else:
                            o_moves.append(i)
                            print(f"o's turn: {o_moves}")

                        for cond in win_conditions:
                            if is_x_turn:
                                if set(cond) <= set(x_moves):
                                    print("X WINS!")
                                    game_over = True
                                    break
                            else:
                                if set(cond) <= set(o_moves):
                                    print("O WINS!")
                                    game_over = True
                                    break

                        move_count = len(x_moves) + len(o_moves)
                        if move_count == 9 and not game_over:
                            print("DRAW!")
                            game_over = True

                        is_x_turn = not is_x_turn
            else:
                print("Restarting game!")
                is_x_turn = False
                x_moves = []
                o_moves = []
                game_over = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(foreground_color)

    # RENDER GAME HERE
    for i, square in enumerate(squares):
        col = background_color

        if i in x_moves:
            col = (0, 127, 127)
            pygame.draw.rect(screen, (0, 0, 0), square)
        elif i in o_moves:
            col = (127, 127, 0)
            pygame.draw.rect(screen, (0, 0, 0), square)

        pygame.draw.rect(screen, col, square, 10)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
