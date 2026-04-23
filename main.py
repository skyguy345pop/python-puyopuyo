from puyopuyo import Puyopuyo, Text
import sys
from settings import *

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Puyopuyo")
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.puyoPuyo = Puyopuyo(self)
        self.text = Text(self)

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)
    
    def update(self):
        self.puyoPuyo.update()
        self.clock.tick(FPS)
    
    def draw(self):
        self.screen.fill(color=BG_COLOUR)
        self.screen.fill(color=FIELD_COLOUR, rect=(0, 0, *FIELD_RES))
        self.puyoPuyo.draw()
        self.text.draw()
        pg.display.flip()
    
    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.puyoPuyo.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True
    
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    App().run()