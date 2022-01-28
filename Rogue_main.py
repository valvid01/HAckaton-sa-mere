from typing import Sized
import pygame as pg
import numpy as np
import copy
from random import randint

SIZE = 50
PIXEL_SIZE = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50,50,50)
BROWN = (165, 42, 42)
RED = (255, 0, 0)

class Character:
    def __init__ (self, x, y, inventory = {}, health=12,strength = 16, armor=5, gold=0):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.health = health
        self.strength = strength
        self.armor = armor
        self.gold = gold
        self.direction = 'N'
    def __repr__(self):
        return f"Position : x = {self.x}, y = {self.y}"
        
def make_straight_corridor(v, u):
    corridor = [v]
    x_dist = u[0] - v[0]
    y_dist = u[1] - v[1]
    if y_dist == 0:
        x_sign = int(x_dist/np.abs(x_dist))
        while u[0] - corridor[-1][0] != 0:
            corridor.append((corridor[-1][0] + x_sign, u[1]))
    if x_dist == 0:
        y_sign = int(y_dist/np.abs(y_dist))
        while u[1] - corridor[-1][1] != 0:
            corridor.append((u[0], corridor[-1][1] + y_sign))
    return corridor[1:]


def make_corridor(porte_1, porte_2):
    corridor = []
    x_dist = porte_1[0] - porte_2[0]
    y_dist = porte_1[1] - porte_2[1]
    if porte_1[2] == 'N':
        corridor.append((porte_1[0], porte_1[1] -1))
        y_dist -= 2
    if porte_1[2] == 'S':
        corridor.append((porte_1[0], porte_1[1] + 1))
        y_dist += 2
    if porte_1[2] == 'E':
        corridor.append((porte_1[0] + 1, porte_1[1]))
        x_dist += 2
    if porte_1[2] == 'W':
        corridor.append((porte_1[0] - 1, porte_1[1]))
        x_dist -= 2
    corridor += make_straight_corridor(corridor[-1], (corridor[-1][0] - x_dist, corridor[-1][1]))
    corridor += make_straight_corridor(corridor[-1], (corridor[-1][0], corridor[-1][1] - y_dist))
    return corridor


class Level():

    def __init__(self, XSIZE, YSIZE, NB_SALLES):
        # le terrain est un numpy array de shape (XSIZE, YSIZE) contenant des entiers : 0, 1, 2...
        # 0 : vide (pas jouable, bloque le joueur)
        # 1 : sol des salles (jouable, le joueur décrouve toute la salle d'un seul coup)
        # 2 : couloir (jouable, le joueur découvre le couloir un bloc devant lui)
        # 3 : objets (jouable, le joueur les récupère en marchant dessus)
        # 4 : portes (jouable)
        # 5 : méchants (le joueur peut leur marcher dessus,
        #     les méchants se déplacent vers le joueur)
        self.map = np.zeros((XSIZE, YSIZE), dtype=int)

        # les salles sont une liste de tuples de tuples [((3, 5), (5, 7)), ...]
        self.rooms = []

        # les objets sont un dictionnaire : {(3, 40): 'potion'}
        self.objects = {}

        # les couloirs sont une liste des listes de tous les points (tuples) du couloir
        self.corridors = [[[] for j in range(NB_SALLES)] for i in range(NB_SALLES)]

        # les portes sont un dictionnaires : {(x_porte, y_porte, 'S'):
        # (salle_d'entrée, salle_de_sortie, (x_porte_2, y_porte_2, 'N')), ...}
        self.doors = {}
    

    def build_corridors(self):
        for door in self.doors.keys():
            if self.corridors[self.doors[door][1]][self.doors[door][0]] == []:
                self.corridors[self.doors[door][0]][self.doors[door][1]] = make_corridor(door, self.doors[door][2])
            else:
                self.corridors[self.doors[door][0]][self.doors[door][1]] = copy.deepcopy(self.corridors[self.doors[door][1]][self.doors[door][0]])
    

    def build_rooms(self, lst):
        self.rooms = lst


    def build_doors(self, dict):
        self.doors = dict
    

    def make_map(self):
        # construction des salles
        print(self.rooms)
        for room in self.rooms:
            width = np.abs(room[1][0] - room[0][0]) - 1
            height = np.abs(room[0][1] - room[1][1]) - 1
            print(height, width)
            for i in range(height):
                for j in range(width):
                    self.map[room[0][0] + 1 + j, room[0][1] + 1 + i] = 1
        for door in self.doors.keys():
            print(door)
            self.map[door[0], door[1]] = 4
        for ligne in self.corridors:
            for corridor in ligne:
                if corridor:
                    print(corridor)
                    for point in corridor:
                        self.map[point[0], point[1]] = 2

