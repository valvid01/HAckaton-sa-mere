from random import randint

from Rogue_affichage import draw_rectangle

def generate_object(level, tableau):
    for room in level.rooms():
        x1, y1, x2, y2 = room[0][0], room[0][1], room[1][0], room[1][1]
        area = (y2-y1)*(x2-x1)
        N = randint(0, 1 + int(area/30))
        for i in range(N):
            x, y = randint(x1+1, x2-1), randint(y1+1, y2-1)
            while tableau[x, y] == ??:
                x, y = randint(x1+1, x2-1), randint(y1+1, y2-1)
            tableau[x, y] = ??