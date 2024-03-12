import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.start_x = x  # Store initial x position for reset
        self.start_y = y  # Store initial y position for reset
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.direction_x = 0  # Initialize direction
        self.direction_y = 1

    def update(self):
        # Move the ball
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        # Check for collisions with walls
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.direction_x *= -1
        if self.y <= self.radius:
            self.direction_y *= -1

        # Reset position if ball goes beyond bottom edge
        if self.y >= HEIGHT + self.radius:
            self.reset()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction_x = 0
        self.direction_y = 1


class Bar:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def update(self):
        # Move the bar with keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Keep the bar within the screen bounds
        if self.x <= 0:
            self.x = 0
        elif self.x >= WIDTH - self.width:
            self.x = WIDTH - self.width

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


# Function to create a grid of bricks
def create_bricks():
    brick_width = 70
    brick_height = 20
    bricks = []
    for row in range(4):
        for col in range(10):
            brick_x = col * (brick_width + 5) + 30
            brick_y = row * (brick_height + 5) + 30
            bricks.append(Brick(brick_x, brick_y, brick_width, brick_height, BLUE))
    return bricks


# Main game loop
def main():
    # Create a ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, 10, RED, 5)

    # Create a bar
    bar = Bar(WIDTH // 2 - 50, HEIGHT - 20, 100, 10, BLACK, 8)

    # Create bricks
    bricks = create_bricks()

    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game objects
        ball.update()
        bar.update()

        # Check for collision between ball and bar
        if bar.y <= ball.y + ball.radius <= bar.y + bar.height:
            if bar.x <= ball.x <= bar.x + bar.width:
                # Adjust ball's direction based on where it hits the bar
                relative_intersect_x = (bar.x + bar.width / 2) - ball.x
                normalized_intersect_x = relative_intersect_x / (bar.width / 2)
                ball.direction_x = normalized_intersect_x
                ball.direction_y = -1

        # Check for collision between ball and bricks
        for brick in bricks:
            if brick.visible:
                if ball.x + ball.radius >= brick.x and ball.x - ball.radius <= brick.x + brick.width:
                    if ball.y - ball.radius <= brick.y + brick.height:
                        ball.direction_y *= -1
                        brick.visible = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw game objects
        ball.draw()
        bar.draw()
        for brick in bricks:
            brick.draw()

        # Update display
        pygame.display.flip()

        # Limit frames per second
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
