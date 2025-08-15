import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)
SNAKE_HEAD = (34, 139, 34)  # Forest green for head
SNAKE_BODY = (50, 205, 50)  # Lime green for body
SNAKE_BODY_DARK = (0, 128, 0)  # Dark green for body segments
SNAKE_TAIL = (124, 252, 0)  # Light green for tail
YELLOW = (255, 255, 0)  # For snake eyes

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        # Check self collision
        if new_head in self.positions:
            return False

        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

        return True

    def change_direction(self, new_direction):
        # Prevent moving in opposite direction
        if (self.direction[0] * -1, self.direction[1] * -1) != new_direction:
            self.direction = new_direction

    def eat_food(self):
        self.grow = True

    def draw(self, screen):
        for i, pos in enumerate(self.positions):
            x = pos[0] * GRID_SIZE
            y = pos[1] * GRID_SIZE

            if i == 0:  # Snake head
                self.draw_head(screen, x, y)
            elif i == len(self.positions) - 1:  # Snake tail
                self.draw_tail(screen, x, y, i)
            else:  # Snake body
                self.draw_body(screen, x, y, i)

    def draw_head(self, screen, x, y):
        # Draw rounded head
        head_rect = pygame.Rect(x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.ellipse(screen, SNAKE_HEAD, head_rect)
        pygame.draw.ellipse(screen, BLACK, head_rect, 2)

        # Draw eyes based on direction
        eye_size = 3
        if self.direction == UP:
            eye1_pos = (x + 6, y + 5)
            eye2_pos = (x + 14, y + 5)
        elif self.direction == DOWN:
            eye1_pos = (x + 6, y + 12)
            eye2_pos = (x + 14, y + 12)
        elif self.direction == LEFT:
            eye1_pos = (x + 5, y + 6)
            eye2_pos = (x + 5, y + 14)
        else:  # RIGHT
            eye1_pos = (x + 12, y + 6)
            eye2_pos = (x + 12, y + 14)

        pygame.draw.circle(screen, YELLOW, eye1_pos, eye_size)
        pygame.draw.circle(screen, YELLOW, eye2_pos, eye_size)
        pygame.draw.circle(screen, BLACK, eye1_pos, 1)
        pygame.draw.circle(screen, BLACK, eye2_pos, 1)

    def draw_body(self, screen, x, y, segment_index):
        # Alternate body colors for realistic pattern
        if segment_index % 2 == 0:
            color = SNAKE_BODY
        else:
            color = SNAKE_BODY_DARK

        # Draw body segment with slight rounding
        body_rect = pygame.Rect(x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(screen, color, body_rect, border_radius=3)
        pygame.draw.rect(screen, BLACK, body_rect, 1, border_radius=3)

        # Add scale pattern
        center_x = x + GRID_SIZE // 2
        center_y = y + GRID_SIZE // 2
        pygame.draw.circle(screen, DARK_GREEN, (center_x, center_y), 2)

    def draw_tail(self, screen, x, y, segment_index):
        # Get direction to previous segment for tail orientation
        if len(self.positions) > 1:
            curr_pos = self.positions[-1]
            prev_pos = self.positions[-2]
            tail_dir = (curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])
        else:
            tail_dir = (0, 0)

        # Draw tapered tail
        if tail_dir == (1, 0):  # Tail pointing right
            points = [(x, y + 5), (x + GRID_SIZE, y + GRID_SIZE // 2), (x, y + 15)]
        elif tail_dir == (-1, 0):  # Tail pointing left
            points = [(x + GRID_SIZE, y + 5), (x, y + GRID_SIZE // 2), (x + GRID_SIZE, y + 15)]
        elif tail_dir == (0, 1):  # Tail pointing down
            points = [(x + 5, y), (x + GRID_SIZE // 2, y + GRID_SIZE), (x + 15, y)]
        elif tail_dir == (0, -1):  # Tail pointing up
            points = [(x + 5, y + GRID_SIZE), (x + GRID_SIZE // 2, y), (x + 15, y + GRID_SIZE)]
        else:  # Default tail
            points = [(x + 2, y + 2), (x + GRID_SIZE - 2, y + GRID_SIZE // 2), (x + 2, y + GRID_SIZE - 2)]

        pygame.draw.polygon(screen, SNAKE_TAIL, points)
        pygame.draw.polygon(screen, BLACK, points, 1)


class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)

    def respawn(self, snake_positions):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_positions:
                break

    def draw(self, screen):
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE

        # Draw apple-like food
        pygame.draw.circle(screen, RED, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2 - 2)
        pygame.draw.circle(screen, BLACK, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2 - 2, 2)

        # Add apple stem
        stem_x = x + GRID_SIZE // 2
        stem_y = y + 3
        pygame.draw.line(screen, (139, 69, 19), (stem_x, stem_y), (stem_x, stem_y + 4), 2)

        # Add apple highlight
        highlight_x = x + GRID_SIZE // 2 - 3
        highlight_y = y + GRID_SIZE // 2 - 3
        pygame.draw.circle(screen, (255, 100, 100), (highlight_x, highlight_y), 3)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
        return True

    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True
                return

            # Check if snake ate food
            if self.snake.positions[0] == self.food.position:
                self.snake.eat_food()
                self.food.respawn(self.snake.positions)
                self.score += 10

    def draw(self):
        self.screen.fill(BLACK)

        if not self.game_over:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)

            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # Game speed (10 FPS)

        pygame.quit()
        sys.exit()


# Game rules and instructions
def print_rules():
    print("=== SNAKE GAME RULES ===")
    print("1. Use arrow keys to control the snake")
    print("2. Eat red food to grow and increase score")
    print("3. Game over if snake hits the wall")
    print("4. Game over if snake bites itself")
    print("5. Press SPACE to restart after game over")
    print("6. Press ESC to quit")
    print("========================")


if __name__ == "__main__":
    print_rules()
    game = Game()
    game.run()