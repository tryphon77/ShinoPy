from object import *
from tsprite import *

from res.hostage_data import *


def init_object():
    print 'init hostage'
    self = allocate_object()
    self.status = ACTIVE

    self.x = 352
    self.y = 127
    self.floor = 2

    self.back = -10
    self.front = 10

    self.sprite = sprite = allocate_sprite()
    sprite.vpos = 0x400
    sprite.status = 1
    sprite.is_dynamic = False
    sprite.x = self.x
    sprite.y = self.y
    sprite.patterns = patterns
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.frame = -1
    sprite.patterns_blocks = patterns_blocks
    sprite.bbox = (-6, 0, 16, 64)

    init_wait(self)


def init_wait(self):
    set_animation(self.sprite, WAIT)

