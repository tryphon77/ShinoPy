from layer import layer_A
from queue import Queue
from tsprite import *

from camera import camera

INACTIVE = 0	# object will be removed from list asap
ACTIVE = 1		# object is on screen and functionnal
DISABLED = 2	# object is missing for some frames, but will reappear

ON_SCREEN = 1
RESPAWNABLE = 2

impulsions_table = [0, -6.5, -7.5, -8.5, -9.5, -10.5, -11.5, -12.5]


class Object():
	# debug purposes
	current_id_ = 1

	def __init__(self):
		# debug purposes
		self.id_ = 0	#@TODO : check if used
		self.name = 'unnamed'	#@DEBUG only
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
		self.other_object = None

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
hostage_objects = Queue()
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
	obj.is_collidable = False
	obj.is_collided = False
	obj.is_dead = False

	obj.collided_object = None
	obj.hit_object = None
	obj.hitting_object = None

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
	x = int(self.x + signate(self, dx)) // 16
	# x = int(self.x + dx) // 16
	y = int(self.y + dy) // 16
	print (x, y)
	res = Globs.collision_map[y * layer_A.twidth + x]
	# print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d -> %d (%d//%d)' % (self.x, signate(self, dx), self.y, dy, x, y, y * layer_A.twidth + x, res, res & 7, self.floor)
	return res & 7 == self.floor & 7


def get_hijump_impulsion(self):
	x1 = int(self.x + self.back) // 16
	x2 = int(self.x + self.front) // 16
	y = int(self.y + 1) // 16
	# print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d' % (self.x, dx, self.y, dy, x, y, y * layer_A.twidth + x)
	i = y * layer_A.twidth + x1
	v = impulsions_table[(Globs.collision_map[i] >> 3) & 7]
	if v and (x1 != x2):
		v = max(v, impulsions_table[(Globs.collision_map[i + 1] >> 3) & 7])
	return v


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
		if self.moves_to_left:
			x_ = -x_ - w_
		bx0 = int(self.x) + x_
		bx1 = bx0 + w_
		by0 = int(self.y) + y_
		by1 = by0 + h_
		return (bx0, bx1, by0, by1)
	else:
		return None
		
def compute_boxes(self):
	sprite = self.sprite
	if sprite:
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


def check_entry(entry, 
				too_far,
				too_near,
				viewable):
	flags, sx, sy, init_function = entry[:4]
	if too_far(sx, sy):
		return True
	elif too_near(sx, sy):
		return False
		# print ('ignoring %d' % i)
	elif flags & ON_SCREEN:
		# print('%d already on screen' % i)
		return False
	elif not (flags & RESPAWNABLE):
		# print('%d not respawnable' % i)
		return False
	elif viewable(sx, sy):
		# print ('sx = %d, camera.left = %d' % (sx, camera.left))
		init_function(entry)
		return True

def too_far_left(x, y):
	return x < camera.virtual_left

def too_near_left(x, y):
	return x > camera.left

def too_far_right(x, y):
	return x > camera.virtual_right

def too_near_right(x, y):
	return x < camera.right

def viewable_h(x, y):
	return camera.virtual_top <= y <= camera.virtual_bottom

def introduce_new_objects():
	if camera.moves_left:
		i = Globs.objects_hindex
		while i > 0:
			i -= 1
			entry = Globs.objects_hlist[i]
			if check_entry(entry, too_far_left, too_near_left, viewable_h):
				break
		Globs.objects_hindex = i + 1

	elif camera.moves_right:
		i = Globs.objects_hindex
		while i < Globs.n_objects:
			entry = Globs.objects_hlist[i]
			if check_entry(entry, too_far_right, too_near_right, viewable_h):
				break
			i += 1
		Globs.objects_hindex = i


def update_all_objects_on_screen():
	for obj in all_objects:
		# print ('object %d' % obj.id_)
		if obj.status:
			if camera.virtual_left <= obj.x <= camera.virtual_right\
			and camera.virtual_top < obj.y < camera.virtual_bottom:
				# print ('update object %d' % obj.id_)
				update_object(obj)

				if obj.status == ACTIVE:
					compute_boxes(obj)
					
			else:
				if obj.release_function:
					obj.release_function(obj)


