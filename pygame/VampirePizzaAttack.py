import pygame
from pygame import *
from random import randint

from pygame import constants
from pygame import display
from pygame import time
from pygame import image
from pygame import transform
from pygame import draw
from pygame import mouse
from pygame import sprite
from pygame import font
from pygame.draw import rect
from pygame.font import Font

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

STARTING_BUCK = 30
BUCK_RATE = 200
STARTING_BUCK_BOOSTER = 3

MAX_BAD_REVIEWS = 3
WIN_TIME = FRAME_RATE * 60 * 3

REG_SPEED = 2
SLOW_SPEED = 1

WIDTH = 100
HEIGHT = 100
WHITE = (255, 255, 255)

tile_color = WHITE
tile_grid = []

pizza_img = image.load('assets/vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, WIDTH))

garlic_image = image.load('assets/garlic.png')
garlic_surf = Surface.convert_alpha(garlic_image)
GARLIC = transform.scale(garlic_surf, (WIDTH, HEIGHT))

cutter_image = image.load('assets/pizzacutter.png')
cutter_surf = Surface.convert_alpha(cutter_image)
CUTTER = transform.scale(cutter_surf, (WIDTH, HEIGHT))

pepperoni_image = image.load('assets/pepperoni.png')
pepperoni_surf = Surface.convert_alpha(pepperoni_image)
PEPPERONI = transform.scale(pepperoni_surf, (WIDTH, HEIGHT))

class Trap(object):
    def __init__(self, trap_kind, cost, trap_img):
        self.trap_kind = trap_kind
        self.cost = cost
        self.trap_img = trap_img

SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 3, CUTTER)
EARN = Trap('EARN', 7, PEPPERONI)

