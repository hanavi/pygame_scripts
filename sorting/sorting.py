#!/usr/bin/env python
"""Simple Sorting Script

Filename: search.py
Author: James Casey
Date Created: 2019-12-02
Last Updated: 2019-12-03

This script is designed to visualize various sorting algorithms.  The problem
turns out not to be implementing the algorithm for the most part, but in
implementing it in such a way as it can be visualized.  There are probably
better ways to visualize it than using pygame as well, but I am just doing this
for fun and to play a little with pygame, so it is what it is!
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
HEIGHT=800
SQUARE_SIZE = 10
MAX_X = int(WIDTH / SQUARE_SIZE) - 1
MAX_Y = int(HEIGHT / SQUARE_SIZE) - 1


def quicksort(data, lo, hi):
    """ Quick Sort.

    In order to visualize the sorting, we have to do some weird stuff with
    yeilding....
    """

    if lo < hi:
        p = partition(data, lo, hi)

        stat = None
        while stat is None:
            stat = p.__next__()
            yield True
        p = stat

        c1 = quicksort(data, lo, p-1)
        c2 = quicksort(data, p+1, hi)

        stat = True
        while stat:
            stat = c1.__next__()
            yield True

        stat = True
        while stat:
            stat = c2.__next__()
            yield True
    yield False

def partition(data, lo, hi):
    """ Partitioning for Quick Sort.  """
    pivot = data[hi]
    i = lo
    for j in range(lo, hi):
        if data[j] < pivot:
            data[i], data[j] = data[j], data[i]
            i += 1
            yield None
    data[i], data[hi] = data[hi], data[i]
    yield i


def insertion_sort(data):
    """ Insertion Sort.

    In order to visualize the sorting, we have to do some weird stuff with
    yeilding....
    """

    i = 0
    while i < len(data):
        j = i
        while j > 0 and data[j-1] > data[j]:
            data[j],data[j-1] = data[j-1],data[j]
            j -= 1
            yield True
        i += 1

    yield False


@click.command()
@click.option("-v", "--verbose", is_flag=True, default=False,
              help="Show debuggging information")
@click.option("-g", "--draw-grid", is_flag=True, default=False,
                help="Draw Base Grid")
@click.option("-i", "--insertion", is_flag=True, default=False,
                help="Run Insertion Sort (Default)")
@click.option("-q", "--quick", is_flag=True, default=False,
                help="Run Quick Sort")
def main(verbose, draw_grid, insertion, quick):

    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # initialization/setup
    pygame.init()
    pygame.font.init()

    gDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    # Generate a list of data and randomize it
    data = list(range(1,MAX_X))
    random.shuffle(data)


    # set the sort function
    if quick is True:
        corou = quicksort(data, 0, len(data)-1)
    else:
        corou = insertion_sort(data)

    sorting = False
    running = True
    while running:

        # handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    sorting = False if sorting else True
                elif pygame.mouse.get_pressed() == (0,0,1):
                    random.shuffle(data)
                    if quick is True:
                        corou = quicksort(data, 0, len(data)-1)
                    else:
                        corou = insertion_sort(data)

        gDisplay.fill(BLACK)

        # Draw the grid
        if draw_grid is True:

            for i in range(1,int(WIDTH/SQUARE_SIZE)):
                x = SQUARE_SIZE*i
                pygame.draw.line(gDisplay, WHITE, (x,0), (x,HEIGHT),1)

            for i in range(1,int(HEIGHT/SQUARE_SIZE)):
                y = SQUARE_SIZE*i
                pygame.draw.line(gDisplay, WHITE, (0,y), (WIDTH,y),1)

        # Don't run unless we've clicked to run
        if sorting is True:
            sorting = corou.__next__()

        # Draw the data
        for i, value in enumerate(data):
            for j in range(1,value):
                x = i*SQUARE_SIZE + 1
                y = (MAX_Y - j)*SQUARE_SIZE + 1
                pygame.draw.rect(gDisplay, CYAN,
                        pygame.Rect(x,y,SQUARE_SIZE - 1, SQUARE_SIZE - 1))

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