level = Level(SIZE, SIZE, 6)
level.build_rooms([((1, 1), (15, 15)), ((12, 20), (30, 38))])
level.build_doors({(10, 15, 'S'): (0, 1, (14, 20, 'N')), (14, 20, 'N'): (1, 0, (10, 15, 'S'))})
level.build_corridors()
map = level.make_map()

def draw_rectangle(screen, i, j, height, length, color):
    rect = pg.Rect(i*PIXEL_SIZE, j*PIXEL_SIZE, height, length)
    # appel à la méthode draw.rect()
    pg.draw.rect(screen, color, rect)

def draw_room(screen, room):
    x1, y1, x2, y2 = room[0][0], room[0][1], room[1][0], room[1][1]
    height, length = (y2-y1+1)*PIXEL_SIZE, (x2-x1+1)*PIXEL_SIZE
    draw_rectangle(screen, x1, y1, height, length, WHITE)
    draw_rectangle(screen, x1+1, y1+1, height-2*PIXEL_SIZE, length-2*PIXEL_SIZE, GREY)

def draw_corridor(screen, corridor):
    for i, j in corridor:
        draw_rectangle(screen, i, j, PIXEL_SIZE, PIXEL_SIZE, GREY)

def draw_door(screen, door):
    draw_rectangle(screen, door[0], door[1], PIXEL_SIZE, PIXEL_SIZE, BROWN)

def draw_level(screen, level):
    for room in level.rooms:
        draw_room(screen, room)
    for line in level.corridors:
        for corridor in line:
            if corridor != []:
                draw_corridor(screen, corridor)
    for door in level.doors:
        draw_door(screen, door)

def move_character(screen, character, a = 0, b = 0, first = False):
    if first :
        x, y = character.x, character.y
        draw_rectangle(screen, x, y, PIXEL_SIZE, PIXEL_SIZE, RED)
    else :
        x, y = character.x, character.y
        draw_rectangle(screen, x, y, PIXEL_SIZE, PIXEL_SIZE, RED)
        draw_rectangle(screen, a, b, PIXEL_SIZE, PIXEL_SIZE, GREY)

start_room = level.rooms[0]
x1, y1, x2, y2 = start_room[0][0], start_room[0][1], start_room[1][0], start_room[1][1]
x, y = (x2+x1)//2, (y2+y1)//2
character = Character(x, y)

pg.init()
screen = pg.display.set_mode((SIZE*PIXEL_SIZE, SIZE*PIXEL_SIZE))

screen.fill(BLACK)
print(f"{character.x =}, {character.y =}")
draw_level(screen, level)
move_character(screen, character, first = True)
pg.display.update()

running = True
while running :
    
    events = pg.event.get()
    a = sum(event.type == pg.KEYDOWN for event in events)
    while a == 0:
        events = pg.event.get()
        a = sum(event.type == pg.KEYDOWN for event in events)
    

    for event in events:

        a, b = character.x, character.y

        if event.type == pg.QUIT:
            running = False
        
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                running = False
            
            elif (event.key == pg.K_UP) and (level.map[character.x, character.y -1] != 0):
                character.y -= 1
                character.direction = 'N'
                move_character(screen, character, a, b)

            elif event.key == pg.K_DOWN and (level.map[character.x, character.y +1] != 0):
                character.y += 1
                character.direction = 'S'
                move_character(screen, character, a, b)

            elif event.key == pg.K_LEFT and (level.map[character.x-1, character.y] != 0):
                character.x -= 1
                character.direction = 'O'
                move_character(screen, character, a, b)

            elif (event.key == pg.K_RIGHT) and (level.map[character.x+1, character.y] != 0):
                character.x += 1
                character.direction = 'E'
                move_character(screen, character, a, b)

    pg.display.update()
