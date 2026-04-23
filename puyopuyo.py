from settings import *
from puyo import Puyo
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
    
    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02), text = "PUYO PUYO", fgcolor="white", size=TILE_SIZE * 1.4, bgcolor="black")
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22), text = "next", fgcolor="orange", size=TILE_SIZE * 1.25, bgcolor="black")
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67), text = "score", fgcolor="orange", size=TILE_SIZE * 1.25, bgcolor="black")
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8), text = f"{self.app.puyoPuyo.score}", fgcolor="white", size=TILE_SIZE * 1.6)
        

class Puyopuyo:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.puyopuyo = Puyo(self)
        self.next_puyo = Puyo(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
    
    def find_groups(self):
        """Find connected groups of 4+ puyos of the same color."""
        visited = [[False] * FIELD_W for _ in range(FIELD_H)]
        groups = []

        for y in range(FIELD_H):
            for x in range(FIELD_W):
                block = self.field_array[y][x]
                if block and not visited[y][x]:
                    color = block.image.get_at((TILE_SIZE // 2, TILE_SIZE // 2))
                    stack = [(x, y)]
                    group = []

                    while stack:
                        cx, cy = stack.pop()
                        if not (0 <= cx < FIELD_W and 0 <= cy < FIELD_H):
                            continue
                        current = self.field_array[cy][cx]
                        if not current or visited[cy][cx]:
                            continue
                        this_color = current.image.get_at((TILE_SIZE // 2, TILE_SIZE // 2))
                        if this_color != color:
                            continue
                        visited[cy][cx] = True
                        group.append((cx, cy))
                        stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])

                    if len(group) >= 4:
                        groups.append(group)
        return groups


    def clear_groups(self, groups):
        """Remove groups from board and mark sprites dead."""
        cleared = 0
        for group in groups:
            cleared += len(group)
            for (x, y) in group:
                block = self.field_array[y][x]
                if block:
                    block.alive = False
                self.field_array[y][x] = 0
        return cleared


    def apply_gravity(self):
        """Make puyos fall down after clears."""
        for x in range(FIELD_W):
            column = [self.field_array[y][x] for y in range(FIELD_H) if self.field_array[y][x]]
            for y in range(FIELD_H):
                self.field_array[y][x] = 0
            for i, block in enumerate(reversed(column)):
                new_y = FIELD_H - 1 - i
                self.field_array[new_y][x] = block
                block.pos = pg.math.Vector2(x, new_y)

    def put_puyo_blocks_in_array(self):
        for block in self.puyopuyo.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range (FIELD_W)] for y in range(FIELD_H)]
    
    def is_game_over(self):
        if self.puyopuyo.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_puyo_landing(self):
        if self.puyopuyo.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                # Add landed puyo blocks to field
                self.put_puyo_blocks_in_array()

                # --- NEW: Check for color matches ---
                while True:
                    groups = self.find_groups()
                    if not groups:
                        break
                    cleared = self.clear_groups(groups)
                    self.apply_gravity()
                    self.score += cleared * 10  # adjust scoring as you like

                # --- Spawn next pair ---
                self.next_puyo.current = True
                self.puyopuyo = self.next_puyo
                self.next_puyo = Puyo(self, current=False)
    
    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.puyopuyo.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.puyopuyo.move(direction="right")
        elif pressed_key == pg.K_UP:
            self.puyopuyo.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, "black", (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.puyopuyo.update()
            self.check_puyo_landing()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)