import pygame
import random
from tgol_conf import TgolConf


conf = TgolConf()

# Inicialización de Pygame
pygame.init()

# Tamaño de la pantalla
screen_width, screen_height = conf.screen_size()

# Crear la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de la Vida")

# Fuente para el texto en el sidebar
font = pygame.font.Font(None, 40)
font_ruler = pygame.font.Font(None, conf.cell_size)

# Inicializar la matriz del juego
game_grid = [[0] * conf.cols for _ in range(conf.rows)]


# Función para dibujar la cuadrícula en la pantalla
def draw_grid():
    screen.fill(conf.bg_color)

    if conf.draw_coordinates:
        # Dibuja números en el lateral izquierdo
        for i in range(-1, conf.rows):
            text = font_ruler.render(str(i), True, conf.grid_color)
            screen.blit(text, (conf.sidebar_width + 3, 3 + i * conf.cell_size))

        # Dibuja números en la parte superior
        for j in range(-1, conf.cols):
            text = font_ruler.render(str(j), True, conf.grid_color)
            screen.blit(text, (conf.sidebar_width + j * conf.cell_size + 3, 3))

    if conf.draw_grid_lines:
        # Dibuja líneas de la cuadrícula
        for i in range(0, screen_height, conf.cell_size):
            pygame.draw.line(
                screen, conf.grid_color, (conf.sidebar_width, i), (screen_width, i), 1
            )
        for j in range(conf.sidebar_width, screen_width, conf.cell_size):
            pygame.draw.line(screen, conf.grid_color, (j, 0), (j, screen_height), 1)

    for i in range(conf.rows):
        for j in range(conf.cols):
            if game_grid[i][j] == 1:
                pygame.draw.rect(
                    screen,
                    conf.cell_color,
                    (
                        conf.sidebar_width + j * conf.cell_size,
                        i * conf.cell_size,
                        conf.cell_size,
                        conf.cell_size,
                    ),
                )


# Función para inicializar aleatoriamente la matriz del juego
def randomize_grid():
    for i in range(conf.rows):
        for j in range(conf.cols):
            game_grid[i][j] = random.choice([0, 1])


# Función para actualizar el juego
def update_game():
    new_grid = [[0] * conf.cols for _ in range(conf.rows)]
    for i in range(conf.rows):
        for j in range(conf.cols):
            total = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if not conf.toroidal:
                        if 0 <= i + x < conf.rows and 0 <= j + y < conf.cols:
                            total += game_grid[i + x][j + y]
                    else:
                        total += game_grid[(i + x) % conf.rows][(j + y) % conf.cols]

            if game_grid[i][j] == 1:
                total -= 1
                if total < 2 or total > 3:
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = 1
            else:
                if total == 3:
                    new_grid[i][j] = 1
    return new_grid


# Función para contar las células vivas en la cuadrícula
def count_live_cells():
    count = sum(sum(row) for row in game_grid)
    return count


# Bucle principal del juego
running = True
paused = False
speed = 10
generation = 0

randomize_grid()
clock = pygame.time.Clock()

# Inicializar el sidebar
sidebar = pygame.Surface((conf.sidebar_width, screen_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            conf.save()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                generation = 0
                randomize_grid()
            if event.key == pygame.K_t:
                conf.toggle_toroidal()
            if event.key == pygame.K_g:
                conf.toggle_grid_lines()
            if event.key == pygame.K_c:
                conf.toggle_coordinates()
            if event.key == pygame.K_q:
                conf.save()
                exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        speed = speed + 1 if 10 <= speed <= 60 else 10

    if keys[pygame.K_z]:
        speed = speed - 1 if speed > 10 else 60

    if not paused:
        game_grid = update_game()
        generation += 1

    # Dibujar la cuadrícula
    draw_grid()

    # Actualizar el sidebar
    sidebar.fill(conf.side_bg_color)

    live_cells_text = font.render(
        f"Living: {count_live_cells()}", True, conf.font_color
    )
    generation_text = font.render(f"Generation: {generation}", True, conf.font_color)
    toroidal_text = font.render(f"Toroidal: {conf.toroidal}", True, conf.font_color)
    grid_lines_text = font.render(
        f"Grid: {conf.draw_grid_lines}", True, conf.font_color
    )
    speed_text = font.render(f"Speed: {speed}", True, conf.font_color)

    sidebar.blit(live_cells_text, (25, 25))
    sidebar.blit(generation_text, (25, 75))
    sidebar.blit(toroidal_text, (25, 125))
    sidebar.blit(grid_lines_text, (25, 175))
    sidebar.blit(speed_text, (25, 225))
    screen.blit(sidebar, (0, 0))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
