from layer import layer_A
from queue import Queue
from tsprite import *

from camera import camera

impulsions_table = [0, -4, -5.5, -7, -8, -9, -10, -10.5, -11.5, -12, -12.5, -13.5, -14, -14.5, -15]


class Object():
	# debug purposes
	current_id_ = 1

	def __init__(self):
		# debug purposes
		self.id_ = 0	#@TODO : check if used
		self.name = 'unnamed'	#@DEBUG only
		self.list = None # useful ?

		self.trigger_x = 0
		self.trigger_y = 0
		self.hp_max = 0
		self.org_floor = 0
		self.org_x = 0
		self.org_y = 0
		
		self.hp = 0
		self.floor = 0
		self.x = 0.0
		self.y = 0.0
		self.speed_x = 0.0
		self.speed_y = 0.0
		self.max_speed_x = 0.0
		self.max_speed_y = 0.0
		self.accel_x = 0.0
		self.accel_y = 0.0

		self.sprite = None

		# global boxes, used when object is collidable but not displayable
		self.global_bbox = None
		self.global_hitbox = None
		
		self.bbox = None
		self.hitbox = None

		self.back = 0
		self.front = 0

		self.moves_to_left = False

		self.is_initialized = False
		self.is_activated = False
		self.is_displayable = False
		self.is_collidable = False
		# self.is_hittable = False

		self.is_dead = False
		self.is_collided = False
		self.is_hit = False
		self.has_hit = False

		# b1 b0
		# b0 : 0 normal, 1 bonus
		# b1 : 0 close contact, 1 projectile 
		self.attack_type = 0
		
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

		self.activate_function = None
		self.update_function = None
		self.collision_function = None
		self.hit_function = None
		self.release_function = None


objects_size = 64
auxiliary_objects_size = 16
temporary_objects_size = 16
objects = [Object() for _ in range(objects_size)]
temporary_objects = [Object() for _ in range(temporary_objects_size)]
auxiliary_objects = [Object() for _ in range(auxiliary_objects_size)]


all_objects = Queue()
friend_objects = Queue()
ennemy_objects = Queue()
hostage_objects = Queue()
friend_projectiles = Queue()
ennemy_projectiles = Queue()


def clear_all_objects():
	all_objects.clear()
	friend_objects.clear()
	ennemy_objects.clear()
	hostage_objects.clear()
	friend_projectiles.clear()
	ennemy_projectiles.clear()
	
	for o in objects:
		clear_object(o)


def clear_object(obj):
	obj.id_ = 0
	obj.is_initialized = False
	reset_object(obj)

def reset_object(obj):
	obj.is_activated = False
	obj.is_displayable = False
	obj.is_collidable = False

	obj.update_function = None
	obj.moves_to_left = False
	obj.is_collided = False

	obj.collided_object = None
	obj.hit_object = None
	obj.hitting_object = None
	
def allocate_object(object_array):
	# print ('allocate_object:')
	for i, o in enumerate(object_array):
		if not o.is_initialized:
			o.id_ = Object.current_id_
			Object.current_id_ += 1
			# print('init object #%d at pos: %d' % (o.id_, i))
			break
	else:
		return None

	# clear fields
	o.collided_object = None
	o.hit_object = None
	o.hitting_object = None

	return o


def release_object(obj):
	if obj.sprite:
		release_sprite(obj.sprite)
		obj.sprite = None

	reset_object(obj)
	
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
		return -value
	else:
		return value


# useful ?
def flip_controls__():
	Globs.forward, Globs.backward = Globs.backward, Globs.forward


# useful ?
def flip__(self):
	# self.back, self.front = self.front, self.back
	self.sprite.is_flipped = not self.sprite.is_flipped
	self.moves_to_left = not self.moves_to_left

# useful ? (to move in common.py)
def head_towards(self, other):
	self.moves_to_left = self.sprite.is_flipped = (self.x >= other.x)

	
def collides_background(self, dx, dy):
	x = int(self.x + signate(self, dx)) // 16
	if x < 0:
		return True
	if x >= layer_A.twidth:
		return True
	y = int(self.y + dy) // 16
	res = Globs.collision_map[y * layer_A.twidth + x]
	# print 'collides_background at pos (%d + %d, %d + %d) on tile (%d, %d) pos = %d -> %d (%d//%d)' % (self.x, signate(self, dx), self.y, dy, x, y, y * layer_A.twidth + x, res, res & 7, self.floor)
	# print ('(%d + %d, %d + %d) : collides_background (%d, %d) : %s' % (self.x, signate(self, dx), self.y, dy, x, y, res & 7))
	return res & 7 == self.floor & 7


def get_hijump_impulsion(self):
	x1 = int(self.x + self.back) // 16
	x2 = int(self.x + self.front) // 16
	y = int(self.y + 1) // 16

	# bug potentiel : x2 n'est pas forcément > x1 !!!
	i = y * layer_A.twidth + x1
	v = impulsions_table[(Globs.collision_map[i] >> 4) & 15]
	if v and (x1 != x2):
		v = max(v, impulsions_table[(Globs.collision_map[i + 1] >> 4) & 15])
		# print('impulsion: %s' % v)
	return v


