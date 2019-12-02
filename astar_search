#!/usr/bin/env python
"""Simple A* Example script

Filename: search.py
Author: James Casey
Date Created: 2019-12-02
Last Updated: 2019-12-02
"""

import click
import logging
import structlog
from structlog.stdlib import LoggerFactory
import pygame
import random
from enum import Enum
from pdb import set_trace

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
YELLOW = (255,255,0)

WIDTH=800
HEIGHT=600
SQUARE_SIZE = 20
MAX_X = int(WIDTH / SQUARE_SIZE) - 1
MAX_Y = int(HEIGHT / SQUARE_SIZE) - 1


def square_center(square):
    x = square[0]*SQUARE_SIZE + 1 + SQUARE_SIZE / 2
    y = square[1]*SQUARE_SIZE + 1 + SQUARE_SIZE / 2

    return (x,y)


def get_neighbors(square, clicked_squares=[], plus_only=False):
    debug("Square: ", square=square)
    neighbors = []

    for i in [square[0] - 1, square[0], square[0] + 1]:
        if i < 0 or i > MAX_X:
            continue
        for j in [square[1] - 1, square[1], square[1] + 1]:
            if j < 0 or j > MAX_Y:
                continue
            if i == square[0] and j == square[1]:
                continue

            if plus_only is True:
                if  i == square[0] - 1 and j !=  square[1]:
                    continue
                if  i == square[0] + 1 and j !=  square[1]:
                    continue

            # Deal with barriers
            if [i,j] in clicked_squares:
                continue

            neighbors.append([i,j])

    return neighbors


class PathNode:
    def __init__(self, parent=None, pos=None, start_square=None, end_square=None):
        debug("generating new node ", pos=pos)
        self.parent_node = parent
        self.pos = pos
        self.start_square = start_square
        self.end_square = end_square

        self.f = 0
        self.g = 0
        self.h = 0

        self.set_h()

    def set_h(self):
        self.h = ((self.end_square[0] - self.pos[0])
                  + (self.end_square[1] - self.pos[1]))

    def __repr__(self):
        return f"<PathNode: {self.pos}>"


def find_path(start_square, end_square, clicked_squares, plus_only=False):

    open_list = []
    closed_list = []

    open_list.append(PathNode(parent=None,
                              pos=start_square,
                              start_square=start_square,
                              end_square=end_square))

    searching = True
    while searching:
        # set_trace()
        debug("open_list: {} closed_list {}".format(len(open_list), len(closed_list)))

        if len(open_list) == 0:
            break

        open_list = sorted(open_list, key=lambda entry: -entry.g)
        q = open_list.pop()

        for neighbor in get_neighbors(q.pos, clicked_squares, plus_only=plus_only):

            node = PathNode(parent=q,
                            pos = neighbor,
                            start_square=start_square,
                            end_square=end_square)
            node.g = q.g + 1
            node.f = node.g + node.h

            if neighbor == end_square:
                searching = False
                break

            check_open = False
            for open_node in open_list:
                if node.pos == open_node.pos and open_node.f <= node.f:
                    check_open = True
                    break
            if check_open is True:
                continue

            check_closed = False
            for closed_node in closed_list:
                if node.pos == closed_node.pos and closed_node.f <= node.f:
                    check_closed = True
                    continue
            if check_closed is True:
                continue

            open_list.append(node)

        closed_list.append(q)

    # open_list = sorted(open_list, key=lambda entry: -entry.g)
    last = node

    best_path = []
    while True:
        if last.parent_node is None:
            break
        best_path.append(last.pos)
        last = last.parent_node
    return best_path


@click.command()
@click.option("-n", "--draw-neighbors", is_flag=True, default=False,
                help="Draw neighbors on click")
@click.option("-p", "--plus-only", is_flag=True, default=False,
                help="Set neighbors to only up/down and left/right")
@click.option("-v", "--verbose", is_flag=True, default=False,
              help="Show debuggging information")
def main(verbose, plus_only, draw_neighbors):

    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    pygame.init()
    pygame.font.init()
    # myfont = pygame.font.SysFont('couriernewbold', 32)

    gDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    # List fonts real quick
    # print(pygame.font.get_fonts())

    start_square = [1,1]
    end_square = [MAX_X-1,MAX_Y-1]
    clicked_squares = []
    path_squares = []
    neighbors = []

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    new_square = [int(x/SQUARE_SIZE),int(y/SQUARE_SIZE)]

                    if draw_neighbors is True:
                        neighbors = get_neighbors(new_square,
                                plus_only=plus_only)

                    if new_square == start_square or new_square == end_square:
                        continue

                    if new_square in clicked_squares:
                        clicked_squares.remove(new_square)
                    else:
                        clicked_squares.append(new_square)

                elif pygame.mouse.get_pressed() == (0,0,1):
                    path_squares = find_path(start_square, end_square,
                            clicked_squares, plus_only)
                    neighbors = []


        gDisplay.fill(BLACK)
        for i in range(1,int(WIDTH/SQUARE_SIZE)):
            x = SQUARE_SIZE*i
            pygame.draw.line(gDisplay, WHITE, (x,0), (x,HEIGHT),1)

        for i in range(1,int(HEIGHT/SQUARE_SIZE)):
            y = SQUARE_SIZE*i
            pygame.draw.line(gDisplay, WHITE, (0,y), (WIDTH,y),1)

        # Draw best path
        if path_squares is not None:
            last_square = start_square
            for square in path_squares[::-1]:
                x = square[0]*SQUARE_SIZE + 1
                y = square[1]*SQUARE_SIZE + 1
                pygame.draw.rect(gDisplay, YELLOW, pygame.Rect(x,y,SQUARE_SIZE - 1,
                    SQUARE_SIZE - 1))
                pygame.draw.line(gDisplay, RED,
                        (square_center(last_square)),
                        (square_center(square)), 2)
                last_square = square

        # Draw neighbors of clicked squares (if enabled)
        for square in neighbors:
            x = square[0]*SQUARE_SIZE + 1
            y = square[1]*SQUARE_SIZE + 1
            pygame.draw.rect(gDisplay, CYAN, pygame.Rect(x,y,SQUARE_SIZE - 1,
                SQUARE_SIZE - 1))

        # Draw clicked squares
        for square in clicked_squares:
            x = square[0]*SQUARE_SIZE + 1
            y = square[1]*SQUARE_SIZE + 1
            pygame.draw.rect(gDisplay, BLUE, pygame.Rect(x,y,SQUARE_SIZE - 1,
                SQUARE_SIZE - 1))

        # Draw Start Square
        x = start_square[0]*SQUARE_SIZE + 1
        y = start_square[1]*SQUARE_SIZE + 1
        pygame.draw.rect(gDisplay, GREEN, pygame.Rect(x,y,SQUARE_SIZE - 1,
            SQUARE_SIZE - 1))

        # Draw End Square
        x = end_square[0]*SQUARE_SIZE + 1
        y = end_square[1]*SQUARE_SIZE + 1
        pygame.draw.rect(gDisplay, RED, pygame.Rect(x,y,SQUARE_SIZE - 1,
            SQUARE_SIZE - 1))


        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
