import pygame as pg
from enum import Enum
from colors import *


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class GameWindow:
    def __init__(self, size):
        self.size = size
        self.screen = pg.display.set_mode(self.size)
        self.players = [Player(50, 50, 10, 10, RED), Player(100, 100, 10, 15, GREEN)]

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
                if keys[pg.K_LEFT]:
                    player.move(Direction.LEFT)
                if keys[pg.K_RIGHT]:
                    player.move(Direction.RIGHT)
                if keys[pg.K_UP]:
                    player.move(Direction.UP)
                if keys[pg.K_DOWN]:
                    player.move(Direction.DOWN)

            self.screen.fill((255, 255, 255))

            # Update all players
            for player in self.players:
                player.draw(self.screen)

            pg.display.update()


class Player:
    def __init__(self, x, y, radius, speed, color):
        self.x, self.y = x, y
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
