from PIL import Image, ImageDraw
from opensimplex import OpenSimplex
import random
import math
import colorsys

WIDTH, HEIGHT = 500, 500

def blob(center_x, center_y, size):
     '''Takes size and a center point as input and generates a polygon shape using opensimplex noise to vary the radius around that center point.
        Returns a list of polygon points'''

     points = [] #list of polygon points
     rando = random.uniform(-1, 1)
     base_r = size
     deform = size *0.4
     gen = OpenSimplex(random.randint(0, 1000)) #noise
     seed = random.random() * 10
     for a in range(0, 361, 2):
          #sample noise in a circle to ensure the start and end meet smoothly
          nx, ny = math.cos(math.radians(a))+1, math.sin(math.radians(a))+1
          noise_val = gen.noise3(nx, ny, seed) 

          r = base_r + (noise_val * deform) #radius
          x = center_x + r * math.cos(math.radians(a))
          y = center_y +  r * math.sin(math.radians(a))
          points.append((int(x), int(y)))

     return points

def draw_image(image, x, y, size, color, alph, iterations, mv):
     '''Takes the position and color as input and performs a random walk across the canvas, drawing noise shapes at each step with slowly drifting HSV color'''
     hue, hue_min, hue_max = color['hue'], color['hue_min'], color['hue_max']
     saturation, saturation_min, saturation_max = color['saturation'], color['saturation_min'], color['saturation_max']
     value, value_min, value_max = color['value'], color['value_min'], color['value_max']

     for i in range(iterations):
          #drift pos
          x += random.uniform(-mv, mv)
          y += random.uniform(-mv, mv)
          #wrap pos
          if x > WIDTH:
               x = 0
          if x < 0:
               x = WIDTH
          if y > HEIGHT:
               y = 0
          if y < 0:
               y = HEIGHT

          #hsv drift
          hue_drift = random.uniform(-0.005, 0.005)
          sat_drift = random.uniform(-0.01, 0.01)
          val_drift = random.uniform(-0.01, 0.01)

          #add to the start values
          hue += hue_drift
          saturation += sat_drift
          value += val_drift

          #clamping the values so that it doesn't jump all around
          new_hue = max(hue_min, min(hue, hue_max))
          new_sat = max(saturation_min, min(saturation, saturation_max))
          new_value = max(value_min, min(value, value_max))

          #convert hsv to rgb
          r,g,b = colorsys.hsv_to_rgb(new_hue, new_sat, new_value)
          fill_color = (int(r*255), int(g*255), int(b*255), alph)

          #create temporary image
          temp_image = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
          #get the polygon points
          points = blob(x, y, size)
          #draw polygon on temporary image
          draw = ImageDraw.Draw(temp_image)
          draw.polygon(points, fill=fill_color)

          #draw edgeline
          edge_color = (int(r*200), int(g*200), int(b*200), alph + 10) #darker/higher alpha
          draw.line(points + [points[0]], fill=edge_color, width=1)
          #composite temp onto main image
          image = Image.alpha_composite(image, temp_image)
     
     return image

def texture(image):
     '''Adds a subtle texture to the final image by sampling random pixels and nudging their RGB values slightly, simulating the texture of paper'''
     draw = ImageDraw.Draw(image)
     sample_num = WIDTH*HEIGHT // 50 #sampling roughly 1 in every x pixels
     for i in range(sample_num):
          #pick a random point on the canvas
          x, y = random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)
          #read its rgba values
          r,g,b,a = image.getpixel((x,y))
          vary = 15
          #nudge the rgb channels slightly (by vary)
          new_r = max(0, min(255, r + random.randint(-vary, vary)))
          new_g = max(0, min(255, g + random.randint(-vary, vary)))
          new_b = max(0, min(255, b + random.randint(-vary, vary)))
          #write the color back
          draw.point((x,y), fill =(new_r, new_g, new_b, 200))

     return image

#color values
color1 = {
    'hue': 0.48, 'hue_min': 0.45, 'hue_max': 0.52, 
    'saturation': 0.2, 'saturation_min': 0.1, 'saturation_max': 0.3, 
    'value': 0.7, 'value_min': 0.6, 'value_max': 0.8
}

color2 = {
    'hue': 0.05, 'hue_min': 0.0, 'hue_max': 0.1, 
    'saturation': 0.1, 'saturation_min': 0.05, 'saturation_max': 0.15, 
    'value': 0.6, 'value_min': 0.5, 'value_max': 0.7
}

color3 = {
    'hue': 0.12, 'hue_min': 0.10, 'hue_max': 0.15, 
    'saturation': 0.15, 'saturation_min': 0.1, 'saturation_max': 0.2, 
    'value': 0.95, 'value_min': 0.9, 'value_max': 1.0
}


#create a blank RGBA image as backround
background_color = (35, 30, 60, 255)
image = Image.new('RGBA', (WIDTH, HEIGHT), background_color)

#random starting points for colors
x1 = random.randint(0, WIDTH)
y1 = random.randint(0, HEIGHT)
final_img = draw_image(image, x1, y1, random.randint(40, 70), color1, 5, 500, 30)

x2 = random.randint(0, WIDTH)
y2 = random.randint(0, HEIGHT)
final_img = draw_image(final_img, x2, y2, random.randint(40, 70), color2, 8, 400, 40)

x3 = random.randint(0, WIDTH)
y3 = random.randint(0, HEIGHT)
final_img = draw_image(final_img, x3, y3, random.randint(20, 50), color3, 12, 300, 20)

#add paper texture
final_img = texture(final_img)
final_img.show()