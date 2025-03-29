import pygame
import random

WHITE = (255, 255, 255)
BLUE = (0, 0, 205)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

WIDTH = 600
HEIGHT = 600

FPS = 40

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")
clock = pygame.time.Clock()

field = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]

screen.fill(WHITE)

def draw_grid():
    pygame.draw.line(screen, (0, 0, 0), (200, 0), (200, 600), 3)
    pygame.draw.line(screen, (0, 0, 0), (400, 0), (400, 600), 3)
    pygame.draw.line(screen, (0, 0, 0), (0, 200), (600, 200), 3)
    pygame.draw.line(screen, (0, 0, 0), (0, 400), (600, 400), 3)

draw_grid()

def draw_tik_tak_toe():
    cell_size = WIDTH // 3
    for row in range(3):
        for col in range(3):
            if field[row][col] == "x":
                draw_x(col * cell_size, row * cell_size, cell_size)
            elif field[row][col] == "0":
                draw_o(col * cell_size, row * cell_size, cell_size)

def draw_x(x, y, size):
    padding = size // 6
    pygame.draw.line(screen, RED, (x + padding, y + padding), (x + size - padding, y + size - padding), size // 10)
    pygame.draw.line(screen, RED, (x + size - padding, y + padding), (x + padding, y + size - padding), size // 10)

def draw_o(x, y, size):
    center_x = x + size // 2
    center_y = y + size // 2
    radius = size // 3
    pygame.draw.circle(screen, BLUE, (center_x, center_y), radius, size // 10)

def get_win_check(symbol):
    global win
    for i in range(3):
        if field[i][0] == field[i][1] == field[i][2] == symbol:
            win = [[0, i], [1, i], [2, i]]
            return True

    for j in range(3):
        if field[0][j] == field[1][j] == field[2][j] == symbol:
            win = [[j, 0], [j, 1], [j, 2]]
            return True

    if field[0][0] == field[1][1] == field[2][2] == symbol:
        win = [[0, 0], [1, 1], [2, 2]]
        return True

    if field[0][2] == field[1][1] == field[2][0] == symbol:
        win = [[2, 0], [1, 1], [0, 2]]
        return True

    return False

def check_draw():
    for row in field:
        if '' in row:
            return False  # игра не окончена
    return True

def ai_turn():
    # Проверка, может ли компьютер выиграть следующим ходом
    for i in range(3):
        for j in range(3):
            if field[i][j] == "":
                field[i][j] = "0"
                if get_win_check("0"):
                    return
                field[i][j] = ""

    # Проверка, может ли игрок выиграть следующим ходом, и блокировка
    for i in range(3):
        for j in range(3):
            if field[i][j] == "":
                field[i][j] = "x"
                if get_win_check("x"):
                    field[i][j] = "0"
                    return
                field[i][j] = ""

    # Если нет выигрышных или блокирующих ходов, делаем случайный ход
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if field[i][j] == "":
                empty_cells.append((j, i))

    if empty_cells:
        x, y = random.choice(empty_cells)
        field[y][x] = "0"

def draw_win_line():
    if win:
        cell_size = WIDTH // 3
        start_pos = (win[0][0] * cell_size + cell_size // 2, win[0][1] * cell_size + cell_size // 2)
        end_pos = (win[2][0] * cell_size + cell_size // 2, win[2][1] * cell_size + cell_size // 2)
        pygame.draw.line(screen, RED, start_pos, end_pos, 10)

# Основной игровой цикл
run = True
game_over = False
win = None

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = event.pos
            col = mouse_x // (WIDTH // 3)
            row = mouse_y // (HEIGHT // 3)

            if field[row][col] == "":
                field[row][col] = "x"  # Ход игрока

                if get_win_check("x"):
                    print("Вы ХАРОШ!!!")
                    game_over = True
                elif check_draw():
                    print("Ничья!")
                    game_over = True
                else:
                    ai_turn()  # Ход компьютера
                    if get_win_check("0"):
                        print("Компьютер победил!")
                        game_over = True
                    elif check_draw():
                        print("Ничья!")
                        game_over = True

    screen.fill(WHITE)  # Очищаем экран
    draw_grid()  # Рисуем сетку
    draw_tik_tak_toe()  # Рисуем крестики-нолики

    if game_over:
        draw_win_line()

    pygame.display.flip()

pygame.quit()
