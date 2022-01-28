from Hachathon.Rogue_affichage import BROWN, GREY
from Hachathon.Rogue_main import BLACK, PIXEL_SIZE, WHITE


map = level.make_map()

def draw_square(screen, j, i, size, color):
    rect = pg.Rect(i*PIXEL_SIZE, j*PIXEL_SIZE, size, size)
    # appel à la méthode draw.rect()
    pg.draw.rect(screen, color, rect)

a, b = np.shape(map)

for i in range(b):
    for j in range(a):
        if map[i,j] == 0:
            color = BLACK
        if map[i,j] == 1:
            color = GREY
        if map[i,j] == GREY:
            color = BLACK
        if map[i,j] == 4:
            color = BROWN
        draw_square(screen, i, j, PIXEL_SIZE, color)