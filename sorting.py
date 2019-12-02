#!/usr/bin/env python
"""Simple Sorting Script

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
HEIGHT=800
SQUARE_SIZE = 10
MAX_X = int(WIDTH / SQUARE_SIZE) - 1
MAX_Y = int(HEIGHT / SQUARE_SIZE) - 1


def quicksort(data, lo, hi):
    print("quicksort called")
    if lo < hi:
        p = partition(data, lo, hi)
        quicksort(data, lo, p-1)
        quicksort(data, p+1, hi)

def partition(data, lo, hi):
    pivot = data[hi]
    i = lo
    for j in range(lo, hi):
        if data[j] < pivot:
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[hi] = data[hi], data[i]
    return i


def insertion_sort(data):

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
def main(verbose, draw_grid):

    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    pygame.init()
    pygame.font.init()
    # myfont = pygame.font.SysFont('couriernewbold', 32)

    gDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    sort_i = 0
    data = list(range(1,MAX_X))
    random.shuffle(data)
    sort_type = 'insertion'
    # sort_type = 'quick'

    sorting = False
    running = True
    corou = insertion_sort(data)
    # corou = quicksort(data, 0, len(data)-1)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    sorting = False if sorting else True
                elif pygame.mouse.get_pressed() == (0,0,1):
                    random.shuffle(data)
                    sort_i = 0

        gDisplay.fill(BLACK)
        if draw_grid is True:

            for i in range(1,int(WIDTH/SQUARE_SIZE)):
                x = SQUARE_SIZE*i
                pygame.draw.line(gDisplay, WHITE, (x,0), (x,HEIGHT),1)

            for i in range(1,int(HEIGHT/SQUARE_SIZE)):
                y = SQUARE_SIZE*i
                pygame.draw.line(gDisplay, WHITE, (0,y), (WIDTH,y),1)

        if sorting is True:

            if sort_type == "insertion":
                sorting = corou.__next__()
            else:
                corou.__next__()


        for i, value in enumerate(data):
            for j in range(1,value):
                x = i*SQUARE_SIZE + 1
                y = (MAX_Y - j)*SQUARE_SIZE + 1
                pygame.draw.rect(gDisplay, CYAN, pygame.Rect(x,y,SQUARE_SIZE - 1,
                    SQUARE_SIZE - 1))




        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()


