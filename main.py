import pygame as pg
import random
from math import pi, sin, cos

G = 9.81


class Main:
    def __init__(self):
        pg.init()
        self.width, self.height = 500, 500
        self.display = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Маятники")
        self.clock = pg.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()


if __name__ == '__main__':
    simulation = Main()
    simulation.run()
