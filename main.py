# Imports necessary modules
import pygame, sys
from pygame.locals import *
import random, time
import pygame.transform


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

# Other variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 1

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
        self.image = pygame.image.load("src/player.png").convert()  # Load player image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale the image to desired size
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (160, 520)  # Position the player near the bottom

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Get the current state of all keyboard buttons
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:  # Move left if left arrow is pressed
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:  # Move right if right arrow is pressed
                self.rect.move_ip(5, 0)

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Get the current state of all keyboard buttons
        # Uncomment the following lines to enable vertical movement
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:  # Move left if left arrow is pressed
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:  # Move right if right arrow is pressed
                self.rect.move_ip(5, 0)

# Setting up sprites
P1 = Player()
E1 = Enemy()

# Creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
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
            SPEED += 2
        if event.type == QUIT:
            running = False

    DISPLAYSURF.blit(BACKGROUND, (0, 0))  # Отобразить фоновое изображение

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        pygame.display.update()
        time.sleep(2)

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


