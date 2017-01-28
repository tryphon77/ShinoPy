from object import *
from tsprite import *
from genepy import *
from res.projectile_data import *


def init_object():
    print 'init_object'
    self = allocate_object()
    self.status = ACTIVE

    self.back = -4
    self.front = 4

    self.sprite = sprite = allocate_sprite()
    sprite.vpos = 0x300
    sprite.is_dynamic = False
    sprite.status = 1
    sprite.x = self.x
    sprite.y = self.y
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.frame = -1

    set_animation(sprite, SHURIKEN)
    self.update_function = update

    return self


def update(self):
    if self.sprite.x <-16 or self.sprite.x > 336:
        release_object(self)
    else:
        self.x += self.speed_x
        if collides_background(self, self.front, 0):
            print 'projectile .x = %d, .speed_x = %d, .front = %d' % (self.x, self.speed_x, self.front)
            init_vanish(self)

def init_vanish(self):
    self.speed_x = 0
    set_animation(self.sprite, SHURIKEN_VANISH)
    self.update_function = update_vanish

def update_vanish(self):
    if self.sprite.is_animation_over:
        release_object(self)


