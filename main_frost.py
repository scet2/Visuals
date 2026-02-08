import pygame
import random
import numpy as np
from pygame.locals import *

pygame.init()

#settings
WIDTH = 640
HEIGHT = 480
FPS = 60

clock = pygame.time.Clock()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Frost Simulation')

bg = (0,0,0)
screen.fill(bg)

#variables
start_x, start_y = WIDTH//2, HEIGHT//2 #starting point
x, y = start_x, start_y
#colorList = [(102, 102, 255), (112, 18, 127), (255, 204, 229), (0, 153,153), (255, 178, 102)]
color_index = 0
pixelColor = screen.map_rgb(((112, 128, 144)))
pixel_count = 0
updateFlag = True
min_x, min_y = x, y
max_x, max_y = x, y
padSize = 20 #creates a bounded box 20 pixels in each direction , total = 40x40 centered on the starting point 
#so that the pixels/frost wont branch out far away, at least for that one loop, creates a compact frost pattern.
domainMinX = start_x - padSize
domainMaxX = start_x + padSize
domainMinY = start_y - padSize
domainMaxY = start_y + padSize

#create pixel array
pixelArray = pygame.PixelArray(screen)
pixelArray[start_x, start_y] =  pixelColor

#functions
def on_loop(): #adding a pixel each time the function is called
     global x,y, new_x, new_y, domainMinX, domainMaxX, domainMinY, domainMaxY, updateFlag, min_x, max_x, min_y, max_y
     #choose random direction in wwhich to move (down, up, right, left) + diagonal movements
     newDir = random.choice(((0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (-1,1), (1,-1)))
     
     #extract dx, dy. delta is the change in position
     dx, dy = newDir

     #apply the change to the actual x and y coordinates
     new_x =x + dx
     new_y =y + dy

     #check we stay within the domain
     if new_x < domainMinX: #if pixel goes past the domain left edge
          new_x = domainMaxX #wraparound
     if new_x > domainMaxX: #same for the right edge
          new_x = domainMinX
     if new_y < domainMinY: #top edge
          new_y = domainMaxY
     if new_y > domainMaxY: #bottom edge
          new_y = domainMinY

     #check if pixel has already been seen, i.e. no backtracking
     if pixelArray[new_x, new_y] != screen.map_rgb(bg):
          updateFlag = True
          #modify the extent of the simulation domain if necessary
          if x < min_x:
               min_x = x
          if x > max_x:
               max_x = x
          if y < min_y:
               min_y = y
          if y > max_y:
               max_y = y
          #modify the domain itself
          domainMinX = max(min_x - padSize, 1)
          domainMaxX = min(max_x + padSize, WIDTH-1)
          domainMinY = max(min_y - padSize, 1)
          domainMaxY = min(max_y + padSize, HEIGHT - 1)

     else:
          updateFlag = False
          x, y = new_x, new_y #if pixel hasn't been colored, then the pixel becomes the new x and y
          #pixelArray[x, y] = pixelColor
          #pygame.display.update()
def on_render(): #display the pixels
     global x, y, updateFlag, new_x, new_y, domainMinX, domainMaxX, domainMinY, domainMaxY, pixel_count, color_index, pixelColor
     #update pixel array
     if updateFlag:
          pixelArray[x, y] = pixelColor #pixel at x,y coordinates turns pixelColor
          pixel_count += 1
          pygame.display.update()
          #reset update flag and random walk
          updateFlag = False 
          #select one of the four sides of the domain to start from
          newSide = random.choice((1,2,3,4))
          if newSide == 1:
               x = domainMinX
               y = int(random.uniform(domainMinY, domainMaxY)) #generates a random int between the upper and lower bounds of the domain
          elif newSide == 2:
               x = int(random.uniform(domainMinX, domainMaxX))
               y = domainMinY
          elif newSide == 3:
               x = domainMaxX
               y = int(random.uniform(domainMinY, domainMaxY))
          else:
               x = int(random.uniform(domainMinX, domainMaxX))
               y = domainMaxY
#number of pixels
max_pixel = 5000

#main loop
def main():
     run = True
     while run:
          clock.tick(FPS)

          for event in pygame.event.get():
               if event.type == QUIT:
                    run = False

          for i in range(2000):  # simulate n particles per frame
               if pixel_count >= max_pixel:
                    break
               on_loop()
               on_render()
               
     pygame.quit()

if __name__ == '__main__':
     main()