import random

from object import *
from tsprite import *

from res import projectiles
from res.shooter_data import *


# param1 = counter for stopping walk
# param2 = number of bullets
    

def init_object(entry):
    print 'init shooter'

    floor, x, y, _ = entry[4:]
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
    
    self.param2 = 3

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

    init_walk(self)


def release(self):
    release_object(self)
    self.object_entry[0] = False
    ennemy_objects.remove(self)

    
def shoot(self, dx, dy):
    bullet = projectiles.init_bullet()
    bullet.x = self.x + signate(self, dx)
    bullet.y = self.y + dy
    bullet.floor = self.floor
    bullet.speed_x = signate(self, 2)
    bullet.sprite.is_flipped = self.sprite.is_flipped
    # print 'throw .x = %d, .speed = %d, .front = %d' % (bullet.x, bullet.speed_x, bullet.front)


def init_walk(self):
    set_animation(self.sprite, WALK)
    set_physics(self, 1, 0, 0, 0)
    self.param1 = 1 << (random.randint(0, 7))
    self.update_function = update_walk
    self.collision_function = init_collision
    self.hit_function = init_hit

def update_walk(self):
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
        head_towards(self, Globs.musashi)
        init_shoot(self)

    elif self.sprite.is_animation_over:
        self.param1 -= 1
        if self.param1 <= 0:
            init_reload(self)


def init_reload(self):
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, RELOAD)
    self.param2 = 3
    self.update_function = update_reload

def update_reload(self):
    if self.sprite.is_animation_over:
        init_walk(self)


def init_shoot(self):
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, PREPARATION_SHOOT_STAND)
    self.update_function = update_shoot

def update_shoot(self):
    if self.sprite.is_animation_over:
        init_shoot1(self)
        

def init_shoot1(self):
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, SHOOT_STAND)
    self.update_function = update_shoot1

def update_shoot1(self):
    if self.sprite.total_ticks_in_animation == 4:
        shoot(self, 40, -40)
    elif self.sprite.is_animation_over:
        init_shoot1(self)
        self.param2 -= 1
        print 'bullets left: %d' % self.param2
        if self.param2 == 0:
            init_reload(self)


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

def update_collision(self):
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
    set_physics(self, 0, 0, 0, 0)
    set_animation(self.sprite, IMPULSE)
    self.update_function = update_jump

def update_jump(self):
    if self.sprite.is_animation_over:
        init_jump1(self)


def init_jump1(self):
    set_physics(self, 1, 0, -5, 0.25)
    set_animation(self.sprite, JUMP)
    self.update_function = update_jump1


def update_jump1(self):
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
        release_object(self)
        self.object_entry[0] = False
        # debug
        ennemy_objects.remove(self)        

