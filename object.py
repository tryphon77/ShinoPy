from layer import layer_A
from queue import Queue
from tsprite import *

from camera import camera

INACTIVE = 0
ACTIVE = 1

impulsions_table = [-5.5, -6.5, -7.5, -8.5, -9.5, -10.5, -11.5, -12.5]


class Object():
    # debug purposes
    current_id_ = 1

    def __init__(self):
        # debug purposes
        self.id_ = 0
        self.status = INACTIVE
        self.list = None

        self.x = 0.0
        self.y = 0.0
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.max_speed_x = 0.0
        self.max_speed_y = 0.0
        self.accel_x = 0.0
        self.accel_y = 0.0

        self.sprite = None

        self.bbox = None
        self.hitbox = None

        self.back = 0
        self.front = 0

#        self.is_flipped = False
        self.moves_to_left = False
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
        self.collision_function = None
        self.hit_function = None
        self.release_function = None


objects_size = 32
objects = [Object() for _ in range(objects_size)]

all_objects = Queue()
friend_objects = Queue()
ennemy_objects = Queue()
friend_projectiles = Queue()
ennemy_projectiles = Queue()


def allocate_object():
    for i, o in enumerate(objects):
        if o.status == INACTIVE:
            o.id_ = Object.current_id_
            Object.current_id_ += 1
            # print 'init object #%d at pos: %d' % (o.id_, i)
            break
    else:
        return None

    # clear fields
    o.collided_object = None
    o.hit_object = None
    o.hitting_object = None

    all_objects.add(o)
    return o


def release_object(obj):
    if obj.sprite:
        disable_sprite(obj.sprite)
        obj.sprite = None

    obj.id_ = 0
    obj.status = INACTIVE
    obj.update_function = None
    obj.moves_to_left = False

    # print 'releasing object #%d at pos: %d' % (obj.id_, all_objects.index(obj))
    all_objects.remove(obj)


def set_physics(self, sx, ax, sy, ay):
    if self.moves_to_left:
        self.speed_x = -sx
        self.accel_x = -ax
    else:
        self.speed_x = sx
        self.accel_x = ax
    self.speed_y = sy
    self.accel_y = ay


def signate(self, value):
    if self.moves_to_left:
#    if self.is_flipped:
        return -value
    else:
        return value


def flip_controls():
    Globs.forward, Globs.backward = Globs.backward, Globs.forward


def flip(self):
    # self.back, self.front = self.front, self.back
    self.sprite.is_flipped = not self.sprite.is_flipped
    self.moves_to_left = not self.moves_to_left


def head_towards(self, other):
    self.moves_to_left = self.sprite.is_flipped = (self.x >= other.x)

    
def collides_background(self, dx, dy):
    x = int(self.x + signate(self, dx)) / 16
    # x = int(self.x + dx) / 16
    y = int(self.y + dy) / 16
    res = Globs.collision_map[y * layer_A.twidth + x]
    # print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d -> %d (%d/%d)' % (self.x, signate(self, dx), self.y, dy, x, y, y * layer_A.twidth + x, res, res & 7, self.floor)
    return res & 7 == self.floor


def get_hijump_impulsion(self):
    x = int(self.x) / 16
    y = int(self.y + 1) / 16
    # print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d' % (self.x, dx, self.y, dy, x, y, y * layer_A.twidth + x)
    return impulsions_table[(Globs.collision_map[y * layer_A.twidth + x] >> 3) & 7]


# def fix_pos(x, dx):
    # if dx > 0:
        # return ((int(x) + dx) & 0xFFF0) - dx
    # return (int(x) & 0xFFF0) + dx

def fix_hpos(self):
    if self.moves_to_left:
        fixed = (int(self.x) & 0xFFF0) + self.front
        # print 'fix_hpos: %d -> %d' % (self.x, fixed)
        self.x = fixed
    else:
        fixed = (int(self.x + self.front) & 0xFFF0) - self.front - 1
        # print 'fix_hpos: %d -> %d' % (self.x, fixed)
        self.x = fixed


def fix_vpos(self):
    # print 'fix_vpos: %d -> %d' % (self.y, (int(self.y) & 0xFFF0) - 1)
    self.y = (int(self.y) & 0xFFF0) - 1


def update_object(self):
    if self.update_function:
        self.update_function(self)


def compute_box(self, box):
    if box:
        x_, y_, w_, h_ = box
        bx0 = int(self.x) + x_
        bx1 = bx0 + w_
        by0 = int(self.y) + y_
        by1 = by0 + h_
        return (bx0, bx1, by0, by1)
    else:
        return None
        
def compute_boxes(self):
    sprite = self.sprite
    self.bbox = compute_box(self, sprite.bbox)
    self.hitbox = compute_box(self, sprite.hitbox)


def collision_between_boxes(box1, box2):
    l1, r1, t1, b1 = box1
    l2, r2, t2, b2 = box2

    if r1 < l2:
        return False
    if l1 > r2:
        return False
    if b1 < t2:
        return False
    if t1 > b2:
        return False

    return True


