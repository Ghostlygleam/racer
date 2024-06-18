import pygame
import sys
import random
import time
import math
import pygame.transform
from pygame.locals import *

# Initializes all imported Pygame modules
pygame.init()

# Setting up FPS (frames per second) to control the game's speed
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors using RGB values
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Other variables for use in the program
SCREEN_WIDTH = 1000  
SCREEN_HEIGHT = 800  
SPEED = 1

max_speed = 10
acceleration = 0.05
deceleration = 0.02
turn_speed = 5

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
        self.image = pygame.image.load("src/enemy.png").convert()  # Load enemy image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale the image to desired size
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  # Position the enemy at a random horizontal location at the top

    def move(self):
        self.rect.move_ip(0, SPEED)  # Move the enemy downward
        if (self.rect.top > SCREEN_HEIGHT):  # If the enemy moves out of the screen
            self.rect.top = 0  # Reset to the top
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  # Reposition at a random horizontal location

# Class for the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("src/player.png").convert_alpha()  # Load player image
        self.original_image = pygame.transform.scale(self.image, (50, 50))  # Scale the image to desired size
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)  # Position the player near the bottom
        self.angle = 0
        self.speed = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Get the current state of all keyboard buttons

        # acceleration and deceleration
        if pressed_keys[pygame.K_UP]:
            self.speed = min(max_speed, self.speed + acceleration)
        elif pressed_keys[pygame.K_DOWN]:
            self.speed = max(-max_speed, self.speed - acceleration)
        else:
            if self.speed > 0:
                self.speed = max(0, self.speed - deceleration)
            elif self.speed < 0:
                self.speed = min(0, self.speed + deceleration)
        
        # turn
        if pressed_keys[pygame.K_LEFT]:
            self.angle += turn_speed
        if pressed_keys[pygame.K_RIGHT]:
            self.angle -= turn_speed

        # Update car position
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))

        # Screen rect check
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Turn car image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

# Class for the coin sprite
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("src/coin.png").convert()  # Load coin image
        self.image = pygame.transform.scale(self.image, (30, 30))  # Scale the image to desired size
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  # Position the coin at a random horizontal location at the top

    def move(self):
        self.rect.move_ip(0, SPEED)  # Move the coin downward
        if (self.rect.top > SCREEN_HEIGHT):  # If the coin moves out of the screen
            self.rect.top = 0  # Reset to the top
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  # Reposition at a random horizontal location

# Setting up sprites
P1 = Player()
E1 = Enemy()

# Creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()  # Group for coins
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new user event to increase speed periodically
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Set the timer to trigger every 1000 milliseconds (1 second)

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

    DISPLAYSURF.blit(BACKGROUND, (0, 0))  # Display the background image

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
            DISPLAYSURF.blit(wasted_text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 50))
            final_score_text = font.render(f"Score: {score}", True, YELLOW)
            DISPLAYSURF.blit(final_score_text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
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
