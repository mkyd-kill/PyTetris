""" A simple tetris game
    coded in python
    using pygame and random
    module
"""

import pygame
import random

pygame.font.init()

# Global variables
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600 # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

WHITE = (255, 255, 255)
RED = (255, 0, 0)

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
            self.color = shape_colors[shape.index(shape)]
            self.rotate = 0


def create_grid(locked_pos={}): # all board # locked_pos is initialised in an empty dictionary
      # a 10 by 20  color grid
      grid = [[(0, 0, 0)for x in range(10)] for x in range(20)]

      for i in range(len(grid)):
            for j in range(len(grid[i])): # we use this bcoz we are now in the grid above
                  if (j, i) in locked_pos:
                        c = locked_pos[(j, i)]
                        grid[i][j] = c
                  
      return grid


def convert_shape_format():
      pass


def valid_space():
      pass


def check_lost():
      pass


def get_shape():
      return Piece(5, 0, random.choice(shapes))


def draw_text_middle():
      pass


def draw_grid(surface, grid):
      for i in range(len(grid)):
            for j in range(len(grid[i])):
                  pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

      pygame.draw.rect(surface, RED, (top_left_x, top_left_y, play_width, play_height), 4)


def clear_rows():
      pass


def draw_next_shape():
      pass


def draw_window(surface, grid):
      surface.fill((0,0,0)) # initialise black as the initial color of the grid

      # writing text
      pygame.font.init()
      font = pygame.font.SysFont('Times New Roman', 40)
      label = font.render('PyTetris Game', 1, WHITE)

      # draw the label
      label.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))

      draw_grid(surface, grid) #function call
      pygame.display.update()


def main(win):
      locked_positions = {} # an empty dictionary
      grid = create_grid(locked_positions)

      change_piece = False
      run = True # for the while loop
      current_piece = get_shape()
      next_piece = get_shape()
      clock = pygame.time.Clock()
      fall_time = 0

      while run:
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False

                  if event.type == pygame.KEYDOWN: # event listeners
                        if event.type == pygame.K_LEFT:
                              current_piece.x -= 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.x += 1

                        if event.type == pygame.K_RIGHT:
                              current_piece.x += 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.x -= 1

                        if event.type == pygame.K_DOWN:
                              current_piece.y +=1
                              if not(valid_space(current_piece, grid)):
                                    current_piece.y -= 1

                        if event.type == pygame.K_UP:
                              current_piece.rotation += 1
                              if not(valid_space(current_piece, grid)):
                                    current_piece -= 1

            draw_window(win, grid)


def main_menu(win):
      main(win)


win = pygame.display.set_mood((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(win)