def update_all_objects():
    # 1) Introduces new objects according to camera movement
    if camera.moves_left:
        i = Globs.objects_hindex
        while i > 0:
            i -= 1
            entry = Globs.objects_hlist[i]
            is_active, sx, sy, init_function = entry[:4]
            # print 'moves left and considering #%d at (%d, %d) / camera.left = %d' % (i, sx, sy, camera.left)
            if sx < camera.virtual_left:
                break
            elif sx > camera.left:
                pass
                # print 'ignoring %d' % i
            elif is_active:
                pass
                # print '%d already active' % i
            elif camera.virtual_top <= sy <= camera.virtual_bottom:
                # print 'sx = %d, camera.left = %d' % (sx, camera.left)
                init_function(entry)
        # if Globs.objects_hindex != i + 1:
            # print 'hindex : %d -> %d' % (Globs.objects_hindex, i + 1)
        Globs.objects_hindex = i + 1
    elif camera.moves_right:
        i = Globs.objects_hindex
        while i < Globs.n_objects:
            entry = Globs.objects_hlist[i]
            is_active, sx, sy, init_function = entry[:4]
            # print 'moves right and considering #%d at (%d, %d) / camera.left = %d' % (i, sx, sy, camera.left)
            if sx > camera.virtual_right:
                break
            elif sx < camera.right:
                pass
                # print 'ignoring %d' % i
            elif is_active:
                pass
                # print '%d already active' % i
            elif camera.virtual_top <= sy <= camera.virtual_bottom:
                # print 'sx = %d, camera.right = %d' % (sx, camera.right)
                init_function(entry)
            i += 1
        # if Globs.objects_hindex != i:
            # print 'hindex : %d -> %d' % (Globs.objects_hindex, i)
        Globs.objects_hindex = i
    
    # 2) Updates visible objects, releases invisibles

    # print 'camera: (%d, %d, %d, %d)' % (camera.virtual_left, camera.virtual_right, camera.virtual_top, camera.virtual_bottom)
    for obj in all_objects:
        # print 'object %d' % obj.id_
        if obj.status:
            if camera.virtual_left <= obj.x <= camera.virtual_right\
                    and camera.virtual_top < obj.y < camera.virtual_bottom:
                # print 'update object %d' % obj.id_
                update_object(obj)

                if obj.status:
                    # print 'compute boxes on object %d' % obj.id_
                    compute_boxes(obj)
                    
            else:
                # print 'out of screen'
                obj.release_function(obj)
                # release_object(obj)
                # obj.object_entry[0] = False
                # debug
                # ennemy_objects.remove(obj)


    # 3) collisions between objects
    
    # 3a) friend_projectiles against ennemy_objects
    # for shuriken in friends_projectiles:
        # shuriken_hitbox = shuriken.hitbox

        # if shuriken_hitbox:
            # for ennemy in ennemy_objects:
                # # print 'ennemy object #%d' % ennemy.id_
                # if ennemy.floor == shuriken.floor:
                    # ennemy_bbox = ennemy.bbox
                    # if ennemy_bbox:
                        # if collision_between_boxes(shuriken_hitbox, ennemy_bbox):
                            # # print 'collision'
                            # shuriken.hitting_object = ennemy
                            # ennemy.hit_object = shuriken
                            # if ennemy.hit_function:
                                # ennemy.hit_function(ennemy)
    
    # 3b) friends 
    for friend in friend_objects:
        friend_bbox = friend.bbox
        friend_hitbox = friend.hitbox
        # print 'testing friend object #%s (%s, %s)' % (friend.id_, friend.x, friend.y)

        # test friend hitbox against ennemy bbox
        if friend_hitbox:
            # print 'against'
            for ennemy in ennemy_objects:
                # print 'ennemy object #%d' % ennemy.id_
                if ennemy.floor == friend.floor:
                    ennemy_bbox = ennemy.bbox
                    if ennemy_bbox:
                        if collision_between_boxes(friend_hitbox, ennemy_bbox):
                            print 'musashi hits ennemy'
                            friend.hitting_object = ennemy
                            ennemy.hit_object = friend
                            if ennemy.hit_function:
                                ennemy.hit_function(ennemy)
        
        # test friend bbox against ennemy bbox
        if friend_bbox:
            # print 'against'
            for ennemy in ennemy_objects:
                # print 'ennemy object #%d' % ennemy.id_
                
                if ennemy.floor == friend.floor:
                
                    ennemy_hitbox = ennemy.hitbox
                    if ennemy_hitbox:
                        if collision_between_boxes(friend_bbox, ennemy_hitbox):
                            print 'ennemy hits musashi'
                            friend.hit_object = ennemy
                            ennemy.hitting_object = friend
                            if friend.hit_function:
                                friend.hit_function(friend)

                    ennemy_bbox = ennemy.bbox
                    if ennemy_bbox:
                        if collision_between_boxes(friend_bbox, ennemy_bbox):
                            print 'collision'
                            friend.collided_object = ennemy
                            ennemy.collided_object = friend
                            if friend.collision_function:
                                friend.collision_function(friend)
                            if ennemy.collision_function:
                                ennemy.collision_function(ennemy)
        
        


def update_all_sprites():
    # print "update_all_sprites"
    Globs.link = 0
    for obj in objects:
        sprite = obj.sprite
        if sprite and sprite.status:
            # print 'sprite #%d (status = %d)' % (i, sprite.status)
            sprite.x = int(obj.x) - Globs.camera_x
            sprite.y = int(obj.y) - Globs.camera_y
#            sprite.is_flipped = obj.is_flipped
            sprite_update(sprite)

    GP.sprite_cache[Globs.link - 1].link = 0
