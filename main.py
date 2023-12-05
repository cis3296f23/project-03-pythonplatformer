import os
import sys
import random
import math
import button
import pygame
from os import listdir
from os.path import isfile, join
from time import sleep

pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

# Define fonts
font = pygame.font.SysFont("arialblack", 40)

# Define colors
TEXT_COL = (255, 255, 255)

# Load button images
resume_img = pygame.image.load("assets/images/button_resume.png").convert_alpha()
quit_img = pygame.image.load("assets/images/button_quit.png").convert_alpha()
#levels_img = pygame.image.load("assets/images/button_levels.png").convert_alpha()

# Create Button instances
resume_button = button.Button(364, 100, resume_img, 1)
quit_button = button.Button(396, 300, quit_img, 1)
#levels_button = button.Button(297, 250, levels_img, 1)



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


# class is for infinitely generating the map
class Level:
    def __init__(self):
        self.platforms = []

    def generate_new_platforms(self, x_start, num_platforms, block_size, height):
        for i in range(num_platforms):
            x_position = x_start + i * block_size
            new_platform = Block(x_position, height - block_size, block_size)
            self.platforms.append(new_platform)

    def generate_spikes(self, x_start, num_spikes, block_size, height):
        for _ in range(num_spikes):
            x_position = x_start + random.randint(0, WIDTH - block_size)
            y_position = height - block_size - random.randint(1, 1) * block_size
            new_spike = Spike(x_position, y_position, block_size)
            self.platforms.append(new_spike)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "HooterTheOwl", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    # function for player respawn
    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.x_vel = 0
        self.jump_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("Enemies", "Skateboarder", 32, 32, True)
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = -3
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.walkCount = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update_sprite(self):
        sprite_sheet = "walk"
        if self.x_vel != 0:
            sprite_sheet = "walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, respawn_point):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

    #if the player collides with a spike they are sent to the respawn point
    for obj in objects:
        if isinstance(obj, Spike) and pygame.sprite.collide_mask(player, obj):
            player.make_hit()
            player.respawn(*respawn_point)
            break

#the spike class that generates the spikes
class Spike(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "spike")
        spike_image = self.load_spike_image(size)
        self.image.blit(spike_image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def load_spike_image(size):
        path = join("assets", "Traps", "Spikes", "Idle.png")  # Update this path as needed
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (size, size))


def main(window):


    # Game variables
    game_paused = False
    menu_state = "main"

    clock = pygame.time.Clock()
    background, bg_image = get_background("cityBackground5.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    enemy = Enemy(200, 200, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]

    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    # initialize the level class for generating platforms
    level = Level()
    level.generate_new_platforms(-WIDTH // block_size, 20, block_size, HEIGHT)

    # sets spawn point for if player falls off the map
    respawn_point = (100, 100)

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:

        clock.tick(FPS)


        # Check if game is paused
        if game_paused:
            if menu_state == "main":
                # draw pause screen buttons
                if resume_button.draw(window):
                    game_paused = False
                # if levels_button.draw(window):
                #     menu_state = "levels"
                if quit_button.draw(window):
                    run = False
        else:
            draw_text("Press P to pause", font, TEXT_COL, 300, 100)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # Pause menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = True
                    window.fill((255, 255, 255))
            if event.type == pygame.QUIT:
                run = False

            # updated to jump with up arrow Or spacebar because using spacebar is weird
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player.jump_count < 2:
                    player.jump()


        pygame.display.update()








        # while in this loop, the platforms will continue to generate as long
        # as the player continues to head left
        rightmost_platform = max(level.platforms, key=lambda plat: plat.rect.x)
        if rightmost_platform.rect.x < WIDTH + offset_x:
            level.generate_new_platforms(rightmost_platform.rect.x + block_size, 5, block_size, HEIGHT)
            level.generate_spikes(rightmost_platform.rect.x, 1, block_size, HEIGHT)  # Adjust the number of spikes as needed

        objects = level.platforms + [fire]

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects, respawn_point)
        draw(window, background, bg_image, player, objects, offset_x)

        # if player falls off of the map, the player will respawn at the starting point
        if player.rect.y > HEIGHT:
            player.respawn(*respawn_point)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel



    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
