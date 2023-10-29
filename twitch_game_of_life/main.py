import pygame
import random
import json

# Dimensiones de la cuadrícula
n = 50  # Número de filas
m = 75  # Número de columnas
cell_size = 20  # Tamaño de cada cuadro en píxeles
sidebar_width = 275  # Ancho del sidebar

# Example usage:
theme_file = "./themes/vibrant2.json"  # Replace with the actual filename

# Inicialización de Pygame
pygame.init()

# Tamaño de la pantalla
screen_width = m * cell_size + sidebar_width
screen_height = n * cell_size

# Crear la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de la Vida")

# Fuente para el texto en el sidebar
font = pygame.font.Font(None, 40)
font_ruler = pygame.font.Font(None, cell_size)

# Inicializar la matriz del juego
game_grid = [[0] * m for _ in range(n)]

# Colores
cell_color = (100, 65, 165)
bg_color = (241, 241, 241)
grid_color = (185, 163, 227)
side_bg_color = (38, 38, 38)
font_color = (241, 241, 241)


def load_colors_from_json(filename):
    try:
        with open(filename, "r") as file:
            color_data = json.load(file)
        return color_data
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{filename}'.")
    return None


theme = load_colors_from_json(theme_file)

if theme:
    cell_color = theme.get("cell_color")
    bg_color = theme.get("bg_color")
    grid_color = theme.get("grid_color")
    side_bg_color = theme.get("side_bg_color")
    font_color = theme.get("font_color")

# Variable para controlar si se deben dibujar las líneas de la cuadrícula
draw_grid_lines = True

# Variable para controlar si se deben dibujar las coordenadas de la cuadricula
draw_coordinates = True

# Variable para controlar el tipo de mundo (toroidal o no toroidal)
toroidal = False


# Función para dibujar la cuadrícula en la pantalla
def draw_grid():
    screen.fill(bg_color)

    if draw_coordinates:
        # Dibuja números en el lateral izquierdo
        for i in range(-1, n):
            text = font_ruler.render(str(i), True, grid_color)
            screen.blit(text, (sidebar_width + 3, 3 + i * cell_size))

        # Dibuja números en la parte superior
        for j in range(-1, m):
            text = font_ruler.render(str(j), True, grid_color)
            screen.blit(text, (sidebar_width + j * cell_size + 3, 3))

    if draw_grid_lines:
        # Dibuja líneas de la cuadrícula
        for i in range(0, screen_height, cell_size):
            pygame.draw.line(
                screen, grid_color, (sidebar_width, i), (screen_width, i), 1
            )
        for j in range(sidebar_width, screen_width, cell_size):
            pygame.draw.line(screen, grid_color, (j, 0), (j, screen_height), 1)

    for i in range(n):
        for j in range(m):
            if game_grid[i][j] == 1:
                pygame.draw.rect(
                    screen,
                    cell_color,
                    (
                        sidebar_width + j * cell_size,
                        i * cell_size,
                        cell_size,
                        cell_size,
                    ),
                )


# Función para inicializar aleatoriamente la matriz del juego
def randomize_grid():
    for i in range(n):
        for j in range(m):
            game_grid[i][j] = random.choice([0, 1])


# Función para actualizar el juego
def update_game():
    new_grid = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            total = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if not toroidal:
                        if 0 <= i + x < n and 0 <= j + y < m:
                            total += game_grid[i + x][j + y]
                    else:
                        total += game_grid[(i + x) % n][(j + y) % m]

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
sidebar = pygame.Surface((sidebar_width, screen_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                generation = 0
                randomize_grid()
            if event.key == pygame.K_t:
                toroidal = not toroidal
            if event.key == pygame.K_g:
                draw_grid_lines = not draw_grid_lines
            if event.key == pygame.K_c:
                draw_coordinates = not draw_coordinates
            if event.key == pygame.K_q:
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
    sidebar.fill(side_bg_color)

    live_cells_text = font.render(f"Living: {count_live_cells()}", True, font_color)
    generation_text = font.render(f"Generation: {generation}", True, font_color)
    toroidal_text = font.render(f"Toroidal: {toroidal}", True, font_color)
    grid_lines_text = font.render(f"Grid: {draw_grid_lines}", True, font_color)
    speed_text = font.render(f"Speed: {speed}", True, font_color)

    sidebar.blit(live_cells_text, (25, 25))
    sidebar.blit(generation_text, (25, 75))
    sidebar.blit(toroidal_text, (25, 125))
    sidebar.blit(grid_lines_text, (25, 175))
    sidebar.blit(speed_text, (25, 225))
    screen.blit(sidebar, (0, 0))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
