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
        self.h = ((self.end_square.x - self.pos.x)
                  + (self.end_square.y - self.pos.y))

    def __repr__(self):
        return f"<PathNode: {self.pos}>"


def find_path(start_square, end_square, clicked_squares):

    open_list = []
    closed_list = []

    open_list.append(PathNode(parent=None,
                              pos=start_square,
                              start_square=start_square,
                              end_square=end_square))

    searching = True
    while searching:

        if len(open_list) == 0:
            break

        open_list = sorted(open_list, key=lambda entry: -entry.g)
        q = open_list.pop()

        for neighbor in get_neighbors(Square(q.pos.x,q.pos.y), clicked_squares):

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

    last = node

    best_path = []
    while True:
        if last.parent_node is None:
            break
        best_path.append(last.pos)
        last = last.parent_node
    return best_path


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
    end_square = Square(MAX_X,MAX_Y)

    visited = [start_square]
    path = [start_square]
    path_squares = []

    c = 0
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (0,0,1):
                    path_squares = find_path(start_square, end_square, path)

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

        x = start_square.x*SQUARE_SIZE + 2
        y = start_square.y*SQUARE_SIZE + 2

        x_step = 2
        y_step = 2

        if start_square.vert is True:
            y_step = 0
        if start_square.horz is True:
            x_step = 0

        pygame.draw.rect(gDisplay, GREEN, pygame.Rect(x,y,SQUARE_SIZE - x_step, SQUARE_SIZE - y_step))

        x = end_square.x*SQUARE_SIZE + 2
        y = end_square.y*SQUARE_SIZE + 2

        x_step = 2
        y_step = 2

        if end_square.vert is True:
            y_step = 0
        if end_square.horz is True:
            x_step = 0

        pygame.draw.rect(gDisplay, RED, pygame.Rect(x,y,SQUARE_SIZE - x_step, SQUARE_SIZE - y_step))

        pygame.display.update()
        clock.tick(30)

        c += 1


if __name__ == "__main__":
    main()

