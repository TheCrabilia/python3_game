import pygame as pg
import random
from colors import *


class GameWindow:
    """
    Game window class. Contains main game loop.
    """

    def __init__(self, size: tuple):
        self.width, self.height = size
        self.screen = pg.display.set_mode((self.width, self.height))

        self.player = Player(position=(100, self.height - 20), radius=10, color=RED)
        self.score_widget = Score(position=(700, 20), font_size=32, bg_color=GRAY)

        self._obstacles = []
        self.obstacle_spawn_delay = 60

        self.game_over = False

    def main_loop(self):
        """
        Main game loop. Processes pressed keys events, calls object update method.
        """
        # Set clock (FPS)
        clock = pg.time.Clock()
        fps = 30

        # Initialize pygame
        pg.init()

        # Set game screen caption
        pg.display.set_caption("Simple game")

        finished = False

        # Game loop
        while not finished:
            clock.tick(fps)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

            self.screen.fill(GRAY)

            if not self.game_over:
                keys = pg.key.get_pressed()
                if not self.player.get_jump_status():  # True if method returns False (player does not jump)
                    if keys[pg.K_SPACE] or keys[pg.K_UP]:
                        self.player.set_jump_status(True)
                else:
                    self.player.jump()

                # Destroy obstacle if it is out of the screen
                self.destroy_obstacle()

                # Move obstacles on the screen
                for obstacle in self._obstacles:
                    obstacle.move()

                self.detect_collision()
                self.spawn_new_obstacle()
            else:
                Text(text="Game Over", position=(self.width / 2 - 150, self.height / 2 - 50),
                     font_size=50, bg_color=GRAY).draw(self.screen)

            self.update_objects()
            pg.display.update()

    def update_objects(self):
        """
        Updates all objects on the screen.
        """
        # Draw obstacles on the screen
        for obstacle in self._obstacles:
            obstacle.draw(self.screen)

        # Draw player on the screen
        self.player.draw(self.screen)
        # Draw score widget on the screen
        self.score_widget.draw(self.screen)

    def spawn_new_obstacle(self):
        if self.obstacle_spawn_delay == 60:
            dimensions = [(20, 60), (20, 20)]
            random_dimensions = random.choices(dimensions, weights=(70, 45), k=1)
            # Create new obstacle
            new_obstacle = Obstacle(position=(self.width + 20, self.height - 70),
                                    dimensions=random_dimensions[0], color=BLACK)
            self._obstacles.append(new_obstacle)
            self.obstacle_spawn_delay = 0
        else:
            self.obstacle_spawn_delay += 1

    def destroy_obstacle(self):
        if len(self._obstacles) != 0:
            if self._obstacles[0].get_x() == 0:
                self._obstacles.pop(0)

    def detect_collision(self):
        player_x, player_y, player_radius = self.player.get_metrics()
        for obstacle in self._obstacles:
            obstacle_x, obstacle_y, obstacle_width, obstacle_height = obstacle.get_metrics()
            if obstacle_y <= (player_y + player_radius) <= (obstacle_y + obstacle_height):
                if obstacle_x <= (player_x + player_radius) <= (obstacle_x + obstacle_width):
                    self.game_over = True


class Player:
    """
    Player class. Draws player on the main game window, realizes player mechanic - jump.
    """
    def __init__(self, position: tuple, radius: int, color: tuple, speed: int = 10):
        self.x, self.y = position
        self.radius = radius
        self.speed = speed
        self.color = color

        # Jump mechanic variables
        self._jump_count = 8
        self.is_jump = False

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def jump(self):
        if self._jump_count >= -8:
            if self._jump_count < 0:
                self.y += (self._jump_count ** 2) / 2
            else:
                self.y -= (self._jump_count ** 2) / 2
            self._jump_count -= 1
        else:
            self.set_jump_status(False)
            self._jump_count = 8

    def set_jump_status(self, status):
        if status:
            self.is_jump = True
        else:
            self.is_jump = False

    def get_jump_status(self):
        return self.is_jump

    def get_metrics(self):
        return self.x, self.y, self.radius


class Obstacle:
    def __init__(self, position: tuple, dimensions: tuple, color: tuple):
        self.x, self.y = position
        self.width, self.height = dimensions
        self.color = color

        self._speed = 10

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x -= self._speed

    def get_x(self):
        return self.x

    def get_metrics(self):
        return self.x, self.y, self.width, self.height


class Text:
    def __init__(self, text: str, position: tuple, font_size: int = 10,
                 fg_color: tuple = BLACK, bg_color: tuple = WHITE):
        pg.font.init()
        self.text = text
        self.x, self.y = position
        self.font_size = font_size
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font = pg.font.Font('freesansbold.ttf', self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.fg_color, self.bg_color)

    def draw(self, screen):
        screen.blit(self.rendered_text, (self.x, self.y))


class Score(Text):
    """
    Game score class. Contains score incrementation method.
    """

    def __init__(self, position: tuple, font_size: int = 10, prefix: str = "Score: ",
                 fg_color: tuple = BLACK, bg_color: tuple = WHITE):
        self.points = 0
        self.prefix = prefix
        self.text = self.prefix + str(self.points)
        super().__init__(self.text, position, font_size, fg_color, bg_color)

    def increment_score(self):
        self.points += 1
        self.text = self.prefix + str(self.points)
        self.rendered_text = self.font.render(self.text, True, self.fg_color, self.bg_color)

    def get_points(self):
        return self.points


def main():
    size = (1000, 300)
    game = GameWindow(size)
    game.main_loop()


if __name__ == "__main__":
    main()
