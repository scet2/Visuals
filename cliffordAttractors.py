import pygame
from pygame.locals import *
import random
from math import sin, cos, sqrt, fabs, exp
from numba import njit
import numpy as np
from perlin_noise import PerlinNoise 
import pandas as pd
from pygame.surfarray import make_surface

pygame.init()

#settings
WIDTH = 800
HEIGHT = 600
FPS = 60

clock = pygame.time.Clock()

#set screen and backround
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = (253, 241, 226)
screen.fill(bg)

#other variables
purple = (101, 90, 124)
iters = 5000000
skipIters = 10
sensitivity = 0.02

#vlifford attractor params
a = 1.5
b = -1.8
c = 1.6
d = 0.9

#view bounds (region of x,y space mapped to the image)
minX = -4
maxX = 4
minY = minX * HEIGHT/WIDTH
maxY = maxX * HEIGHT/WIDTH

arr = np.zeros((HEIGHT, WIDTH)) #counts for the pixels

@njit
def Clifford(a, b, c, d, iters, arr, WIDTH, HEIGHT, minX, maxX, minY, maxY):
     x, y = 0,0 #starting coordinates
     for i in range(iters):
          xn = sin(a * y) + c * cos(a * x) #new x pos
          yn = sin(b * x) + d * cos(b * y) #new y pos
          x = xn
          y = yn

          if i < skipIters: #warmup phase, not drawn untill skipIters
               continue
          xi = int((x - minX) * WIDTH / (maxX - minX)) #translate point to pixel
          yi = int((y - minY) * HEIGHT / (maxY - minY))

          if (xi >= 0) and (xi < WIDTH) and (yi >= 0) and (yi < HEIGHT):
               arr[yi, xi] += 1 
     
     return arr

#using the exponential curve to squash huge raw numbers from the denarr counts into a scale from 0 to 255 
def toneMapping(den_arr, sensitivity):
     return (1.0 - np.exp( -sensitivity * den_arr)) 

def coloring(percent, color):
     #initialize r,g,b values
     r = bg[0] + (percent * (color[0] - bg[0]))
     g = bg[1] + (percent * (color[1] - bg[1]))
     b = bg[2] + (percent * (color[2] - bg[2]))

     #stack rgb
     return np.stack([r, g, b], axis=-1).astype(np.uint8).swapaxes(0, 1) #to match pygame surface (width, height)

#put everything together
den_arr = Clifford(a, b, c, d, iters, arr, WIDTH, HEIGHT, minX, maxX, minY, maxY)
percent = toneMapping(den_arr, sensitivity)
colored_arr = coloring(percent, purple)

surf = make_surface(colored_arr)
screen.blit(surf, (0,0))

#main loop
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
