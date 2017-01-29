from tilemap import layer_A
from queue import Queue
from tsprite import *

INACTIVE = 0
ACTIVE = 1

impulsions_table = [-5.5, -6.5, -7.5, -8.5, -9.5, -10.5, -11.5, -12.5]


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

        self.back = 0
        self.front = 0

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

        self.update_function = None


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

    print 'releasing object #%d' % all_objects.index(obj)
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


def signate(self, value):
    if self.is_flipped:
        return -value
    else:
        return value


def flip_controls():
    Globs.forward, Globs.backward = Globs.backward, Globs.forward


def flip(self):
    # self.back, self.front = self.front, self.back
    self.is_flipped = not self.is_flipped


def collides_background(self, dx, dy):
    x = int(self.x + signate(self, dx)) / 16
    y = int(self.y + dy) / 16
    res = Globs.collision_map[y * layer_A.twidth + x]
    # print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d -> %d (%d/%d)' % (self.x, signate(self, dx), self.y, dy, x, y, y * layer_A.twidth + x, res, res & 7, self.floor)
    return res & 7 == self.floor


def get_hijump_impulsion(self):
    x = int(self.x) / 16
    y = int(self.y + 1) / 16
    # print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d' % (self.x, dx, self.y, dy, x, y, y * layer_A.twidth + x)
    return impulsions_table[(Globs.collision_map[y * layer_A.twidth + x] >> 3) & 7]


def fix_hpos(self):
    if self.is_flipped:
        fixed = (int(self.x) & 0xFFF0) + self.front
        # print 'fix_hpos: %d -> %d' % (self.x, fixed)
        self.x = fixed
    else:
        fixed = (int(self.x + self.front) & 0xFFF0) - self.front - 1
        # print 'fix_hpos: %d -> %d' % (self.x, fixed)
        self.x = fixed


def fix_vpos(self):
    self.y = (int(self.y) & 0xFFF0) - 1


def update_object(self):
    if self.update_function:
        self.update_function(self)


def update_all_objects():
    for obj in all_objects.data[:all_objects.cursor]:
        if obj.status:
            update_object(obj)
#        else:
#            break


def update_all_sprites():
    # print "update_all_sprites"
    Globs.link = 0
    for obj in objects:
        sprite = obj.sprite
        if sprite and sprite.status:
            # print 'sprite #%d (status = %d)' % (i, sprite.status)
            sprite.x = int(obj.x) - Globs.camera_x
            sprite.y = int(obj.y) - Globs.camera_y
            sprite.is_flipped = obj.is_flipped
            sprite_update(sprite)

    GP.sprite_cache[Globs.link - 1].link = 0
