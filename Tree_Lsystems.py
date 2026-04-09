import pygame
from pygame import Vector2
from pygame.locals import *
import numpy as np
import random
import math
import colorsys

pygame.init()
pygame.font.get_init()

#settings
WIDTH = 700
HEIGHT = 800
FPS = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (253, 251, 245)
screen.fill(bg)

class Tree():
     def __init__(self):
          self.rules = {'F': 'FF+[+F-F-F]-[-F+F+F]'}
          self.axiom = 'F'
          self.length = 12
          self.strokeW = 5
          self.angle = 22.5
          self.branch_color = (140, 110, 90)
          self.cur_depth = 0

     def expand(self):
          newStr = ''
          for char in self.axiom:
               rule = self.rules.get(char, char)
               newStr += rule
          self.axiom = newStr
          return newStr
     
     def leaf(self, x, y, color):
          width = 10
          height = 20
          leaf_surf = pygame.Surface((width, height), pygame.SRCALPHA)

          halo_color = (color[0], color[1], color[2], 50) #alpha = 50 
          pygame.draw.ellipse(leaf_surf, halo_color, (0, 0, width, height))

          core_color = (color[0], color[1], color[2], 255)
          pygame.draw.ellipse(leaf_surf, core_color, (2, 5, width//2, height//2))

          screen.blit(leaf_surf, (x-width//2, y-height//2))
     
     def draw(self, final_seq):
          stack = []
          cur_vector = Vector2(WIDTH // 2, HEIGHT - 10)
          velo = Vector2(0, -self.length)

          for char in final_seq:
               if char == 'F': #draw straight line up
                    new_vector = cur_vector + velo #straight ahead (up)
                    pygame.draw.line(screen, self.branch_color, cur_vector, new_vector, max(1, int(self.strokeW)))
                    cur_vector = new_vector 
               
               elif char == '+':
                    velo.rotate_ip(-self.angle)
               
               elif char == '-':
                    velo.rotate_ip(self.angle)
               
               # save (push/pop) the spot before branching so we can go back and continue w the other side
               elif char == '[':
                    stack.append((cur_vector.copy(), velo.copy(), self.strokeW))

                    self.strokeW *= 0.7
                    self.cur_depth +=1
               
               elif char == ']' and stack:
                    for i in range(random.randint(4, 6)):
                         jitter_x = random.randint(-5, 5)
                         jitter_y = random.randint(-5, 5)
                         color = (255, 220, 220)
                         self.leaf(cur_vector.x+jitter_x, cur_vector.y + jitter_y, color)
                    
                    cur_vector, velo, self.strokeW = stack.pop()
                    self.cur_depth -=1
iterations = 4
tree = Tree()
final_seq = []
for i in range(iterations):
     add = tree.expand()
     final_seq.append(add)
tree.draw(final_seq[-1])

#main 
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