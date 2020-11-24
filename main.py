import pygame as pg
from colors import *


class GameWindow:
    """
    Game window class. Contains main game loop.
    """
    def __init__(self, size: tuple):
        self.width, self.height = size
        self.screen = pg.display.set_mode((self.width, self.height))

        # Objects that are drawn on the screen
        self.player = Player(position=(200, self.height - 20), radius=10, color=RED)
        self.score_widget = Score(position=(700, 20), font_size=32)
        self.obstacles = [Obstacle(position=(50, 50), dimensions=(70, 70), color=GREEN)]

    def main_loop(self):
        """
        Main game loop. Processes pressed keys events, calls object update method.
        """
        # Set clock (FPS)
        clock = pg.time.Clock()
        fps = 30

        # Initialize pygame
        pg.init()

        finished = False

        while not finished:
            clock.tick(fps)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

            keys = pg.key.get_pressed()

            if not self.player.is_jump:
                if keys[pg.K_SPACE]:
                    self.player.is_jump = True
            else:
                self.player.jump()

            self.screen.fill(WHITE)
            self.update_objects()
            pg.display.update()

    def update_objects(self):
        """
        Updates all objects on the screen.
        """
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.player.draw(self.screen)
        self.score_widget.draw(self.screen)


class Player:
    """
    Player class. Draws player on the main game window, realizes player mechanic - jump.
    """
    # Jump status class variable (available outside the class)
    is_jump = False

    def __init__(self, position: tuple, radius: int, color: tuple, speed: int = 10):
        self.x, self.y = position
        self.radius = radius
        self.speed = speed
        self.color = color

        # Jump mechanic variable
        self._jump_count = 10

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def jump(self):
        if self._jump_count >= -10:
            if self._jump_count < 0:
                self.y += (self._jump_count ** 2) / 2
            else:
                self.y -= (self._jump_count ** 2) / 2
            self._jump_count -= 1
        else:
            self.is_jump = False
            self._jump_count = 10


class Obstacle:
    def __init__(self, position: tuple, dimensions: tuple, color: tuple):
        self.x, self.y = position
        self.width, self.height = dimensions
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


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
        self.score = 0
        self.prefix = prefix
        self.text = self.prefix + str(self.score)
        super().__init__(self.text, position, font_size, fg_color, bg_color)

    def increment_score(self):
        self.score += 1
        self.text = self.prefix + str(self.score)
        self.rendered_text = self.font.render(self.text, True, self.fg_color, self.bg_color)


def main():
    size = (1000, 300)
    game = GameWindow(size)
    game.main_loop()


if __name__ == "__main__":
    main()
