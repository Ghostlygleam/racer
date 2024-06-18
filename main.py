import pygame
import sys
import random
import time
from pygame.locals import *

# Initializes all imported Pygame modules
pygame.init()

# Setting up FPS (frames per second) to control the game's speed
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors using RGB values
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Other variables for use in the program
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SPEED = 1

lives = 5
score = 0
start_time = pygame.time.get_ticks()

# Create a display surface (screen) with a specified size
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)  # Fill the screen with white color
BACKGROUND = pygame.image.load("src/bacgr.png").convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")  # Set the title of the window

# Class for the enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/enemy.png").convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Class for the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("src/player.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        self.image = self.original_image.copy()  # Reset image to original

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.image = pygame.transform.rotate(self.original_image, 15)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.image = pygame.transform.rotate(self.original_image, -15)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        # Keep the player within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Class for the coin sprite
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/coin.png").convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Setting up sprites
P1 = Player()
E1 = Enemy()

# Creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new user event to increase speed periodically
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2
        if event.type == pygame.QUIT:
            running = False

    # Generate coins randomly
    if random.randint(1, 100) == 1:
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    DISPLAYSURF.blit(BACKGROUND, (0, 0))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check for collisions with coins
    coin_collisions = pygame.sprite.spritecollide(P1, coins, True)
    for coin in coin_collisions:
        score += 100

    # Display lives and score
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    DISPLAYSURF.blit(lives_text, (10, 10))
    DISPLAYSURF.blit(score_text, (10, 50))

    # Check for collisions with enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        lives -= 1
        if lives == 0:
            wasted_font = pygame.font.Font(None, 36)
            wasted_text = wasted_font.render("Wasted", True, RED)
            DISPLAYSURF.blit(wasted_text, (150, 250))
            final_score_text = font.render(f"Score: {score}", True, YELLOW)
            DISPLAYSURF.blit(final_score_text, (150, 300))
            pygame.display.update()
            end_time = pygame.time.get_ticks()
            duration = (end_time - start_time) // 1000  # Duration in seconds
            print(f"Survived for {duration} seconds.")
            time.sleep(2)
            pygame.quit()
            sys.exit()

        P1 = Player()
        E1 = Enemy()
        enemies.empty()
        enemies.add(E1)
        all_sprites.empty()
        all_sprites.add(P1)
        all_sprites.add(E1)

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()
