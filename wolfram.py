#Made by LimonAga. Press 'esc' to exit window, 'space' to change color. (don
import sys
import random
import colorsys
import pygame
import numpy as np

pygame.init()
info = pygame.display.Info()
# Constants
FPS = 10
alive_color = (255, 255, 255)
dead_color = (0, 0, 0)
change_color = False

WINDOW_WIDTH, WINDOW_HEIGHT = info.current_w, info.current_h
CELL_SIZE = 5

# Initialize the grid with zeros
grid = np.zeros((WINDOW_WIDTH // CELL_SIZE), dtype=int)

# Set up the Pygame screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wolfram Cellular Automaton')
clock = pygame.time.Clock()

# Function to determine the next state based on the ruleset
def rules(left, middle, right):
    binary_code = int(f"{left}{middle}{right}", 2)
    return ruleset[binary_code]

# Function to update the grid for the next generation
def update_grid(grid):
    new_grid = np.zeros((WINDOW_WIDTH // CELL_SIZE), dtype=int)
    
    for i in range(len(grid)):
        if i == 0 or i == len(grid) - 1:
            # Skip edges for now (keep them as zeros)
            new_grid[i] = 0
        else:
            left = grid[i-1]
            middle = grid[i]
            right = grid[i+1]

            # Apply the rules to determine the new state
            new_grid[i] = rules(left, middle, right)
    return new_grid

# Function to draw the grid
def draw_grid(max_generations, cell_states, delay_ms=50, slow_draw=True):
    for generation in range(max_generations):
        for col_index, cell_state in enumerate(cell_states):
            if cell_state:
                cell_color = alive_color
            else:
                cell_color = dead_color
            cell_rect = pygame.Rect(col_index * CELL_SIZE, generation * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, cell_color, cell_rect)
        cell_states = update_grid(cell_states)
        pygame.display.flip()  # Update the screen
        if slow_draw:
            pygame.time.delay(delay_ms)  # Introduce a delay in milliseconds

max_gen = WINDOW_HEIGHT // CELL_SIZE
grid_size = WINDOW_WIDTH // CELL_SIZE

# Initial configuration of the grid
def create_new_grid():
    grid = [0 for _ in range(grid_size)]
    grid[grid_size // 2] = 1
    return grid

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE:
                    change_color = not change_color

    # Get a empty grid
    grid = create_new_grid()

    if change_color:
        # Generate a random hue value (0 to 1) and convert it to RGB
        random_hue = random.uniform(0, 1)
        rgb_color = colorsys.hsv_to_rgb(random_hue, 1.0, 1.0)

        # Scale the RGB values to the range (0, 255)
        alive_color = (
            int(rgb_color[0] * 255),
            int(rgb_color[1] * 255),
            int(rgb_color[2] * 255)
        )

    else:
        alive_color = (255, 255, 255)
    # Get a random ruleset
    ruleset = [int(bit) for bit in format(random.randint(0, 255), '08b')]

    # Draw the initial grid
    draw_grid(max_gen, grid)
    clock.tick(FPS)