class VampireSprite(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.lane = randint(0, 4)
        all_vampires.add(self)
        self.image = VAMPIRE_PIZZA.copy()
        y = 50 + self.lane * 100
        self.rect = self.image.get_rect(center = (1100, y))
        self.health = 100

    def update(self, game_window, counters):
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.x -= self.speed

        if self.health <= 0 or self.rect.x <= 100:
            self.kill()
            if self.rect.x <= 100:
                counters.bad_reviews += 1
        else:
            game_window.blit(self.image, (self.rect.x, self.rect.y))

    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = SLOW_SPEED
        if tile.trap == DAMAGE:
            self.health = self.health - 1


class Counters(object):
    def __init__(self, pizza_bucks, buck_rate, buck_booster, timer):
        self.loop_count = 0
        self.display_font = Font('assets/pizza_font.ttf', 25)
        self.pizza_bucks  = pizza_bucks
        self.buck_rate = buck_rate
        self.buck_booster = buck_booster
        self.bucks_rect = None
        self.timer = timer
        self.timer_rect = None
        self.bad_reviews = 0
        self.bad_rev_rect = None
    
    def increment_bucks(self):
        if self.loop_count % self.buck_rate == 0:
            self.pizza_bucks = self.pizza_bucks + self.buck_booster

    def draw_bucks(self, game_window):
        if bool(self.bucks_rect):
            game_window.blit(BACKGROUND, (self.bucks_rect.x, self.bucks_rect.y), self.bucks_rect)

        bucks_surf = self.display_font.render(str(self.pizza_bucks), True, WHITE)
        self.bucks_rect = bucks_surf.get_rect()
        self.bucks_rect.x = WINDOW_WIDTH - 50
        self.bucks_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(bucks_surf, self.bucks_rect)

    def draw_bad_reviews(self, game_window):
        if bool(self.bad_rev_rect):
            game_window.blit(BACKGROUND, (self.bad_rev_rect.x, self.bad_rev_rect.y), self.bad_rev_rect)
        bad_rev_surf = self.display_font.render(str(self.bad_reviews), True, WHITE)
        self.bad_rev_rect = bad_rev_surf.get_rect()
        self.bad_rev_rect.x = WINDOW_WIDTH - 150
        self.bad_rev_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(bad_rev_surf, self.bad_rev_rect)

    def draw_timer(self, game_window):
        if bool(self.timer_rect):
            game_window.blit(BACKGROUND, (self.timer_rect.x, self.timer_rect.y), self.timer_rect)
        timer_surf = self.display_font.render(str((WIN_TIME - self.loop_count) // FRAME_RATE), True, WHITE)
        self.timer_rect = timer_surf.get_rect()
        self.timer_rect.x = WINDOW_WIDTH - 150
        self.timer_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(timer_surf, self.timer_rect)

    def update(self, game_window):
        self.loop_count = self.loop_count + 1
        self.increment_bucks()
        self.draw_bucks(game_window)
        self.draw_bad_reviews(game_window)
        self.draw_timer(game_window)


class TrapApplicator(object):
    def __init__(self):
        self.selected = None

    def select_trap(self, trap):
        if trap.cost <= counters.pizza_bucks:
            self.selected = trap

    def select_tile(self, tile, counters):
        self.selected = tile.set_trap(self.selected, counters)

trap_applicator = TrapApplicator()

class BackgroundTile(sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.trap = None
        self.rect = rect

class PlayTile(BackgroundTile):
    def set_trap(self, trap, counters):
        if bool(trap) and not bool(self.trap):
            counters.pizza_bucks -= trap.cost
            self.trap = trap
            if trap == EARN:
                counters.buck_booster += 1
        return None
    def draw_trap(self, game_window, trap_applicator):
        if bool(self.trap):
            game_window.blit(self.trap.trap_img, (self.rect.x, self.rect.y))

class ButtonTile(BackgroundTile):
    def set_trap(self, trap, counters):
        if counters.pizza_bucks >= self.trap.cost:
            return self.trap
        else:
            return None

    def draw_trap(self, game_windwow, trap_applicator):
        if bool(trap_applicator.selected):
            if trap_applicator.selected == self.trap:
                draw.rect(game_windwow, (238, 190, 47), (self.rect.x, self.rect.y, WIDTH, HEIGHT), 5)

class InactiveTile(BackgroundTile):
    def set_trap(self, trap, counters):
        return None

    def draw_trap(self, game_window, trap_applicator):
        pass


all_vampires = sprite.Group()

counters = Counters(STARTING_BUCK, BUCK_RATE, STARTING_BUCK_BOOSTER, WIN_TIME)



for row in range(6):
    row_of_tiles = []
    tile_grid.append(row_of_tiles)

    for column in range(11):
        tile_rect = Rect(WIDTH*column, HEIGHT*row,WIDTH, HEIGHT)
        if column <= 1:
            new_tile = InactiveTile(tile_rect)
        else:
            if row == 5:
                if 2 <= column <= 4:
                    new_tile = ButtonTile(tile_rect)
                    new_tile.trap = [SLOW, DAMAGE, EARN][column - 2]
                else:
                    new_tile = InactiveTile(tile_rect)
            else:
                new_tile = PlayTile(tile_rect)

        row_of_tiles.append(new_tile)
        if row == 5:
            if 2 <= column <= 4:
                BACKGROUND.blit(new_tile.trap.trap_img, (new_tile.rect.x, new_tile.rect.y))

        if column !=0 and row != 5:
            if column != 1:
                draw.rect(BACKGROUND, tile_color, (WIDTH * column, HEIGHT * row, WIDTH, HEIGHT), 1)

GAME_WINDOW.blit(BACKGROUND, (0, 0))

game_running = True
program_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False
            program_running = False

        elif event.type == MOUSEBUTTONDOWN:
            coordinates = mouse.get_pos()
            x = coordinates[0]
            y = coordinates[1]

            tile_y = y // 100
            tile_x = x // 100
            trap_applicator.select_tile(tile_grid[tile_y][tile_x], counters)

    if randint(1, SPAWN_RATE) == 1:
        VampireSprite()

    for tile_row in tile_grid:
        for tile in tile_row:
            if bool(tile.trap):
                GAME_WINDOW.blit(BACKGROUND, (tile.rect.x, tile.rect.y), tile.rect)

    for vampire in all_vampires:
        tile_row = tile_grid[vampire.rect.y // 100]
        vampire_left_side = vampire.rect.x // 100
        vampire_right_side = (vampire.rect.x + vampire.rect.width) // 100
        if 0 <= vampire_left_side <= 10:
            left_tile = tile_row[vampire_left_side]
        else:
            left_tile = None

        if 0 <= vampire_right_side <= 10:
            right_tile = tile_row[vampire_right_side]
        else:
            right_tile = None

        if bool(left_tile):
            vampire.attack(left_tile)
        if bool(right_tile):
            if right_tile != left_tile:
                vampire.attack(left_tile)

        if counters.bad_reviews >= MAX_BAD_REVIEWS:
            game_running = False
        if counters.loop_count > WIN_TIME:
            game_running = False

    for vampire in all_vampires:
        vampire.update(GAME_WINDOW, counters)

    for tile_row in tile_grid:
        for tile in tile_row:
            tile.draw_trap(GAME_WINDOW, trap_applicator)

    counters.update(GAME_WINDOW)
    display.update()
    clock.tick(FRAME_RATE)

end_font = font.Font('assets/pizza_font.ttf', 50)
if program_running:
    if counters.bad_reviews >= MAX_BAD_REVIEWS:
        end_surf = end_font.render('Game Over', True, WHITE)
    else:
        end_surf = end_font.render('You Win!', True, WHITE)
    GAME_WINDOW.blit(end_surf, (350, 200))
    display.update()

while program_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            program_running = False

    clock.tick(FRAME_RATE)

pygame.quit()