import pygame
from config import Config

# pygame init
pygame.init()

# create the screen
screen = pygame.display.set_mode(Config.windowSize)

# window caption
pygame.display.set_caption(Config.windowCaption)

# window logo
icon = pygame.image.load(Config.windowIconPath)
pygame.display.set_icon(icon)

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(Config.backgroundColour)
    pygame.display.update()


