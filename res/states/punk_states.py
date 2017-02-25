from object import *
from tsprite import *
from globals import Globs

from res.punk_data import *


def init_object(entry):
    floor, x, y, _ = entry[4:]
    # print 'init punk at (%d, %d)' % (x, y)
    self = allocate_object()
    
    entry[0] = True
    self.object_entry = entry
    ennemy_objects.add(self)
    self.release_function = release
    
    self.status = ACTIVE

    self.x = x
    self.y = y
    self.floor = floor

    self.back = -10
    self.front = 10

    self.sprite = sprite = allocate_dynamic_sprite()
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

    # if self.sprite.is_flipped:
        # res = 'flipped, '
    # else:
        # res = 'not flipped, '
    # if self.moves_to_left:
        # res += 'moves to left'
    # else:
        # res += 'moves to right'
    # print res
    
    init_walk(self)


def release(self):
    release_object(self)
    self.object_entry[0] = False
    ennemy_objects.remove(self)


def init_hit(self):
    # print 'punk init_hit'
    self.is_dead = True
    other = self.hit_object
    # print 'other.speed = %f' % other.speed_x

    if self.x < other.x:
        self.speed_x = -2
        self.moves_to_left = True
    else:
        self.speed_x = 2
        self.moves_to_left = False

    self.speed_y = -4
    self.accel_y = 0.5

    set_animation(self.sprite, HIT)
    self.update_function = update_collision
    self.collision_function = None
    self.hit_function = None


def init_walk(self):
    # print 'punk init_walk'
    self.moves_to_left = self.sprite.is_flipped
    set_physics(self, 1, 0, 0, 0)
    set_animation(self.sprite, WALK)
    self.update_function = update_walk
    self.collision_function = init_collision
    self.hit_function = init_hit


def update_walk(self):
    # check_disable
    # print 'punk update_walk'

    self.x += self.speed_x

    if collides_background(self, self.front, 1) == 0\
       and collides_background(self, self.back, 1) == 0:
        init_fall(self)

    elif collides_background(self, self.front + 1, -32):
        fix_hpos(self)
        flip(self)
        self.speed_x = -self.speed_x
        # init_walk(self)

    elif collides_background(self, self.front + 1, 0):
        init_jump(self)

    elif self.floor == Globs.musashi.floor:
        if self.moves_to_left:
            d = self.x - Globs.musashi.x
            if d > 0:
                if d < 32:
                    init_punch(self)
                elif d < 48:
                    init_kick(self)
        else:
            d = Globs.musashi.x - self.x
            if d > 0:
                if d < 32:
                    init_punch(self)
                elif d < 48:
                    init_kick(self)


def init_collision(self):
    # print 'punk init_collision'
    self.is_dead = False # self.is_hit
    other = self.collided_object
    # print 'other.speed = %f' % other.speed_x

    if self.x < other.x:
        self.speed_x = -2
        self.moves_to_left = True
    else:
        self.speed_x = 2
        self.moves_to_left = False

    self.speed_y = -4
    self.accel_y = 0.5

    set_animation(self.sprite, HIT)
    self.update_function = update_collision
    self.collision_function = None


def update_collision(self):
    # print 'punk update_collision [moves_to_left = %s, front = %s]' % (self.moves_to_left, self.front)
    self.x += self.speed_x

    if collides_background(self, self.front, 0):
        fix_hpos(self)
        self.speed_x = 0

    self.speed_y += self.accel_y
    self.y += self.speed_y

    if collides_background(self, self.front, 0) or\
            collides_background(self, self.back, 0):
        fix_vpos(self)
        if self.is_dead:
            init_death(self)
        else:
            init_walk(self)


def init_jump(self):
    set_physics(self, 1, 0, -5, 0.25)
    set_animation(self.sprite, JUMP)
    self.update_function = update_jump


def update_jump(self):
    self.x += self.speed_x

    if collides_background(self, self.front, 0):
        fix_hpos(self)
        self.speed_x = signate(self, 1)

    self.speed_y += self.accel_y
    self.y += self.speed_y

    if self.speed_y >= 0:
        init_fall(self)


def init_fall(self):
    # print 'punk init_fall'
    self.accel_y = 0.25
    set_animation(self.sprite, FALL)
    self.update_function = update_fall


def update_fall(self):
    # print 'punk update_fall'
    self.x += self.speed_x

    if collides_background(self, self.front, 0):
        fix_hpos(self)
        self.speed_x = 0

    self.speed_y += self.accel_y
    self.y += self.speed_y

    if collides_background(self, self.front, 0)\
            or collides_background(self, self.back, 0):
        fix_vpos(self)
        init_walk(self)


def init_death(self):
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, DEAD)
    self.update_function = update_death


def update_death(self):
    if self.sprite.is_animation_over:
        # print 'dead'
        release(self)


def init_punch(self):
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, PUNCH)
    self.update_function = update_attack


def init_kick(self):
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, KICK)
    self.update_function = update_attack


def update_attack(self):
    if self.sprite.is_animation_over:
        init_walk(self)