def get_hijump_down_impulsion(self):
	x1 = int(self.x + self.back) // 16
	x2 = int(self.x + self.front) // 16
	y = int(self.y + 1) // 16
	i = y * layer_A.twidth + x1
	v = impulsions_table[(Globs.collision_map[i] >> 8) & 15]

	# bug potentiel : x2 n'est pas forcément > x1 !!!
	if v and (x1 != x2):
		v = max(v, impulsions_table[(Globs.collision_map[i + 1] >> 8) & 15])
		# print('impulsion: %s' % v)
		# GP.halt()
	return v


def fix_hpos(self):
	if self.moves_to_left:
		# print ('left')
		if self.speed_x <= 0:
			# print ('front: %d' % self.front)
			fixed = (int(self.x - self.front) & 0xFFF0) + self.front + 16
		else:
			# print ('back: %d' % self.back)
			fixed = (int(self.x - self.back) & 0xFFF0) + self.back - 1
		# print 'fix_hpos: %d -> %d' % (self.x, fixed)
	else:
		# print ('right')
		if self.speed_x >= 0:
			# print ('front: %d' % self.front)
			fixed = (int(self.x + self.front) & 0xFFF0) - self.front - 1
		else:
			# print ('back: %d' % self.back)
			fixed = (int(self.x + self.back) & 0xFFF0) - self.back + 16
	# print ('fix_hpos: %d -> %d' % (self.x, fixed))
	self.x = fixed

def fix_hpos_(self, dx):
	if self.moves_to_left:
		fixed = ((int(self.x) - dx) & 0xFFF0) + dx
	else:
		fixed = ((int(self.x) + dx) & 0xFFF0) - dx
	self.x = fixed

def fix_vpos(self):
	# print 'fix_vpos: %d -> %d' % (self.y, (int(self.y) & 0xFFF0) - 1)
	self.y = ((int(self.y) + 1) & 0xFFF0) - 1


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
	if self.is_displayable:
		sprite = self.sprite
		bbox = sprite.bbox
		hitbox = sprite.hitbox
	else:
		bbox = self.global_bbox
		hitbox = self.global_hitbox
	self.bbox = compute_box(self, bbox)
	self.hitbox = compute_box(self, hitbox)


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


def check_entry(obj, 
				too_far,
				too_near,
				viewable):
	sx = obj.trigger_x
	sy = obj.trigger_y
	
	if too_far(sx, sy):
		# print ('%s: too far' % entry)
		return True
	elif too_near(sx, sy):
		# print ('ignoring %s: too near' % entry)
		return False
	elif obj.is_activated:
		# print('%s already on screen' % entry)
		return False
	elif viewable(sx, sy):
		# print ('sx = %d, camera.left = %d' % (sx, camera.left))
		obj.activate_function(obj)
		return True
	else:
		print ('this shouldnt occur')
		print (camera.virtual_top, sy, camera.virtual_bottom)
		# exit()

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
	new_object_chunk = Globs.objects_map[(int(Globs.musashi.y) >> 4) * layer_A.twidth + (int(Globs.musashi.x) >> 4)]
	if (new_object_chunk != Globs.objects_chunk):
		Globs.objects_chunk = new_object_chunk
		
		if camera.moves_right:
			# print ('entering chunk %02X from the left: %s' % (Globs.objects_chunk, Globs.objects_from_left[new_object_chunk]))
			# GP.halt()

			introduce_new_object_chunk(Globs.objects_from_left[new_object_chunk])
		elif camera.moves_left:
			# print ('entering chunk %02X from the right: %s' % (Globs.objects_chunk, Globs.objects_from_right[new_object_chunk]))
			introduce_new_object_chunk(Globs.objects_from_right[new_object_chunk])
			
		if camera.moves_up:
			# print ('entering chunk %02X from the bottom: %s' % (Globs.objects_chunk, Globs.objects_from_bottom[new_object_chunk]))
			introduce_new_object_chunk(Globs.objects_from_bottom[new_object_chunk])
		elif camera.moves_down:
			# print ('entering chunk %02X from the top: %s' % (Globs.objects_chunk, Globs.objects_from_top[new_object_chunk]))
			introduce_new_object_chunk(Globs.objects_from_top[new_object_chunk])
		

def introduce_new_object_chunk(chunk):
	for i in chunk:
		obj = objects[i]
		if obj.is_initialized and not obj.is_activated:
			obj.activate_function(obj)

def update_all_objects_on_screen():
	print('update_all_objects_on_screen: #all = %d' % len(all_objects))
	for obj in all_objects:
		print ('object %d (%s) : %s, bbox = %s, hitbox = %s' % (obj.id_, obj.name, ', '.join([['', 'initialized'][obj.is_initialized], ['', 'activated'][obj.is_activated], ['', 'displayable'][obj.is_displayable], ['', 'collidable'][obj.is_collidable]]), obj.bbox, obj.hitbox))
		# if obj.status:
		if obj.is_activated:
			if camera.virtual_left <= obj.x <= camera.virtual_right\
			and camera.virtual_top < obj.y < camera.virtual_bottom:
				# print ('update object %d' % obj.id_)
				update_object(obj)

				if obj.is_collidable:
					compute_boxes(obj)
					
			else:
				if obj.release_function:
					obj.release_function(obj)


