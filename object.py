from queue import Queue
from tsprite import *

INACTIVE = 0
ACTIVE = 1


class Object():
    def __init__(self):
        self.id_ = 0
        self.status = INACTIVE

        self.x = 0.0
        self.y = 0.0
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.max_speed_x = 0.0
        self.max_speed_y = 0.0
        self.accel_x = 0.0
        self.accel_y = 0.0

        self.sprite = None

        self.bx0 = 0
        self.by0 = 0
        self.bx1 = 0
        self.by1 = 0

        self.hx0 = 0
        self.hy0 = 0
        self.hx1 = 0
        self.hy1 = 0

        self.is_flipped = False
        self.collision_flag = False
        self.is_collidable = False
        self.is_hittable = False
        self.is_dead = False
        self.is_collided = False
        self.is_hit = False
        self.has_hit = False
        self.collided_object = None
        self.hit_object = None
        self.hitting_object = None

        self.param1 = 0
        self.param2 = 0
        self.param3 = 0
        self.param4 = 0
        self.ptr1 = None
        self.ptr2 = None


objects_size = 32
objects = [Object() for _ in range(objects_size)]

all_objects = Queue()
friends_objects = Queue()
ennemy_objects = Queue()


def allocate_object():
    for i, o in enumerate(objects):
        if o.status == INACTIVE:
            print 'allocating object #%d' % i
            break
    else:
        return None

    all_objects.add(o)
    return o


def release_object(obj):
    if obj.sprite:
        disable_sprite(obj.sprite)
        obj.sprite = None

    obj.id_ = 0
    obj.status = INACTIVE
    obj.update_function = None

    all_objects.remove(obj)


def set_physics(self, sx, ax, sy, ay):
    if self.is_flipped:
        self.speed_x = -sx
        self.accel_x = -ax
    else:
        self.speed_x = sx
        self.accel_x = ax
    self.speed_y = sy
    self.accel_y = ay


def flip_controls():
    Globs.forward, Globs.backward = Globs.backward, Globs.forward


def flip(self):
    self.poi_Gb, self.poi_Gf = self.poi_Gf, self.poi_Gb
    self.poi_Ab, self.poi_Af = self.poi_Af, self.poi_Ab
    self.is_flipped = not self.is_flipped


def collides_background(self, poi):
    x, y = poi
    x /= 32
    y /= 32
    return Globs.collision_map[y * Globs.layer_a_twidth + x]


def update_object(self):
    print 'update_function:', self.update_function
    if self.update_function:
        self.update_function(self)

        sprite = self.sprite
        if sprite:
            sprite.x = int(self.x)
            sprite.y = int(self.y)
            
            sprite_update(sprite)
            if sprite.new_frame:
                x, y, w, h = sprite.bbox
                if self.is_flipped:
                    self.poi_Gb = x + w, -1
                    self.poi_Gf = x, -1
                    self.poi_Af = x, 0
                    self.poi_Ab = x + w, 0
                else:
                    self.poi_Gf = x + w, -1
                    self.poi_Gb = x, -1
                    self.poi_Ab = x, 0
                    self.poi_Af = x + w, 0


def update_all_objects():
    for obj in objects:
        if obj.status:
            update_object(obj)
        else:
            break
