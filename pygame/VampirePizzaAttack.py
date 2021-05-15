import pygame
from pygame import *
from random import randint

pygame.init()
clock = time.Clock()

SPAWN_RATE = 360
FRAME_RATE = 60

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)

GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('attack of the Vampire Pizzas!')

background_img = image.load('assets/restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_RES)


WIDTH = 100
HEIGHT = 100
WHITE = (255, 255, 255)
tile_color = WHITE
for row in range(6):
    for column in range(11):
        draw.rect(BACKGROUND, tile_color, (WIDTH*column, HEIGHT*row, WIDTH, HEIGHT), 1)

GAME_WINDOW.blit(BACKGROUND, (0,0))
pizza_img = image.load('assets/vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, WIDTH))

class VampireSprite(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.lane = randint(0, 4)
        all_vampires.add(self)
        self.image = VAMPIRE_PIZZA.copy()
        y = 50 + self.lane * 100
        self.rect = self.image.get_rect(center = (1100, y))

    def update(self, game_window):
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.x -= self.speed

        game_window.blit(self.image, (self.rect.x, self.rect.y))


all_vampires = sprite.Group()





# peperoni
# draw.circle(GAME_WINDOW, (255, 0, 0), (1100, 600), 25, 0)
# pizza box
# draw.rect(GAME_WINDOW, (0, 255, 0), (25, 25, 50, 25), 5)

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False
    if randint(1, 360) == 1:
        VampireSprite()

    for vampire in all_vampires:
        vampire.update(GAME_WINDOW)

    display.update()
    clock.tick(FRAME_RATE)

pygame.quit()