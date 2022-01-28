import pygame as pg
from random import randint
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

import copy
from random import uniform

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

    def __init__(self, XSIZE, YSIZE, TAILLE_GRILLE):
        self.taille_grille = TAILLE_GRILLE
        self.forme = (XSIZE, YSIZE)
        NB_SALLES = TAILLE_GRILLE * TAILLE_GRILLE
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


    def build_rooms(self):
        L = []
        x_grid = self.forme[0] // self.taille_grille
        y_grid = self.forme[1] // self.taille_grille
        for i in range(self.taille_grille - 1):
            for j in range(self.taille_grille - 1):
                hg_x, hg_y = uniform(0, 1), uniform(0, 1)
                HG_X, HG_Y = (int((i + hg_x) * x_grid), int((j + hg_y) * y_grid))
                bd_x, bd_y = uniform(0, 1), uniform(0, 1)
                BD_X, BD_Y = (int((i + 0.5 + bd_x) * x_grid), int((j + 0.5 + bd_y) * y_grid))
                L.append(((HG_X, HG_Y), (BD_X, BD_Y)))
        self.rooms = L
        print(L)


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


# level = Level(30, 30, 6)
# level.build_rooms([((1, 1), (4, 4)), ((4, 9), (7, 12))])
# level.build_doors({(2, 4, 'S'): (0, 1, (5, 9, 'N')), (5, 9, 'N'): (1, 0, (2, 4, 'S'))})
# level.build_corridors()
# level.make_map()
# print(level.map)

level = Level(300, 300, 6)
level.build_doors({})
level.build_rooms()
level.make_map()
print(level.map)