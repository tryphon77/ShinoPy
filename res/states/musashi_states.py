from object import *
from tsprite import *
from genepy import load_data_from_png
from res.musashi_data import *


def init_object():
    print 'init_object'
    self = allocate_object()
    self.status = ACTIVE

    self.x = 160
    self.y = 128

    self.poi_Gb = (-6, -1)
    self.poi_Gf = (10, -1)
    self.poi_Ab = (-6, 0)
    self.poi_Af = (10, 0)

    self.sprite = sprite = allocate_sprite()
    sprite.status = 1
    sprite.x = self.x
    sprite.y = self.y
    sprite.patterns = load_data_from_png('res/musashi_patterns.png')
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.frame = 76
    sprite.patterns_blocks = patterns_blocks
    sprite.bbox = (-6, 0, 16, 64)

    init_stand(self)


def init_stand(self):
    print 'init_stand'
    set_animation(self.sprite, STAND)
    set_physics(self, 0, 0, 0, 0)
    self.update_function = update_stand


def update_stand(self):
    print 'update_stand'
    if Globs.joy & Globs.forward:
        init_walk(self)
    elif Globs.joy & Globs.backward:
        flip_controls()
        flip(self)
        init_walk(self)
    elif not (collides_background(self, self.poi_Gf) or collides_background(self, self.poi_Gb)):
        init_fall(self)


def init_walk(self):
    print 'init_walk'
    set_animation(self.sprite, WALK)
    set_physics(self, 2, 0, 0, 0)
    self.update_function = update_walk


def update_walk(self):
    print 'update_walk'
    if Globs.joy & Globs.backward:
        print 'backward'
        flip_controls()
        flip(self)
        init_walk(self)
    elif not (Globs.joy & Globs.forward):
        init_stand(self)
    else:
        self.x += self.speed_x
        print 'moving: x = %d' % self.x

        if not (collides_background(self, self.poi_Gf) or collides_background(self, self.poi_Gb)):
            init_fall(self)
        elif collides_background(self, self.poi_Af):
            print 'collision'
            fix_hpos(self)
            init_stand(self)


def init_fall(self):
    pass
