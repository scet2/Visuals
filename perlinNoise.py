import pygame
from pygame.locals import *
import random
import numpy as np
from perlin_noise import PerlinNoise 
import pandas as pd

pygame.init()

#settings
WIDTH = 500
HEIGHT = 500
FPS = 60

clock = pygame.time.Clock()

#set screen and backround
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = (143, 196, 204)
screen.fill(bg)

#colors csv with 677 color palettes with 5 RGB tuples 
colors = pd.read_csv('colors.csv')

def get_color(row_idx):
     '''Takes a row index as input and returns 5 RGB tuples (a whole color palette)'''
     row = colors.iloc[row_idx]
     color = [(int(row.iloc[i*3]), int(row.iloc[i*3+1]), int(row.iloc[i*3+2])) for i in range(5)]
     
     return color

def get_noise_array(noise1, noise2):
     '''Takes two perlin noise as input and returns the average normalized np array'''
     scale = 0.009
     noise_map_1 = [[noise1([x*scale, y*scale]) for y in range(500)] for x in range(500)]
     noise_map_2 = [[noise2([x*scale, y*scale]) for y in range(500)] for x in range(500)]
     
     #convert noise maps to np arrays
     arr_1 = np.array(noise_map_1)
     arr_2 = np.array(noise_map_2)

     #average them together and normalize 
     avg_arr = (arr_1 + arr_2) / 2
     avg_arr = (avg_arr - avg_arr.min()) / (avg_arr.max() - avg_arr.min())

     return avg_arr

def draw_result(palette, noise_array):
     '''Takes a noise array and a palette as arguements and returns the colored noise array'''
     #sf = random.uniform(0.5, 1)
     sf = 0.5
     transformed = np.mod(noise_array / sf, 1)

     #create an empty color layer (height, width, 3 for rgb)
     color_world = np.zeros((500, 500, 3), dtype=np.uint8)

     #map noise to the colors
     color_world[transformed < 0.2] = palette[0]
     color_world[(transformed >= 0.2) & (transformed < 0.4)] = palette[1]
     color_world[(transformed >= 0.4) & (transformed < 0.6)] = palette[2]
     color_world[(transformed >= 0.6) & (transformed < 0.8)] = palette[3]
     color_world[transformed >= 0.8] = palette[4]

     return color_world

def generate(palette_count=3):
     '''Takes pallete count as input and returns the final colored map'''
     #create two seperate perlin noise maps stored as lists
     noise1 = PerlinNoise(octaves=6, seed=1)
     noise2 = PerlinNoise(octaves=10, seed=2)

     #get the noise array
     noise_array = get_noise_array(noise1, noise2)

     #collect x (3) color palettes at random 
     all_palettes = []
     for i in range(palette_count):
          cur_color = get_color(random.randint(0, len(colors)-1))
          all_palettes.append(cur_color)
     
     #collect all the color_world arrays in a list then average them
     results = []
     for pal in all_palettes:
          color_world = draw_result(pal, noise_array)
          results.append(color_world)

     final_result = np.mean(results, axis = 0)
     norm_final = (final_result - final_result.min()) / (final_result.max() - final_result.min())
     norm_final = (norm_final*255).astype(np.uint8)

     #display the result
     #surface = pygame.surfarray.make_surface(norm_final)
     surface = pygame.surfarray.make_surface(final_result)
     return surface
     

#main loop
def main():
     art = generate()
     i = 0
     run = True
     while run:
          clock.tick(FPS)

          for event in pygame.event.get():
               if event.type == QUIT:
                    run = False
               if event.type == KEYDOWN:
                    if event.key == K_s:
                         pygame.image.save(screen, f"perlinNoiseArt{i}.png")
                         i+=1
               if event.type == MOUSEBUTTONDOWN:
                    art = generate()
               
          screen.blit(art, (0,0))

          pygame.display.update()   
     
     pygame.quit()

if __name__ == '__main__':
     main()
