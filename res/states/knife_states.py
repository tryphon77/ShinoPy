from object import *
from tsprite import *

from res.knife_data import *


def init_object():
    print 'init knife'
    self = allocate_object()
    self.status = ACTIVE

    self.x = 256
    self.y = 127
    self.floor = 2

    self.back = -10
    self.front = 10

    self.sprite = sprite = allocate_sprite()
    sprite.vpos = 0x260
    sprite.status = 1
    sprite.is_dynamic = True
    sprite.x = self.x
    sprite.y = self.y
    sprite.patterns = patterns
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.frame = -1
    sprite.patterns_blocks = patterns_blocks
    sprite.bbox = (-6, 0, 16, 64)

    init_walk(self)


def init_walk(self):
    set_animation(self.sprite, WALK)

