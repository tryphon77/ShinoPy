from object import *
from tsprite import *

from res.shooter_data import *


def init_object(entry):
    print 'init shooter'

    floor, x, y, _ = entry[4:]
    self = allocate_object()

    entry[0] = True
    self.object_entry = entry

    self.list = ennemy_objects
    ennemy_objects.add(self)
    
    self.status = ACTIVE

    self.x = x
    self.y = y
    self.floor = floor

    self.back = -10
    self.front = 10

    self.sprite = sprite = allocate_sprite()
    sprite.status = 1
    sprite.x = self.x
    sprite.y = self.y
    sprite.patterns = patterns
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.bboxes_table = bounding_boxes
    sprite.hitboxes = hitboxes

    sprite.frame = -1
    sprite.patterns_blocks = patterns_blocks
    sprite.bbox = (-6, 0, 16, 64)

    if self.x > Globs.musashi.x:
        flip(self)

    init_walk(self)


def init_walk(self):
    set_animation(self.sprite, WALK)

