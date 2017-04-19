from object import *
from tsprite import *
from genepy import *
from res.projectile_data import *


def init_object():
    # print 'init shuriken'
    self = allocate_object()
    # print 'shuriken id = %d' % self.id_
    friend_projectiles.add(self)
    
    self.status = ACTIVE

    self.back = -4
    self.front = 4

    self.sprite = sprite = allocate_static_sprite()
    sprite.vpos = 0x300
    sprite.status = 1
    sprite.x = self.x
    sprite.y = self.y
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.bboxes_table = bounding_boxes
    sprite.hitboxes = hitboxes

    sprite.frame = -1

    self.hitting_object = None
    set_animation(sprite, SHURIKEN)
    self.update_function = update
    self.collision_function = init_vanish
    self.release_function = release_shuriken

    return self


def release_shuriken(self):
    release_object(self)
    friend_projectiles.remove(self)


def update(self):
    self.x += self.speed_x
    if self.hitting_object:
        init_vanish(self)
    if collides_background(self, self.front, 0):
        # print 'projectile .x = %d, .speed_x = %d, .front = %d' % (self.x, self.speed_x, self.front)
        init_vanish(self)

def init_vanish(self):
    self.speed_x = 0
    set_animation(self.sprite, SHURIKEN_VANISH)
    self.update_function = update_vanish

def update_vanish(self):
    if self.sprite.is_animation_over:
        release_shuriken(self)


def init_bullet():
    # print 'init bullet'
    self = allocate_object()
    # print 'shuriken id = %d' % self.id_
    ennemy_projectiles.add(self)
    
    self.status = ACTIVE

    self.back = -4
    self.front = 4

    self.sprite = sprite = allocate_static_sprite()
    sprite.vpos = 0x300
    sprite.status = 1
    sprite.x = self.x
    sprite.y = self.y
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.bboxes_table = bounding_boxes
    sprite.hitboxes = hitboxes

    sprite.frame = -1

    set_animation(sprite, BULLET)
    self.update_function = update_bullet
    self.collision_function = init_bullet_vanish
    self.release_function = release_bullet

    return self


def release_bullet(self):
    release_object(self)
    ennemy_projectiles.remove(self)


def update_bullet(self):
    self.x += self.speed_x
    if self.hitting_object:
        init_bullet_vanish(self)
    if collides_background(self, self.front, 0):
        # print 'projectile .x = %d, .speed_x = %d, .front = %d' % (self.x, self.speed_x, self.front)
        init_bullet_vanish(self)

def init_bullet_vanish(self):
    self.speed_x = 0
    set_animation(self.sprite, BULLET_VANISH)
    self.update_function = update_bullet_vanish

def update_bullet_vanish(self):
    if self.sprite.is_animation_over:
        release_bullet(self)

