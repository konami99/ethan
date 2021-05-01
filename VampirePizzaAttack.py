import pygame
from pygame import *
pygame.init()
GAME_WINDOW = display.set_mode((1200, 700))
display.set_caption('attack of the Vampire Pizzas!')

background_img = image.load('restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, (1200, 700))
GAME_WINDOW.blit(BACKGROUND, (0,0))

pizza_img = image.load('vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (100, 100))
GAME_WINDOW.blit(VAMPIRE_PIZZA, (1100 ,600))


# peperoni
# draw.circle(GAME_WINDOW, (255, 0, 0), (1100, 600), 25, 0)
# pizza box
# draw.rect(GAME_WINDOW, (0, 255, 0), (25, 25, 50, 25), 5)

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False
    display.update()
pygame.quit()