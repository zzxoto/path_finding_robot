"""
Contains Global Settings and constants For Entire Module
Contains Standard Data Structure Implementaions
"""


from os import sys
import pygame
import random

pygame.init()
pygame.font.init()

Font = pygame.font.SysFont( None , 20)
    
SCREEN_SIZE = 800
MENU_HEIGHT = 50
GAME_SCREEN_HEIGHT = SCREEN_SIZE - MENU_HEIGHT

S_D_SIZE = 25#Standard size for the source and destination objects

MENU_PORTION = pygame.Rect(0, 0, SCREEN_SIZE, MENU_HEIGHT)
GAME_PORTION = pygame.Rect(0, MENU_HEIGHT, SCREEN_SIZE, GAME_SCREEN_HEIGHT)

screen = pygame.display.set_mode( [SCREEN_SIZE , SCREEN_SIZE] )



def blit( block ):
    if block:
        screen.blit( block.image , block.pos )


class Color:
    white = (250, 250, 250)
    black = (0 , 0 , 0)
    red = (250 ,0 , 0)
    green = ( 0, 255, 0 )
    yellow = (255, 255, 0)
    brown = (92, 64, 51),
    grey = ( 72, 72, 72)


class Stack:
    '''
    First In Last Out
    Provides Undo mechanism
    '''
    def __init__(self):
        self.st = []

    def push(self, item):
        self.st.append( item )
        return item

    def pop(self):
        popped = None
        if not self.isEmpty():
            popped = self.st.pop()
        return popped

    def peek( self ):
        if not self.isEmpty():
            return self.st[-1]

    def isEmpty( self ):
        return len( self.st ) == 0

    def iterable( self ):
        return self.st





