from object import *
from tsprite import *
from genepy import *
from res.projectile_data import *


def init_object():
    print 'init_object'
    self = allocate_object()
    self.status = ACTIVE

    self.x = x
    self.y = y
    self.floor = 2

    self.back = -4
    self.front = 4

    self.sprite = sprite = allocate_sprite()
    sprite.vpos = 0x300
    sprite.is_static = True
    sprite.status = 1
    sprite.x = self.x
    sprite.y = self.y
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.frame = -1

    init_stand(self)
