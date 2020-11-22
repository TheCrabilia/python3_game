import pygame as pg
from colors import *
from enums import *


class GameWindow:
    def __init__(self, size: tuple):
        self.height, self.width = size
        self.screen = pg.display.set_mode((self.height, self.width))
        self.players = [Player(position=(50, 50), radius=10, color=RED)]

    def main_loop(self):
        finished = False
        while not finished:
            pg.time.delay(100)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

            # Move events for all players
            for player in self.players:
                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT] and player.x > player.radius:
                    player.move(Direction.LEFT)
                if keys[pg.K_RIGHT] and player.x < (self.width - player.radius):
                    player.move(Direction.RIGHT)
                if keys[pg.K_UP] and player.y > player.radius:
                    player.move(Direction.UP)
                if keys[pg.K_DOWN] and player.y < (self.height - player.radius):
                    player.move(Direction.DOWN)

            self.screen.fill((255, 255, 255))

            # Update all players
            for player in self.players:
                player.draw(self.screen)

            pg.display.update()

    def get_height(self):
        return self.height

    def git_width(self):
        return self.width


class Player:
    def __init__(self, position: tuple, radius: int, color: tuple, speed: int = 10):
        self.x, self.y = position
        self.radius = radius
        self.speed = speed
        self.color = color

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, direction):
        if direction == Direction.LEFT:
            self.x -= self.speed
        if direction == Direction.RIGHT:
            self.x += self.speed
        if direction == Direction.UP:
            self.y -= self.speed
        if direction == Direction.DOWN:
            self.y += self.speed


def main():
    size = (1000, 1000)
    game = GameWindow(size)
    game.main_loop()


if __name__ == "__main__":
    main()
