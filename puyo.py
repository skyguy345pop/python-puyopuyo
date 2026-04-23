from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, puyoPuyo, pos, colour):
        self.puyoPuyo = puyoPuyo
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(puyoPuyo.puyoPuyo.sprite_group)
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        pg.draw.rect(self.image, colour, (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=8)
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.alive:
            self.kill()
    
    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
    
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.puyoPuyo.current]
        self.rect.topleft = pos * TILE_SIZE
    
    def update(self):
        self.is_alive()
        self.set_rect_pos()
    
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.puyoPuyo.puyoPuyo.field_array[y][x]):
            return False
        return True


class Puyo:
    def __init__(self, puyoPuyo, current=True):
        self.puyoPuyo = puyoPuyo
        self.shape = [(0, 0), (0, 1)]
        self.blocks = [Block(self, pos, random.choice(["orange", "blue", "purple", "red", "yellow", "green", "brown", "white"])) for pos in self.shape]
        self.landing = False
        self.current = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
    
    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == "down":
            self.landing = True
    
    def update(self):
        self.move(direction="down")