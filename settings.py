import pygame as pg

vec = pg.math.Vector2

FPS = 60
FIELD_COLOUR = (48, 39, 32)
BG_COLOUR = (24, 89, 117)

FONT_PATH = "LuckiestGuy-Regular.ttf"

ANIM_TIME_INTERVAL = 150
FAST_ANIM_TIME_INTERVAL = 15

TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES= WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)
MOVE_DIRECTIONS= {"left": vec(-1, 0), "right": vec(1, 0), "down": vec(0, 1)}