def check_collisions(source, source_box_type,
					 targets, target_box_type,
					 do_collision):
		source_floor = source.floor
		source_box = getattr(source, source_box_type)
		if source_box:
			for target in targets:
				if target.floor == source_floor:
					target_box = getattr(target, target_box_type)
					if target_box:
						if collision_between_boxes(source_box, target_box):
							do_collision(source, target)


def musashi_collides_ennemy(friend, ennemy):
	# print('collision', friend.collision_function, ennemy.collision_function)
	friend.other_object = ennemy
	ennemy.other_object = friend
	if friend.collision_function:
		friend.collision_function(friend)
	if ennemy.collision_function:
		ennemy.collision_function(ennemy)

def musashi_frees_hostage(musashi, hostage):
	hostage.collision_function(hostage)

def musashi_hits_ennemy(friend, ennemy):
	print('musashi hits ennemy')
	friend.other_object = ennemy
	ennemy.other_object = friend
	if ennemy.hit_function:
		ennemy.hit_function(ennemy)

def shuriken_hits_ennemy(friend, ennemy):
	print('musashi hits ennemy')
	ennemy.other_object = friend
	if ennemy.hit_function:
		ennemy.hit_function(ennemy)
	friend.collision_function(friend)

def bullet_hits_musashi(friend, ennemy):
	print('projectile hits musashi')
	friend.other_object = ennemy
	friend.hit_function(friend)
	ennemy.collision_function(ennemy)

def ennemy_hits_musashi(friend, ennemy):
	print('ennemy hits musashi')
	friend.other_object = ennemy
	ennemy.other_object = friend
	friend.hit_function(friend)

def handle_collisions():
	check_collisions(Globs.musashi, 'bbox',
					 hostage_objects, 'bbox',
					 musashi_frees_hostage)
	check_collisions(Globs.musashi, 'hitbox',
					 ennemy_objects, 'bbox',
					 musashi_hits_ennemy)
	for projectile in friend_projectiles:
		check_collisions(projectile, 'hitbox',
						 ennemy_objects, 'bbox',
						 shuriken_hits_ennemy)

	check_collisions(Globs.musashi, 'bbox',
					 ennemy_objects, 'hitbox',
					 ennemy_hits_musashi)
	check_collisions(Globs.musashi, 'bbox',
					 ennemy_projectiles, 'hitbox',
					 bullet_hits_musashi)
	check_collisions(Globs.musashi, 'bbox',
					 ennemy_objects, 'bbox',
					 musashi_collides_ennemy)


def update_all_objects():
	# 1) Introduces new objects according to camera movement
	introduce_new_objects()
		
	# 2) Updates visible objects, releases <invisibles
	update_all_objects_on_screen()

	# 3) collisions between objects
	handle_collisions()


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

#@deprecated
def check_box_on_objects(self, raw_box, objects):
	floor = self.floor
	box = compute_box(self, raw_box)

	for obj in objects:
		# print 'ennemy object #%d' % ennemy.id_
		if obj.floor == floor:
			other_box = obj.bbox
			if other_box:
				if collision_between_boxes(box, other_box):
					return True
	return False


def is_near(self, dx, dy, objects):
	floor = self.floor
	y1 = self.y
	y0 = y1 - dy

	if self.moves_to_left:
		x1 = self.x
		x0 = x1 - dx
	else:
		x0 = self.x
		x1 = x0 + dx
	for obj in objects:
		# print 'ennemy object #%d' % ennemy.id_
		if obj.is_collidable and obj.floor == floor:
			if x0 <= obj.x <= x1 and y0 <= obj.y <= y1:
				return True
	return False


def generic_collision(self):
	other = self.other_object

	if other.speed_x > 0:
		self.speed_x = 2
		self.moves_to_left = False
	elif other.speed_x < 0:
		self.speed_x = -2
		self.moves_to_left = True
	if self.x < other.x:
		self.speed_x = -2
		self.moves_to_left = True
	else:
		self.speed_x = 2
		self.moves_to_left = False