def check_collisions(source, source_box_type,
					 targets, target_box_type,
					 do_collision):
		if source.is_collidable:
			source_floor = source.floor
			source_box = getattr(source, source_box_type)
			if source_box:
				for target in targets:
					# print ('source: %s, target: %s, %s, %s' % (source.name, target.name, target.is_collidable, target.floor))
						
					if target.is_collidable and target.floor == source_floor:
						target_box = getattr(target, target_box_type)
						# print ('%s: x = %d, y = %d, box = %s' % (target.name, target.x, target.y, target_box))
						
						if target_box:
							if collision_between_boxes(source_box, target_box):
								# print ('collision between [%s] and [%s]' % (source.name, target.name))
								do_collision(source, target)


def musashi_collides_ennemy(friend, ennemy):
	# print ('musashi_collides_ennemy : %s -> %s' % (friend.name, ennemy.name))
	# GP.halt()
	friend.other_object = ennemy
	ennemy.other_object = friend
	
	# if ennemy.speed_x > 0:
		# friend.speed_x = 2
		# # friend.moves_to_left = False
		# ennemy.speed_x = -2
		# # ennemy.moves_to_left = True
	# elif ennemy.speed_x < 0:
		# friend.speed_x = -2
		# # friend.moves_to_left = True
		# ennemy.speed_x = 2
		# # ennemy.moves_to_left = False
	if friend.x < ennemy.x:
		friend.speed_x = -2
		# friend.moves_to_left = True
		ennemy.speed_x = 2
		# ennemy.moves_to_left = False
	else:
		friend.speed_x = 2
		# friend.moves_to_left = False
		ennemy.speed_x = -2
		# ennemy.moves_to_left = True
	
	if friend.collision_function:
		friend.collision_function(friend)
	if ennemy.collision_function:
		ennemy.collision_function(ennemy)

def musashi_frees_hostage(musashi, hostage):
	print ('musashi_frees_hostage')
	hostage.collision_function(hostage)

def musashi_hits_ennemy(friend, ennemy):
	# print ('musashi_hits_ennemy : %s -> %s' % (friend.name, ennemy.name))
	# GP.halt()
	if friend.x < ennemy.x:
		friend.speed_x = -2
		# friend.moves_to_left = True
		ennemy.speed_x = 2
		# ennemy.moves_to_left = False
	else:
		friend.speed_x = 2
		# friend.moves_to_left = False
		ennemy.speed_x = -2
		# ennemy.moves_to_left = True

	# print('musashi hits ennemy')
	friend.other_object = ennemy
	ennemy.other_object = friend
	if ennemy.hit_function:
		ennemy.hit_function(ennemy)

def shuriken_hits_ennemy(friend, ennemy):
	# print ('shuriken_hits_ennemy: %d (%s) -> %d (%s | %s)' % (friend.id_, friend.hitbox, ennemy.id_, ennemy.bbox, ennemy.global_bbox))
	# print (ennemy.hit_function)
	# GP.halt()
	if friend.x < ennemy.x:
		ennemy.speed_x = 2
	else:
		ennemy.speed_x = -2
	# else:
		# print ('immobile projectile')
		# print (friend.name, friend.id_, friend.is_collidable, friend.sprite.animation_id, friend.speed_x)
		# exit()

	friend.collision_function(friend)
	ennemy.other_object = friend
	if ennemy.hit_function:
		ennemy.hit_function(ennemy)

def bullet_hits_musashi(friend, ennemy):
	print ('bullet_hits_musashi')
	if ennemy.speed_x > 0:
		friend.speed_x = 2
	else:
		friend.speed_x = -2

	# print('projectile hits musashi')
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
		
	# 2) Updates visible objects, releases invisibles
	update_all_objects_on_screen()

	# 3) collisions between objects
	handle_collisions()


def update_all_sprites():
	# print "update_all_sprites"
	Globs.link = 0
	debug = []
	for i, obj in enumerate(all_objects):
		if obj.is_displayable:
			# print ('updating sprite of object #%d' % obj.id_)
			sprite = obj.sprite

			if sprite:
				if sprite.is_dynamic:
					debug += ['(%02dd)' % i]
				else:
					debug += ['(%02ds)' % i]
				
			if sprite and sprite.status:
				# print 'sprite #%d (status = %d)' % (i, sprite.status)
				sprite.x = int(obj.x) - Globs.camera_x
				sprite.y = int(obj.y) - Globs.camera_y
				sprite_update(sprite)
		else:
			pass
			# print ('object #%d is not displayable' % obj.id_)

	GP.sprite_cache[Globs.link - 1].link = 0
	
	print (', '.join(debug))


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

def __str__(self):
	return self.name