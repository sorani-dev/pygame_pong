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

# Ball
BALL_RADIUS = 7

# Score font
SCORE_FONT = pygame.font.SysFont("comicssans", 50)
# Max score to win the game
WINNING_SCORE = 10


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
        self.x = self.original_x = x
        self.y = self.original_y = y
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

    def reset(self) -> None:
        """Reset the paddle"""
        self.x = self.original_x
        self.y = self.original_y


class Ball():
    """Ball"""
    MAX_VELOCITY = 5  # Maximum ball velocity
    COLOR = WHITE  # Ball color

    def __init__(self, x: int, y: int, radius: int) -> None:
        """Args:
            x (int): x coordinate
            y (int): y coordinate
           radius (int): ball radius
        """
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0.0

    def draw(self, win: Surface):
        """Draw ball on the screen

        Args:
            win (Surface)
        """
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        """Move the ball"""
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self) -> None:
        """Reset the ball's position"""
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity *= -1
        self.y_velocity = 0


def draw(win: pygame.surface.Surface, paddles: List[Paddle], ball: Ball, left_score: int, right_score: int):
    """Draw on the screen"""
    # Change screen background
    win.fill(BLACK)

    # Draw scores
    left_score_text = SCORE_FONT.render(f"{left_score}", True, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, WHITE)

    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -
             right_score_text.get_width()//2, 20))

    # Draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw a dotted line in the middle
    for i in range(10, HEIGHT, HEIGHT//20):
        # Do not draw on odd number
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (((WIDTH//2) - 5, i, 10, HEIGHT//20)))

    # Draw the ball
    ball.draw(win)

    # Update display
    pygame.display.update()


def handle_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> None:
    """Manage collision between the ball and the paddles or the walls

    Args:
        ball (Ball): the ball
        left_paddle (Paddle)
        right_paddle (Paddle)
    """
    # Ceiling (reverse direction)
    if ball.y+ball.radius >= HEIGHT:
        ball.y_velocity *= -1
    # Floor (reverse direction)
    elif ball.y-ball.radius <= 0:
        ball.y_velocity *= -1

    # Left side
    if ball.x_velocity < 0:
        # Left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                # Reverse the y direction
                ball.x_velocity *= -1

                # Where is the ball colliding on the paddle?
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y_paddle = middle_y - ball.y
                # how much does the ball need to reduce its speed based on its position on the paddle
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_in_y_paddle / reduction_factor
                # Set the ball velocity
                ball.y_velocity = y_velocity * -1
    else:
        # Right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                # Reverse the y direction
                ball.x_velocity *= -1

                # Where is the ball colliding on the paddle?
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y_paddle = middle_y - ball.y
                # how much does the ball need to reduce its speed based on its position on the paddle
                reduction_factor = (right_paddle.height /
                                    2) / ball.MAX_VELOCITY
                y_velocity = difference_in_y_paddle / reduction_factor
                # Set the ball velocity
                ball.y_velocity = y_velocity * -1


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

    # Make game run on same frame rate on every computer
    clock = pygame.time.Clock()

    # Paddles
    left_paddle = Paddle(10, (HEIGHT//2)-(PADDLE_HEIGHT//2),
                         PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH, (HEIGHT//2) -
                          (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    # Score
    left_score = 0
    right_score = 0

    # Program main event loop
    while run:
        clock.tick(FPS)

        # Draw on screen
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        # Check events
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                run = False
                break

        # Get all keyboard keys pressed
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        # Move the ball
        ball.move()
        # Ball collision?
        handle_collision(ball, left_paddle, right_paddle)

        # Check the score
        if ball.x < 0:
            # Left player
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            # Right player
            left_score += 1
            ball.reset()

        # Check win
        won = False
        win_text = ''
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            # Show who won in the middle of the screen
            text = SCORE_FONT.render(win_text, True, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                     2, HEIGHT//2-text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)  # 5s

            # Reset all
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
