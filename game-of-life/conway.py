import pygame
import random

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PIXEL_SIZE = 4


def get_row_neigbour_count(row_data, col_idx, col_max, ignore_center):
  count =0

  if col_idx >0:
    if row_data[col_idx -1]:
      count +=1

  if col_idx < col_max:
    if row_data[col_idx +1]:
      count +=1

  if not ignore_center and row_data[col_idx]:
    count +=1

  return count


def get_neigbour_count(grid, row, col):
  row_max = len(grid) -1
  col_max = len(grid[0]) -1

  neighbour_count =0
  if row > 0:
    above_row = grid[row-1]
    neighbour_count += get_row_neigbour_count(above_row, col,col_max, False)

  if row < row_max:
    below_row = grid[row+1]
    neighbour_count += get_row_neigbour_count(below_row, col,col_max, False)

  neighbour_count += get_row_neigbour_count(grid[row], col,col_max, True)

  return neighbour_count


def generate_grid(grid_width, grid_height):
  grid = []
  for _ in range (grid_height):
    row_data = []
    for _ in range (grid_width):
      rand_val = random.randint(1,5)
      row_data.append(rand_val == 4)
    grid.append(row_data)
    
  return grid
  

def display_game(game_screen: pygame.Surface, grid, colour):
  game_screen.fill(BLACK)

  row_offset, column_offset = 0,0
  for row in grid:
    column_offset =0
    for val in row:
      if val:
        pixel = pygame.Rect(column_offset, row_offset, PIXEL_SIZE, PIXEL_SIZE)
        pygame.draw.rect(game_screen,colour,pixel)
      column_offset += PIXEL_SIZE
    row_offset += PIXEL_SIZE

 
def next_step (grid):
  next_grid = []
  for row_idx, row in enumerate(grid):
    next_row = []
    for col_idx, val in enumerate(row):
      neighbour_count = get_neigbour_count(grid,row_idx, col_idx)
      next_value = is_alive(val, neighbour_count)
      next_row.append(next_value)
    next_grid.append(next_row)
  
  return next_grid

def is_alive(val, neighbour_count):
    next_value = False
    if val:
      if neighbour_count >=2 and neighbour_count <=3:
        next_value = True
    else:
      if neighbour_count == 3:
        next_value = True
    return next_value

def main(GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_SIZE):
    size = (800, 600)
    pygame.init()
    game_screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game of Life")
# pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()

    grid_width = SCREEN_WIDTH// PIXEL_SIZE
    grid_height = SCREEN_HEIGHT// PIXEL_SIZE
    grid = generate_grid(grid_width, grid_height)

    exit_game = False
    while not exit_game:
      grid = next_step(grid)
      display_game(game_screen, grid, GREEN)
      for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
          exit_game = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
          if event.key == 114:
            grid = generate_grid(grid_width, grid_height)
        if event.type == pygame.MOUSEBUTTONDOWN:
          mouse_x,mouse_y = pygame.mouse.get_pos()
          grid_x = mouse_x // PIXEL_SIZE
          grid_y = mouse_y // PIXEL_SIZE
          grid[grid_y][grid_x] = True

      pygame.display.flip()
      clock.tick(500)


    pygame.quit()

main(GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_SIZE)
