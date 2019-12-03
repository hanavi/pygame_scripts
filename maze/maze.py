#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Maze Generator

Filename: mazy.py
Author: James Casey
Date Created:
Last Updated:
"""

import click
import logging
import structlog
from structlog.stdlib import LoggerFactory
import pygame
import random
# import pdb

structlog.configure(logger_factory=LoggerFactory())
log = structlog.get_logger()

debug = log.debug
info = log.info
warning = log.warning
error = log.error

# Global stuff to make life easier
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

WIDTH=600
HEIGHT=600
SQUARE_SIZE = 30
MAX_X = int(WIDTH / SQUARE_SIZE) - 1
MAX_Y = int(HEIGHT / SQUARE_SIZE) - 1

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = [x,y]
        self.vert = False
        self.horz = False


def idx_to_grid(n):
    x = n %  MAX_Y
    y = int(n / MAX_X)
    return(x,y)


def get_neighbors(start_square, visited=[]):
    neighbors = []

    for i in [start_square.x - 1, start_square.x, start_square.x + 1]:
        if i < 0 or i > MAX_X:
            continue
        for j in [start_square.y - 1, start_square.y, start_square.y + 1]:
            if j < 0 or j > MAX_Y:
                continue
            if i == start_square.x and j == start_square.y:
                continue
            if  i == start_square.x - 1 and j !=  start_square.y:
                continue
            if  i == start_square.x + 1 and j !=  start_square.y:
                continue

            # Deal with barriers
            found = False
            for square in visited:
                if square.pos == [i,j]:
                    found = True
                    break
            if found:
                continue

            neighbors.append(Square(i,j))

    return neighbors


@click.command()
@click.option("-d", "--debug", "dbg", is_flag=True, default=False,
              help="Show debugging information")
def main(dbg):
    """ Main code block """

    if dbg is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    pygame.init()
    clock = pygame.time.Clock()
    gDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

    start_square = Square(0,0)

    visited = [start_square]
    path = [start_square]

    c = 0
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gDisplay.fill(WHITE)

        for i in range(0, int(WIDTH/SQUARE_SIZE)):
            x = SQUARE_SIZE*i
            pygame.draw.line(gDisplay, BLACK, (x, 0), (x, HEIGHT), 2)

        for i in range(0, int(HEIGHT/SQUARE_SIZE)):
            y = SQUARE_SIZE*i
            pygame.draw.line(gDisplay, BLACK, (0, y), (WIDTH, y), 2)

        total_squares = (MAX_X + 1) * (MAX_Y + 1)

        if len(visited) < total_squares:
            # pdb.set_trace()

            while True:
                last = path.pop()
                neighbors = get_neighbors(last, visited)
                if len(neighbors) == 0:
                    continue
                random.shuffle(neighbors)
                neighbor = neighbors.pop()

                if neighbor.x == last.x:
                    if neighbor.y == last.y + 1:
                        last.vert = True
                    if neighbor.y == last.y - 1:
                        neighbor.vert = True

                if neighbor.y == last.y:
                    if neighbor.x == last.x + 1:
                        last.horz = True
                    if neighbor.x == last.x - 1:
                        neighbor.horz = True

                path.append(last)
                path.append(neighbor)
                visited.append(neighbor)
                break

        for square in visited:

            x = square.x*SQUARE_SIZE + 2
            y = square.y*SQUARE_SIZE + 2

            x_step = 2
            y_step = 2

            if square.vert is True:
                y_step = 0

            if square.horz is True:
                x_step = 0

            pygame.draw.rect(gDisplay, CYAN, pygame.Rect(x,y,SQUARE_SIZE - x_step, SQUARE_SIZE - y_step))

        pygame.display.update()
        clock.tick(15)

        c += 1


if __name__ == "__main__":
    main()

