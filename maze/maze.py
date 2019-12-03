#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Maze Generator

Filename: maze.py
Author: James Casey
Date Created: 2019-12-02
Last Updated: 2019-12-03
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
SQUARE_SIZE = 20
MAX_X = int(WIDTH / SQUARE_SIZE) - 1
MAX_Y = int(HEIGHT / SQUARE_SIZE) - 1

class Square:
    """ Store unit path information. """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.vert = False
        self.horz = False


def idx_to_grid(n):
    """ Convert between array and grid points. (Used in testing) """

    x = n %  MAX_Y
    y = int(n / MAX_X)
    return(x, y)


def get_neighbors(start_square, visited=[]):
    """ Get the valid neighbors of a given square. """
    neighbors = []

    # loop over possible x values
    for i in [start_square.x - 1, start_square.x, start_square.x + 1]:

        # drop neighbors outside of our region of interest
        if i < 0 or i > MAX_X:
            continue

        # loop over possible y values
        for j in [start_square.y - 1, start_square.y, start_square.y + 1]:

            # drop neighbors outside of our region of interest
            if j < 0 or j > MAX_Y:
                continue

            # Ignore ourself
            if i == start_square.x and j == start_square.y:
                continue

            # Ignore corner pieces
            if  i == start_square.x - 1 and j !=  start_square.y:
                continue
            if  i == start_square.x + 1 and j !=  start_square.y:
                continue

            # Deal with barriers
            found = False
            for square in visited:
                if square.pos == [i, j]:
                    found = True
                    break
            if found:
                continue

            neighbors.append(Square(i, j))

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

    # Basic initialization
    pygame.init()
    clock = pygame.time.Clock()
    gDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

    # Start and end points
    start_square = Square(0, 0)
    end_square = Square(MAX_X, MAX_Y)

    # Keep track of everything
    visited = [start_square]
    path = [start_square]
    total_squares = (MAX_X + 1) * (MAX_Y + 1)

    # The game loop
    running = True
    while running:

        # Check for interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Set the initial background
        gDisplay.fill(WHITE)

        # Draw the grid
        for i in range(0, int(WIDTH/SQUARE_SIZE)):
            x = SQUARE_SIZE*i
            pygame.draw.line(gDisplay, BLACK, (x, 0), (x, HEIGHT), 2)

        for i in range(0, int(HEIGHT/SQUARE_SIZE)):
            y = SQUARE_SIZE*i
            pygame.draw.line(gDisplay, BLACK, (0, y), (WIDTH, y), 2)

        # continue running until we've been to every square
        if len(visited) < total_squares:

            # loop until we've successfully added a new square to the path
            while True:

                # get the last square visited and it's neighbor
                last = path.pop()
                neighbors = get_neighbors(last, visited)

                # Backup if there are no neighbors left for the square
                if len(neighbors) == 0:
                    continue

                # Pick a neighbor square at random
                random.shuffle(neighbors)
                neighbor = neighbors.pop()

                # set the direction of travel for the borders
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

                # add the last visited back to the path along with the new
                # square
                path.append(last)
                path.append(neighbor)

                # mark the new square as now visited
                visited.append(neighbor)

                break

        # Draw all of the visited squares
        for square in visited:

            x = square.x*SQUARE_SIZE + 2
            y = square.y*SQUARE_SIZE + 2

            # Deal with the borders
            x_step = 2
            y_step = 2

            if square.vert is True:
                y_step = 0

            if square.horz is True:
                x_step = 0

            pygame.draw.rect(gDisplay, CYAN,
                    pygame.Rect(x, y,
                        SQUARE_SIZE - x_step,
                        SQUARE_SIZE - y_step))

        # Draw the start square green
        x = start_square.x*SQUARE_SIZE + 2
        y = start_square.y*SQUARE_SIZE + 2

        # Deal with the borders
        x_step = 2
        y_step = 2

        if start_square.vert is True:
            y_step = 0
        if start_square.horz is True:
            x_step = 0

        pygame.draw.rect(gDisplay, GREEN,
                pygame.Rect(x, y, SQUARE_SIZE - x_step, SQUARE_SIZE - y_step))

        # Draw the finish red
        x = end_square.x*SQUARE_SIZE + 2
        y = end_square.y*SQUARE_SIZE + 2

        # Deal with the borders
        x_step = 2
        y_step = 2

        if end_square.vert is True:
            y_step = 0
        if end_square.horz is True:
            x_step = 0

        pygame.draw.rect(gDisplay, RED,
                pygame.Rect(x, y, SQUARE_SIZE - x_step, SQUARE_SIZE - y_step))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
