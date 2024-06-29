import pygame
import sys
import random
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1820, 980
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
JETBRAINS_RADIUS = 20
PELLET_RADIUS = 16
GHOST_RADIUS = 35
NUM_PELLETS = 12

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JetBrains")

class JetBrains:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.direction = 0
        self.speed = 5

    def update_position(self):
        if self.direction == 0:
            self.x += self.speed
        elif self.direction == 1:
            self.y -= self.speed
        elif self.direction == 2:
            self.x -= self.speed
        elif self.direction == 3:
            self.y += self.speed
        self.x = max(JETBRAINS_RADIUS, min(WIDTH - JETBRAINS_RADIUS, self.x))
        self.y = max(JETBRAINS_RADIUS, min(HEIGHT - JETBRAINS_RADIUS, self.y))

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), JETBRAINS_RADIUS)

class Pellet:
    def __init__(self):
        self.position = (random.randint(PELLET_RADIUS, WIDTH - PELLET_RADIUS), random.randint(PELLET_RADIUS, HEIGHT - PELLET_RADIUS))

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.position, PELLET_RADIUS)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_direction = 0
        self.y_direction = 0
        self.speed = 4

    def move(self, target_x, target_y):
        if target_x < self.x:
            self.x_direction = -1
        elif target_x > self.x:
            self.x_direction = 1
        else:
            self.x_direction = 0

        if target_y < self.y:
            self.y_direction = -1
        elif target_y > self.y:
            self.y_direction = 1
        else:
            self.y_direction = 0

        self.x += self.x_direction * self.speed
        self.y += self.y_direction * self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), GHOST_RADIUS)

class Game:
    def __init__(self):
        self.jetbrains = JetBrains()
        self.pellets = [Pellet() for _ in range(NUM_PELLETS)]
        self.ghosts = [Ghost(1600, 400), Ghost(400, 1600)]
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()

    def reset(self):
        self.jetbrains = JetBrains()
        self.pellets = [Pellet() for _ in range(NUM_PELLETS)]
        self.ghosts = [Ghost(1600, 400), Ghost(400, 1600)]
        self.score = 0
        self.game_over = False

    def check_win_condition(self) -> bool:
        return len(self.pellets) == 0

    def eat_pellet(self):
        for pellet in self.pellets[:]:
            distance = pygame.math.Vector2(self.jetbrains.x - pellet.position[0], self.jetbrains.y - pellet.position[1]).length()
            if distance < JETBRAINS_RADIUS + PELLET_RADIUS:
                self.pellets.remove(pellet)
                self.score += 1
                self.jetbrains.speed += 1  # Increase speed by 1

    def handle_ghost_collision(self):
        for ghost in self.ghosts:
            distance = pygame.math.Vector2(self.jetbrains.x - ghost.x, self.jetbrains.y - ghost.y).length()
            if distance < JETBRAINS_RADIUS + GHOST_RADIUS:
                self.game_over = True

    def draw_pellets(self):
        for pellet in self.pellets:
            pellet.draw()

    def draw_ghosts(self):
        for ghost in self.ghosts:
            ghost.draw()

    def draw_game_over_screen(self, message: str):
        squircle_width, squircle_height = 600, 300
        squircle_rect = pygame.Rect(WIDTH // 2 - squircle_width // 2, HEIGHT // 2 - squircle_height // 2, squircle_width, squircle_height)
        pygame.draw.rect(screen, GRAY, squircle_rect, border_radius=50)
        font = pygame.font.Font(None, 72)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(text_surface, text_rect)
        font = pygame.font.Font(None, 36)
        play_again_text = font.render("Press Enter to Play Again", True, BLUE)
        screen.blit(play_again_text, (WIDTH // 2 - 170, HEIGHT // 2 + 20))
        exit_text = font.render("Press Escape to Exit", True, BLUE)
        screen.blit(exit_text, (WIDTH // 2 - 150, HEIGHT // 2 + 70))

    def run_start_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return  # Exit the start menu and start the game
            self.draw_start_menu()

    def draw_start_menu(self):
        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        title_text = font.render("Keep away from the red circles", True, BLUE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)
        
        font = pygame.font.Font(None, 72)
        start_text = font.render("Collect the yellow circles to win", True, BLUE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 75))
        screen.blit(start_text, start_rect)

        font = pygame.font.Font(None, 36)
        start_text = font.render("Press Enter to Start", True, GREEN)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(start_text, start_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.jetbrains.direction = 0
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.jetbrains.direction = 1
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.jetbrains.direction = 2
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.jetbrains.direction = 3
                else:
                    if event.key == pygame.K_RETURN:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def update_game_state(self):
        if not self.game_over:
            self.jetbrains.update_position()
            self.eat_pellet()
            for ghost in self.ghosts:
                ghost.move(self.jetbrains.x, self.jetbrains.y)
            self.handle_ghost_collision()

            if self.check_win_condition():
                self.game_over = True

    def draw_game_screen(self):
        screen.fill(BLACK)
        self.draw_pellets()
        self.draw_ghosts()
        self.jetbrains.draw()

        if self.game_over:
            if self.check_win_condition():
                self.draw_game_over_screen("YOU WIN!!!")
            else:
                self.draw_game_over_screen("Game Over!!!")
        else:
            self.draw_score()

        pygame.display.flip()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLUE)
        screen.blit(score_text, (10, 10))

    def main_game_loop(self):
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw_game_screen()
            self.clock.tick(60)

# Initialize and run the game
game = Game()
game.run_start_menu()
game.main_game_loop()
