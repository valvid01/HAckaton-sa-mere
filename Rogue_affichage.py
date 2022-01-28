import pygame as pg
import numpy as np

SIZE = 30
PIXEL_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50,50,50)
BROWN = (165, 42, 42)

def draw_rectangle(screen, i, j, height, length, color):
    rect = pg.Rect(i*PIXEL_SIZE, j*PIXEL_SIZE, height, length)
    # appel à la méthode draw.rect()
    pg.draw.rect(screen, color, rect)

def draw_room(screen, room):
    x1, y1, x2, y2 = room[0][0], room[0][1], room[1][0], room[1][1]
    height, length = (y2-y1)*PIXEL_SIZE, (x2-x1)*PIXEL_SIZE
    draw_rectangle(screen, x1, y1, height, length, WHITE)
    draw_rectangle(screen, x1+1, y1+1, height-2, length-2, GREY)

def draw_corridor(screen, corridor):
    for i, j in corridor:
        draw_rectangle(screen, i, j, PIXEL_SIZE, PIXEL_SIZE, GREY)

def draw_door(screen, door):
    draw_rectangle(screen, door[0], door[1], PIXEL_SIZE, PIXEL_SIZE, BROWN)

def draw_level(screen, level):
    for room in level.rooms():
        draw_room(screen, room)
    for corridor in level.corridor():
        draw_corridor(screen, corridor)
    for door in level.doors():
        draw_door(screen, door)

start_room = level.rooms[0]
x1, y1, x2, y2 = start_room[0][0], start_room[0][1], start_room[1][0], start_room[1][1]
x, y = (x2-x1)//2, (y2-y1)//2
character = Character(x, y)

pg.init()
screen = pg.display.set_mode((SIZE*PIXEL_SIZE, SIZE*PIXEL_SIZE))

screen.fill(BLACK)
draw_level(screen, level)
pg.display.update()

running = True
while running :
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                running = False
            
            elif event.key == pg.K_UP:
                character.x

            elif event.key == pg.K_DOWN:
                if direction != (0, -1):
                    direction = (0, 1)
                    accept = False
            elif event.key == pg.K_LEFT:
                if direction != (1, 0):
                    direction = (-1, 0)
                    accept = False
            elif event.key == pg.K_RIGHT:
                if direction != (-1, 0):
                    direction = (1, 0)
                    accept = False