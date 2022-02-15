from typing import List, Sequence
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
    COLOR = WHITE  # Paddle color
    VELOCITY = 4  # Paddle velocity

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
        """Draw paddle on screen

        Args:
            win (pygame.surface.Surface): Pygame window
        """
        pygame.draw.rect(win, self.COLOR,
                         (self.x, self.y, self.width, self.height))

    def move(self, up: bool = True) -> None:
        """Move paddle up or down the screen depending on the selected key

        Args:
            up (bool, optional): Which direction is the paddle supposed to move (Up or Down). Defaults to True.
        """
        # Move up or down
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY


def draw(win: pygame.surface.Surface, paddles: List[Paddle]):
    """Draw on the screen"""
    # Change screen background
    win.fill(BLACK)

    # Draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw a dotted line in the middle
    for i in range(10, HEIGHT, HEIGHT//20):
        # Do not draw on odd number
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (((WIDTH//2) - 5, i, 10, HEIGHT//20)))

    # Update display
    pygame.display.update()


def handle_paddle_movement(keys: Sequence[bool], left_paddle: Paddle, right_paddle: Paddle) -> None:
    """Change the paddle movement on which key is pressed

    Args:
        keys (Sequence[bool]): Keys pressed
        left_paddle (Paddle)
        right_paddle (Paddle)
    """
    # Left paddle movement
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # Right paddle movement
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    """"Program"""
    # Is the game running?
    run = True

    # Make game run on same framerame on every computer
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
            # Quit game
            if event.type == pygame.QUIT:
                run = False
                break

        # Get all keyboard keys pressed
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

    pygame.quit()


if __name__ == '__main__':
    main()
