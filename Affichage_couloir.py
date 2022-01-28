import pygame as pg
import numpy as np
import copy
from random import randint

from Rogue_main import PIXEL_SIZE

def print_corridor(screen, character, level):
    if(level.map[character.x,character.y] == 4):
        d = character.direction
        if(d == 'N'):
            if(level.map[character.x, character.y-1]==1):
                a,b,c = level.doors[character.x, character.y, 'S']
                draw_room(screen,level.rooms[a])
            elif(level.map[character.x, character.y-1]==2):
                draw_rectangle(screen, character.x, character.y-1, PIXEL_SIZE, PIXEL_SIZE, GREY)
        if(d == 'S'):
            if(level.map[character.x, character.y+1]==1):
                a,b,c = level.doors[character.x, character.y, 'N']
                draw_room(screen,level.rooms[a])
            elif(level.map[character.x, character.y+1]==2):
                draw_rectangle(screen, character.x, character.y+1, PIXEL_SIZE, PIXEL_SIZE, GREY)
        if(d == 'O'):
            if(level.map[character.x-1, character.y]==1):
                a,b,c = level.doors[character.x, character.y, 'E']
                draw_room(screen, level.rooms[a])
            elif(level.map[character.x-1, character.y]==2):
                draw_rectangle(screen, character.x-1, character.y, PIXEL_SIZE, PIXEL_SIZE, GREY)
        if(d == 'E'):
            if(level.map[character.x+1, character.y]==1):
                a,b,c = level.doors[character.x, character.y, 'S']
                draw_room(screen, level.rooms[a])
            elif(level.map[character.x+1, character.y]==2):
                draw_rectangle(screen, character.x+1, character.y, PIXEL_SIZE, PIXEL_SIZE, GREY)
    elif(level.map[character.x,character.y] == 2):
        if(level.map[character.x-1,character.y] == 2):
            draw_rectangle(screen, character.x-1, character.y, PIXEL_SIZE, PIXEL_SIZE, GREY)
        if(level.map[character.x+1,character.y] == 2):
            draw_rectangle(screen, character.x+1, character.y, PIXEL_SIZE, PIXEL_SIZE, GREY)
        if(level.map[character.x,character.y-1] == 2):
            draw_rectangle(screen, character.x, character.y-1, PIXEL_SIZE, PIXEL_SIZE, GREY)
        if(level.map[character.x,character.y+1] == 2):
            draw_rectangle(screen, character.x, character.y+1, PIXEL_SIZE, PIXEL_SIZE, GREY)







