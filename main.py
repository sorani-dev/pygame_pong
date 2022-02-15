import pygame

# Initialize pygame
pygame.init()

# Variables
# Window dimensions
WIDTH, HEIGHT = 700, 500
# Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Game Frame rate
FPS = 60

# Colors
WHITE = (255, 255, 255,)
BLACK = (0, 0, 0,)


def draw(win: pygame.surface.Surface):
    """Draw on the screen"""
    # Change screen background
    win.fill(BLACK)

    # Update display
    pygame.display.update()


def main():
    """"Program"""
    # Is the game running?
    run = True

    # make game run on same framerame on every computer
    clock = pygame.time.Clock()

    # Program main event loop
    while run:
        clock.tick(FPS)

        # Draw on screen
        draw(WIN)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
