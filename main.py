import pygame
import sys
from enum import Enum, auto


class WinState(Enum):
    NONE = auto()
    X_WINS = auto()
    O_WINS = auto()
    DRAW = auto()


win_state = WinState.NONE

square_size: int = 400
half_square = square_size // 2

resolution: tuple[int, int] = (square_size * 3, square_size * 3)
text_pos: tuple[int, int] = (600, 600)

background_color = (0, 0, 0)
foreground_color = (127, 127, 127)


# pygame setup
pygame.init()
pygame.font.init()
font_name = "Hack Nerd Font Mono Regular"
font: pygame.font.Font = pygame.font.SysFont(font_name, 128)
font_big: pygame.font.Font = pygame.font.SysFont(font_name, square_size // 2)

x_wins_surface = font.render("X WINS!", True, (255, 255, 255))
o_wins_surface = font.render("O WINS!", True, (255, 255, 255))
draw_surface = font.render("DRAW", True, (255, 255, 255))

x_surface = font_big.render("X", True, (255, 255, 255))
o_surface = font_big.render("O", True, (255, 255, 255))


def center_surface(
        surf: pygame.Surface,
        center: tuple[int, int]
        ) -> tuple[int, int]:
    surf_size = surf.get_size()
    pos_x = center[0] - (surf_size[0] // 2)
    pos_y = center[1] - (surf_size[1] // 2)
    return (pos_x, pos_y)


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
total_moves: list[int] = []

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

                    if (_square.collidepoint(mouse_pos) and
                            i not in total_moves):

                        total_moves.append(i)

                        if is_x_turn:
                            x_moves.append(i)
                        else:
                            o_moves.append(i)

                        for cond in win_conditions:
                            if is_x_turn:
                                if set(cond) <= set(x_moves):
                                    # print("X WINS!")
                                    win_state = WinState.X_WINS
                                    game_over = True
                                    break
                            else:
                                if set(cond) <= set(o_moves):
                                    # print("O WINS!")
                                    win_state = WinState.O_WINS
                                    game_over = True
                                    break

                        move_count = len(x_moves) + len(o_moves)
                        if move_count == 9 and not game_over:
                            # print("DRAW!")
                            win_state = WinState.DRAW
                            game_over = True

                        is_x_turn = not is_x_turn
            else:
                # print("Restarting game!")
                is_x_turn = False
                x_moves = []
                o_moves = []
                total_moves = []
                win_state = win_state.NONE
                game_over = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(foreground_color)

    # RENDER GAME HERE
    for i, square in enumerate(squares):
        col = background_color
        square_center = (square[0] + half_square, square[1] + half_square)
        if not game_over:
            if i in x_moves:
                text_center = center_surface(x_surface, square_center)
                screen.blit(x_surface, text_center)
            elif i in o_moves:
                text_center = center_surface(o_surface, square_center)
                screen.blit(o_surface, text_center)

        if i in x_moves:
            col = (0, 127, 127)
        elif i in o_moves:
            col = (127, 127, 0)

        pygame.draw.rect(screen, col, square, 10)

    screen_center = (resolution[0] // 2, resolution[1] // 2)
    match win_state:
        case WinState.X_WINS:
            center = center_surface(x_wins_surface, screen_center)
            screen.blit(x_wins_surface, center)
        case WinState.O_WINS:
            center = center_surface(o_wins_surface, screen_center)
            screen.blit(o_wins_surface, center)
        case WinState.DRAW:
            center = center_surface(draw_surface, screen_center)
            screen.blit(draw_surface, center)
        case _:
            pass

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
