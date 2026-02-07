import pygame
from pygame import *
import random
import math
import colorsys

pygame.init()

#settings
WIDTH = 600
HEIGHT = 600
FPS = 1

clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (255,255,255)


class Flower:
     def __init__(self):
          #flower attributes
          self.hue = random.randint(0, 360)
          self.petalCount = random.randint(3, 8) * 4
          self.rowCount = random.randint(10, 30)
          self.color = (self.hue, 100, 100)
          self.width = random.randint(25, 40)
          self.height = random.randint(100, 150)

          #shift factor, random angle in radians
          self.shift = random.uniform(0.8, 2.0) 

          #base offset vector, the 'stick' connecting the flower center to the petal
          distance_from_center = self.width*1.2
          self.base_offset = Vector2(0, -(self.height/2 + distance_from_center))

     def petal(self, surface, cP):

          base_h, base_s, base_v, base_a = cP.hsva

          #start from the biggest petal
          for i in reversed(range(1, 21)):

               #calculate cur size
               frac = i/ 20.0
               cur_w = self.width * frac
               cur_h = self.height * frac

               #center the ellipses
               center_x = (self.width - cur_w) / 2
               center_y = (self.height - cur_h) / 2

               #shift hue inwards
               new_hue = (base_h + i*2) % 360
               new_color = pygame.Color(0)
               new_color.hsva = (new_hue, 80, 5*i, base_a) #value(v)=brightness
          
               #draw the ellipse onto this surface
               pygame.draw.ellipse(surface, new_color, (center_x, center_y, cur_w, cur_h))

               #draw the outline/weird effect
               #pygame.draw.ellipse(surface, (0, 0, 0), (center_x, center_y, cur_w, cur_h), width=1)

     def draw(self, screen, x, y):
          #create pivot point/center of the flower on screen
          pivot_point = Vector2(x, y)

          cur_vector = self.base_offset.copy()

          #track rotation and scaling for row
          cur_row_rotation = 0
          cur_scale = 1.0 #start at 100% size

          for r in range(self.rowCount):

               cur_hue = (self.hue + r * 20) % 360
               row_color = pygame.Color(0)
               row_color.hsva= (cur_hue, 100, 100, 100)

               #create transparent surface for one petal
               master_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

               self.petal(master_surf, row_color)

               display_surf = transform.scale_by(master_surf, cur_scale)

               for i in range(self.petalCount):
                    #compute angle for petal 
                    angle = (i * (360/self.petalCount)) + cur_row_rotation

                    #rotate the base offset vector
                    ro = cur_vector.rotate(angle)
                    
                    #compute center of petal
                    petal_center = pivot_point + ro

                    #rotate the surface
                    rs = pygame.transform.rotate(display_surf, -angle) 

                    #create the new rect and set its center to the calculated pos
                    new_rect = rs.get_rect()
                    new_rect.center = petal_center

                    #draw the petal
                    screen.blit(rs, new_rect)

               cur_row_rotation += math.degrees(self.shift)

               #shrink the petal each row

               cur_vector = cur_vector * 0.6
               cur_scale = cur_scale * 0.8

def main():
     run = True
     while run:
          screen.fill(bg)
          clock.tick(FPS)

          for event in pygame.event.get():
               if event.type == QUIT:
                    run = False

          f = Flower()
          f.draw(screen, WIDTH//2, HEIGHT//2)

          pygame.display.update()
     pygame.quit()

if __name__ == '__main__':
     main()