""" A simple tetris game
    coded in python
    using pygame and random
    module
"""

import pygame
import random
from network import Network

pygame.font.init()

# Global variables
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600 # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Shapes
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
# indices 0 - 6 represent shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# function  & class definitions

class Piece(object): # all board pieces
      def __init__(self, x, y, shape):
            self.x = x
            self.y = y
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]
            self.rotation = 0


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def create_grid(locked_pos={}): # all board # locked_pos is initialised in an empty dictionary
      # a 10 by 20  color grid
      grid = [[(0, 0, 0)for x in range(10)] for x in range(20)]

      for i in range(len(grid)):
            for j in range(len(grid[i])): # we use this bcoz we are now in the grid above
                  if (j, i) in locked_pos:
                        c = locked_pos[(j, i)]
                        grid[i][j] = c
                  
      return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
      # we are adding a piece to an empty space only and only if the condition 'if grid[i][j] == (0,0,0)'
      accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
      accepted_pos = [j for sub in accepted_pos for j in sub] # This takes all positions in our list and adds them to a 1 dimenstion list

      formatted = convert_shape_format(shape)

      for pos in formatted: # Check to see if the position is real in valid positions
            if pos not in accepted_pos:
                  if pos[1] > -1:
                        return False
      return True


def check_lost(positions):
      for pos in positions:
            x, y = pos
            if y < 1:
                  return True
      return False


def get_shape():
      return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
      font = pygame.font.SysFont('Times New Roman', size, bold=True)
      label = font.render(text, 1, color)

      surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))


def draw_grid(surface, grid):
      sx = top_left_x # sx stands for start x
      sy = top_left_y # sy stands for start y

      for i in range(len(grid)):
            pygame.draw.line(surface, GREY, (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
            for j in range(len(grid[i])):
                  pygame.draw.line(surface, GREY, (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
      inc = 0 # inc is increment
      for i in range(len(grid)-1, -1, -1): # this will loop our grid backwards starting from the 20th floor
            row = grid[i]
            if (0,0,0) not in row:
                  inc += 1
                  ind = i
                  for j in range(len(row)):
                        try:
                              del locked[(j, i)]
                        except:
                              continue

      if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                  x, y = key
                  if y < ind:
                        newKey = (x, y + inc)
                        locked[newKey] = locked.pop(key)

      return inc

def draw_next_shape(shape, surface):
      font = pygame.font.SysFont('Helvetica', 30)
      label = font.render('Next Shape: ', 1, WHITE)

      # plotting the x and y
      sx = top_left_x + play_width + 50
      sy = top_left_y + play_height / 2 - 100
      format = shape.shape[shape.rotation % len(shape.shape)]

      for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                  if column == '0':
                        pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

      surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
      score = max_score()

      with open('scores.txt', 'w') as f:
            if int(score) > nscore:
                  f.write(str(score))
            else:
                  f.write(str(nscore))

def max_score():
      with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip() # strip() prevents any use of blackslashes in code mode


      return score


def draw_window(surface, grid, score=0, last_score=0):
      surface.fill((0,0,0)) # initialise black as the initial color of the grid

      # writing text
      pygame.font.init()
      font = pygame.font.SysFont('Times New Roman', 35)
      label = font.render('Tetris Game', 1, WHITE)

      # draw the label
      surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

      # Score display side
      font = pygame.font.SysFont('Helvetica', 25)
      label = font.render('Score: ' + str(score), 1, WHITE)

      # plotting the x and y
      sx = top_left_x + play_width + 50
      sy = top_left_y + play_height / 2 - 100

      surface.blit(label, (sx + 15, sy + 160))

      # High Score display side
      label = font.render('High Score: ' + last_score, 1, WHITE)

      sx = top_left_x - 200
      sy = top_left_y + 200

      surface.blit(label, (sx + 15, sy + 160))

      for i in range(len(grid)):
            for j in range(len(grid[i])):
                  pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

      pygame.draw.rect(surface, RED, (top_left_x, top_left_y, play_width, play_height), 5)

      draw_grid(surface, grid) #function call
      # pygame.display.update()


def main(win):
      n = Network()
      startPos = read_pos(n.getPos())
      last_score = max_score()
      locked_positions = {} # an empty dictionary
      grid = create_grid(locked_positions)

      change_piece = False
      run = True # for the while loop
      current_piece = get_shape()
      next_piece = get_shape()
      clock = pygame.time.Clock()
      fall_time = 0
      fall_speed = 0.30
      level_time = 0
      score = 0

      while run:
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime() # what this does is that is add the total time taken to run the while loop to fall_time
            clock.tick()
            level_time += clock.get_rawtime()

            if level_time/1000 > 5:
                  level_time = 0
                  if fall_speed > 0.12: # the .12 is a terminal velocity
                        fall_speed -= 0.005

            if fall_time/1000 > fall_speed:
                  fall_time = 0
                  current_piece.y += 1
                  if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y -= 1
                        change_piece = True

            for event in pygame.event.get():

                  if event.type == pygame.QUIT:
                        run = False
                        pygame.display.quit()

                  if event.type == pygame.KEYDOWN:
                        # key listeners
                        if event.key == pygame.K_LEFT:
                              current_piece.x -= 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.x += 1

                        if event.key == pygame.K_RIGHT:
                              current_piece.x += 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.x -= 1


                        if event.key == pygame.K_UP:
                              # rotate shape
                              current_piece.rotation = current_piece.rotation + 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.rotation = current_piece.rotation - 1

                        if event.key == pygame.K_DOWN:
                              # move shape down
                              current_piece.y += 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.y -= 1


            shape_pos = convert_shape_format(current_piece)

            for i in range(len(shape_pos)):
                  x, y = shape_pos[i]
                  if y > -1:
                        grid[y][x] = current_piece.color

            if change_piece:
                  for pos in shape_pos:
                        p = (pos[0], pos[1])
                        locked_positions[p] = current_piece.color
                  current_piece = next_piece
                  next_piece = get_shape()
                  change_piece = False
                  score += clear_rows(grid, locked_positions) * 10

            draw_window(win, grid, score, last_score)
            draw_next_shape(next_piece, win)
            pygame.display.update()

            if check_lost(locked_positions):
                  win.fill(BLACK)
                  draw_text_middle(win, "YOU LOST!!!", 80, RED)
                  pygame.display.update()
                  pygame.time.delay(2000)
                  run = False  # or you can use pygame.display.quit()
                  update_score(score)

      pygame.time.delay(5000)
      pygame.display.quit()

def main_menu(win):
      run = True
      while run:
            win.fill(BLACK)
            draw_text_middle(win, "Press any key to play", 60, WHITE)
            pygame.display.update()

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False

                  if event.type == pygame.KEYDOWN:
                        main(win)

      pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris Game')

main_menu(win)