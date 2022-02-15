from typing import List
import pygame
from pygame.surface import Surface

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

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100


class Paddle():
    """Paddle shape
    """
    COLOR = WHITE  # paddle color

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Args:
            x (int): x position
            y (int): y position
            width (int): paddle width
            height (int): paddle height
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def draw(self, win: pygame.surface.Surface) -> None:
        pygame.draw.rect(win, self.COLOR,
                         (self.x, self.y, self.width, self.height))


def draw(win: pygame.surface.Surface, paddles: List[Paddle]):
    """Draw on the screen"""
    # Change screen background
    win.fill(BLACK)

    # Draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # Update display
    pygame.display.update()


def main():
    """"Program"""
    # Is the game running?
    run = True

    # make game run on same framerame on every computer
    clock = pygame.time.Clock()

    # Paddles
    left_paddle = Paddle(10, (HEIGHT//2)-(PADDLE_HEIGHT//2),
                         PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH, (HEIGHT//2)-(PADDLE_HEIGHT//2),
                          PADDLE_WIDTH, PADDLE_HEIGHT)

    # Program main event loop
    while run:
        clock.tick(FPS)

        # Draw on screen
        draw(WIN, [left_paddle, right_paddle])

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
