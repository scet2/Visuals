#L systems

import pygame
from pygame import Vector2
from pygame.locals import *
import math
import matplotlib
import numpy as np
import random

pygame.init()

WIDTH = 500
HEIGHT = 500
FPS = 60

bg_color = (40, 45, 55)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(bg_color)

#rules for the letters
rules = {'S': 'FlGlG', 'F':'FlGrFrGlF', 'G':'GG'}

def expand(sent):
     newStr = ''
     for c in sent:
          rule = rules.get(c, c)
          newStr += rule
     
     return newStr

sent = 'S'

length = 100
iterations = 6

colors = [(160, 85, 75),  
    (190, 115, 90),  
    (215, 145, 110), 
    (235, 175, 140), 
    (245, 210, 165)]
history = []
lengths = []

history.append(sent)
lengths.append(length)

#iterate and add the resulting sequences to the lists along with the reduced lengths
for i in range(iterations):
     sent = expand(sent)
     history.append(sent)
     length *= 0.7
     lengths.append(length)

#get the boundaries of the big triangle
def get_bounds(history, length):
     temp_vec = Vector2(0,0)
     temp_velo = Vector2(length, 0)

     x_coords = [0]
     y_coords = [0]

     for c in history:
          if c in 'FG':
               temp_vec += temp_velo
               x_coords.append(temp_vec.x)
               y_coords.append(temp_vec.y)
          elif c == 'l':
            temp_velo.rotate_ip(-120)
          elif c == 'r':
            temp_velo.rotate_ip(120)

     width = max(x_coords) - min(x_coords)
     height = max(y_coords) - min(y_coords)

     return width, height

x_bound, y_bound = get_bounds(history[-1], lengths[-1]) 

def draw(history, length, colors):
     top_y = (HEIGHT // 2) - (y_bound//2)

     cur_vector = Vector2((WIDTH // 2) - (x_bound//2), (HEIGHT // 2) + (y_bound//2))
     velo = Vector2(length, 0) #direction/length
     angle = 120

     for c in history:
          if c in 'FG': 
               
               #color bottom -> up from the colors list
               rel_y = (cur_vector.y - top_y) / y_bound #if cur_vector.y = top_y then rel_y = 0.0, rel_y approaches 1.0 at the bottom
               rel_y = max(0, min(0.99, rel_y))
               #multiply the number by the length of the colors list
               color_idx = int(rel_y * len(colors)) 
               line_color = colors[color_idx]
               
               new_vector = cur_vector + velo #straight ahead (up)
               pygame.draw.line(screen, line_color, cur_vector, new_vector, 2)
               cur_vector = new_vector 
               
          elif c == 'l':
               velo.rotate_ip(-angle) #rotate left
               
          elif c == 'r':
               velo.rotate_ip(angle) #rotate right

draw(history[-1], lengths[-1], colors[::-1])

def main():
     run = True
     while run:
          clock.tick(FPS)

          for event in pygame.event.get():
               if event.type == QUIT:
                    run = False

          pygame.display.update()
     pygame.quit()

if __name__ == '__main__':
     main()
