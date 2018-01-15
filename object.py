from layer import layer_A
from queue import Queue
from tsprite import *

from camera import camera

import log

# debug
_max_objects = 0
_max_dynamics = _max_viewable_dynamics = 0
_max_statics = _max_viewable_statics = 0
# end debug

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
		self.org_faces_left = False
		self.spawn_counter = 0
		
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
		
		# used for collisions : 
		# 1 if object ejected to the left, -1 to the right
		self.impulsion_x = 0

		self.sprite = None

		# global boxes, used when object is collidable but not displayable
		self.global_bbox = None
		self.global_hitbox = None
		
		self.bbox = None
		self.hitbox = None

		# deprecated (to remove)
		self.back = 0
		self.front = 0
		
		# last collision value computed (useful for fix_v/h_pos)
		self.coll_value = 0

		self.moves_to_left = False

		# FLAGS
		# is_initialized : True when the object in the object list is not NULL
		self.is_initialized = False
		
		# is_activated : True when the state machine of this object is running
		self.is_activated = False
		
		# is_displayable : True when the object has a sprite attached
		self.is_displayable = False
		
		# is collidable : True when the object has collision boxes (that can be NULL on some frames) and collisions must be checked
		self.is_collidable = False
		
		# is_boxed : True when the object sprite is onscreen (should be moved to tsprite)
		self.is_boxed = False
		# self.is_hittable = False

		self.is_dead = False
		self.is_collided = False
		self.is_hit = False
		self.has_hit = False

		# b1 b0
		# b0 : 0 normal, 1 bonus
		# b1 : 0 close contact, 1 projectile 
		# 0 = punch, 1 = sword, 2 = shuriken, 3 = bullet
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
temporary_objects_size = 16
objects = [Object() for _ in range(objects_size)]
temporary_objects = [Object() for _ in range(temporary_objects_size)]

display_list = [None] * 64
collision_list = [None] * 64

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
	obj.name = "cleared"
	obj.is_initialized = False
	reset_object(obj)
	obj.is_dead = False

def reset_object(obj):
	obj.is_activated = False
	obj.is_displayable = False
	obj.is_collidable = False
	obj.is_boxed = False

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


def collides_background(self, dx, dy):
	DEFAULT = 7
	x = int(self.x + signate(self, dx)) // 16
	# print ('px = %s, x = %s, py = %s, y = %s' % (self.x + signate(self, dx), x, self.y + dy, int(self.y + dy) // 16))
	if x < 0:
		# self.coll_value = DEFAULT
		return DEFAULT
	if x >= layer_A.twidth:
		# self.coll_value = DEFAULT
		return DEFAULT

	yp = int(self.y + dy)
	y = yp // 16
	if y < 0:
		# self.coll_value = DEFAULT
		return DEFAULT
	if y >= layer_A.theight:
		# self.coll_value = DEFAULT
		return DEFAULT

	res = Globs.collision_map[y * layer_A.twidth + x] & 15
	# self.coll_value = res

	if res & 8:
		print ('yp = %X, coll = %X' % (yp, res))
		# half tile
		# GP.halt()
		if yp & 8 and (res & 7 == 7 or res & 7 == self.floor & 7):
			return res
		print ('return 0')
		return 0
	if res == 7 or res & 7 == self.floor & 7:
		return res
	return 0


def get_hijump_impulsion(self):
	x1 = int(self.x + self.back) // 16
	x2 = int(self.x + self.front) // 16
	y = int(self.y) // 16
	
	if not(0 <= y < layer_A.theight and 0 <= x1 < layer_A.twidth):
		return 0

	# bug potentiel : x2 n'est pas forcément > x1 !!!
	i = y * layer_A.twidth + x1

	v = impulsions_table[(Globs.collision_map[i] >> 4) & 15]
	print ('x1 = %s, v = %d' % (x1, v))
	
	if v:
		if x2 != x1:
			w = impulsions_table[(Globs.collision_map[i + x2 - x1] >> 4) & 15]
			print ('x2 = %d, w = %s' % (x2, w))
			GP.halt()
			if w:
				v = max(v, w)
			else:
				return 0
	else:
		return 0

	return v


def get_hijump_down_impulsion(self):
	x1 = int(self.x + self.back) // 16
	x2 = int(self.x + self.front) // 16
	y = int(self.y) // 16

	i = y * layer_A.twidth + x1
	v = impulsions_table[(Globs.collision_map[i] >> 8) & 15]

	# bug potentiel : x2 n'est pas forcément > x1 !!!
	if v:
		if x1 != x2:
			w = impulsions_table[(Globs.collision_map[i + x2 - x1] >> 8) & 15]
			if w:
				v = max(v, w)
			else:
				return 0
	else:
		return 0
	return v


def fix_hpos(self):
	if self.moves_to_left:
		log.write(2, 'left')
		if self.speed_x <= 0:
			log.write(2, 'front: %d' % self.front)
			fixed = (int(self.x - self.front) & 0xFFF0) + self.front + 16
		else:
			log.write(2, 'back: %d' % self.back)
			fixed = (int(self.x - self.back) & 0xFFF0) + self.back - 1
		log.write(2, 'fix_hpos: %d -> %d' % (self.x, fixed))
	else:
		log.write(2, 'right')
		if self.speed_x >= 0:
			log.write(2, 'front: %d' % self.front)
			fixed = (int(self.x + self.front) & 0xFFF0) - self.front - 1
		else:
			log.write(2, 'back: %d' % self.back)
			fixed = (int(self.x + self.back) & 0xFFF0) - self.back + 16
	log.write(2, 'fix_hpos: %d -> %d' % (self.x, fixed))
	self.x = fixed

def fix_hpos_(self, dx):
	if self.moves_to_left:
		fixed = ((int(self.x) - dx) & 0xFFF0) + dx
	else:
		fixed = ((int(self.x) + dx) & 0xFFF0) - dx
	self.x = fixed

def handle_fall(self):
	print ('handle_fall')
	coll = collides_background(self, self.front, 0) | collides_background(self, self.back, 0)

	print ('coll: %X' % self.coll_value)
	if coll:
		old_y = self.y
		print ('!')
		self.y = ((int(self.y)) & 0xFFF0) - 1

		print ('handle_fall: (coll_value = %X) %X -> %X' % (coll, int(old_y), int(self.y))) 

		if coll & 8:
			self.y += 8
			print ('then %X' % self.y)
			# GP.halt()
		else:
			coll = collides_background(self, self.front, 0) | collides_background(self, self.back, 0)
			if coll & 8:
				self.y -= 8
				print ('then %X' % self.y)
				# GP.halt()
			elif coll:
				self.y -= 16
				print ('then %X' % self.y)
				
		print ('end handle_fall')
		return True
	
	return False


def fix_vpos_(self):
	old_y = self.y
	
	self.y = ((int(self.y)) & 0xFFF0) - 1

	print ('fix_vpos: (coll_value = %X) %X -> %X' % (self.coll_value, int(old_y), int(self.y))) 

	if self.coll_value & 8:
		self.y += 8
		print ('then %X' % self.y)
		# GP.halt()
		
	# self.y = ((int(self.y)) & 0xFFF0) - 1


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
	new_object_chunk = Globs.objects_map[(camera.top >> 4) * layer_A.twidth + (camera.left >> 4)]
	# print ('camera tpos = %d, %d' % (camera.left >> 4, camera.top >> 4))
	if (new_object_chunk != Globs.objects_chunk):
	
		Globs.objects_chunk = new_object_chunk
		
		if camera.moves_right: 
			# print ('right')
			introduce_new_object_chunk(Globs.objects_from_left[new_object_chunk])
		else:
			# print ('left')
			introduce_new_object_chunk(Globs.objects_from_right[new_object_chunk])
			
		if camera.moves_up:
			# print ('up')
			introduce_new_object_chunk(Globs.objects_from_bottom[new_object_chunk])
		else: 
			# print ('down')
			introduce_new_object_chunk(Globs.objects_from_top[new_object_chunk])
		

def introduce_new_object_chunk(chunk):

	if chunk:
		# print ('introduce chunk #%s (pos = (%d, %d) : %s' % (chunk, Globs.musashi.x, Globs.musashi.y, Globs.objects_chunks[chunk]))
		# GP.halt()
		
		for i in Globs.objects_chunks[chunk]:
			print ('object: %d' % i)
			
			# if i == 4:
				# print('object %d from chunk %d' % (i, chunk))
				# GP.halt()
			obj = objects[i]
			if obj.is_initialized and not obj.is_activated:
				obj.activate_function(obj)

def update_all_objects_on_screen():
	log.write(1, 'update_all_objects_on_screen: #all = %d' % len(all_objects))
	GP.log_write('updatable objects: %d' % len(all_objects), 0, 0)
	
	log.write(1, "camera : left = %d, right = %d, top = %d, bottom = %d" % (camera.left, camera.right, camera.top, camera.bottom))
	log.refresh_max_updatables(len(all_objects))
	
	display_list_ptr = 0
	collision_list_ptr = 0
	
	for obj in all_objects:
		log.write(1, 'object %d (%s) : %s, bbox = %s, hitbox = %s' % (obj.id_, obj.name, ', '.join([['', 'initialized'][obj.is_initialized], ['', 'activated'][obj.is_activated], ['', 'displayable'][obj.is_displayable], ['', 'collidable'][obj.is_collidable]]), obj.bbox, obj.hitbox))

		if obj.is_activated:
			if camera.virtual_left <= obj.x <= camera.virtual_right\
			and camera.virtual_top < obj.y < camera.virtual_bottom:
				# print ('update object %d' % obj.id_)
				update_object(obj)				

				obj.is_boxed = False
				obj.is_drawn = False
				if obj.is_displayable and camera.left - 16 <= obj.x <= camera.right + 16 and camera.top <= obj.y < camera.bottom + 16:
					display_list[display_list_ptr] = obj
					display_list_ptr += 1
					obj.is_drawn = True
					if obj.is_collidable:
						compute_boxes(obj)
						obj.is_boxed = True
					
			else:
				log.write(2, '[update_all_objects] release %s' % obj.name)
				print('[update_all_objects] release %s (camera = %d -> %d, object = %d' % (obj.name, camera.virtual_left, camera.virtual_right, obj.x))
				if obj.release_function:
					obj.release_function(obj)
	
	display_list[display_list_ptr] = None


def check_collisions(source, source_box_type,
					 targets, target_box_type,
					 do_collision):
	collision_occured = False
	if source.is_collidable and source.is_boxed:
		source_floor = source.floor
		source_box = getattr(source, source_box_type)
		if source_box:
			for target in targets:
				# print ('source: %s, %s | target: %s, %s, %s' % (source.name, source.floor, target.name, target.is_collidable, target.floor))
					
				if target.is_collidable and target.is_boxed and target.floor & 0x7F == source_floor & 0x7F:
					target_box = getattr(target, target_box_type)
					# print ('%s: x = %d, y = %d, box = %s' % (target.name, target.x, target.y, target_box))
					
					if target_box:
						if collision_between_boxes(source_box, target_box):
							# print ('collision between [%s] and [%s]' % (source.name, target.name))
							do_collision(source, target)
							collision_occured = True
	return collision_occured


def compute_by_position(o1, o2):
	if o1.x < o2.x:
		o1.impulsion_x = -1
		o2.impulsion_x = 1
	else:
		o1.impulsion_x = 1
		o2.impulsion_x = -1

def compute_impulsion(o1, o2):
	if o1.speed_x < 0:
		if o2.speed_x >= 0:
			o1.impulsion_x = 1
			o2.impulsion_x = -1
		else:
			compute_by_position(o1, o2)
	
	elif o1.speed_x > 0:
		if o2.speed_x <= 0:
			o1.impulsion_x = -1
			o2.impulsion_x = 1
		else:
			compute_by_position(o1, o2)
	
	else:
		compute_by_position(o1, o2)
		
def musashi_collides_ennemy(friend, ennemy):
	# print ('musashi_collides_ennemy : %s -> %s' % (friend.name, ennemy.name))
	friend.other_object = ennemy
	ennemy.other_object = friend

	compute_impulsion(ennemy, friend)
	
	if friend.collision_function:
		friend.collision_function(friend)
	if ennemy.collision_function:
		ennemy.collision_function(ennemy)

def musashi_frees_hostage(musashi, hostage):
	# print ('musashi_frees_hostage')
	hostage.collision_function(hostage)

def musashi_hits_ennemy(friend, ennemy):
	# print ('musashi_hits_ennemy : %s -> %s' % (friend.name, ennemy.name))

	# print('musashi hits ennemy')
	compute_impulsion(friend, ennemy)
	friend.other_object = ennemy
	ennemy.other_object = friend
	if ennemy.hit_function:
		ennemy.hit_function(ennemy)

def shuriken_hits_ennemy(friend, ennemy):
	# added 2017/10/10
	# try to avoid ennemy ejected in the opposite 
	# direction of the shuriken
	
	if friend.speed_x > 0:
		ennemy.impulsion_x = 1
	else:
		ennemy.impulsion_x = -1

	# friend.collision_function(friend)
	ennemy.other_object = friend
	if ennemy.hit_function:
		ennemy.hit_function(ennemy)

def bullet_hits_musashi(friend, ennemy):
	# print ('bullet_hits_musashi')
	if ennemy.speed_x > 0:
		friend.impulsion_x = 2
	else:
		friend.impulsion_x = -2

	# print('projectile hits musashi')
	friend.other_object = ennemy
	
	friend.hit_function(friend)
	
	if ennemy.collision_function:
		ennemy.collision_function(ennemy)

def ennemy_hits_musashi(friend, ennemy):
	# print('ennemy hits musashi')
	compute_impulsion(ennemy, friend)
	friend.other_object = ennemy
	ennemy.other_object = friend

def handle_collisions():
	check_collisions(Globs.musashi, 'bbox',
					 hostage_objects, 'bbox',
					 musashi_frees_hostage)
	
	check_collisions(Globs.musashi, 'hitbox',
					 ennemy_objects, 'bbox',
					 musashi_hits_ennemy)
	
	for projectile in friend_projectiles:
		if check_collisions(projectile, 'hitbox',
				ennemy_objects, 'bbox',
				shuriken_hits_ennemy):
			projectile.collision_function(projectile)

	if check_collisions(Globs.musashi, 'bbox',
			ennemy_objects, 'hitbox',
			ennemy_hits_musashi):
		Globs.musashi.hit_function(Globs.musashi)
			
	if check_collisions(Globs.musashi, 'bbox',
			ennemy_projectiles, 'hitbox',
			bullet_hits_musashi):
		Globs.musashi.hit_function(Globs.musashi)

	if check_collisions(Globs.musashi, 'bbox',
			ennemy_objects, 'bbox',
			musashi_collides_ennemy):
		Globs.musashi.collision_function(Globs.musashi)

def update_all_objects():
	# 1) Introduces new objects according to camera movement
	introduce_new_objects()
		
	# 2) Updates visible objects, releases invisibles
	update_all_objects_on_screen()

	# 3) collisions between objects
	handle_collisions()


def update_all_sprites():
	# print ("update_all_sprites")
	global _max_dynamics, _max_statics, _max_viewable_dynamics, _max_viewable_statics
	
	Globs.link = 0
	debug = []
	
	_dynamics = _viewable_dynamics = 0
	_statics = _viewable_statics = 0
	
	# we can't use display_list because it'll miss new sprites that'd be created by update_all_objects (projectiles)
	for obj in all_objects: 
		if obj is None:
			break
		
		# print ('updating sprite of object #%d' % obj.id_)
		sprite = obj.sprite

		if sprite:			
			sprite.x = int(obj.x) - camera.left
			sprite.y = int(obj.y) - camera.top
			
			#==============================
			# if obj.is_boxed:
			# deux options :
			# 1) passer is_boxed en parametre de sprite_update, qui devient is_viewable dans sprite_update
			# 2) avoir un champs was_drawn pour savoir si on doit mettre needs_refresh_patterns à True et le faire localement
			# if obj.is_drawn:
				# sprite_update(sprite)
			# else:
				# sprite.is_viewable = False
			sprite_update(sprite)
			
			if sprite.is_dynamic:
				_dynamics += 1
				if sprite.is_viewable:
					_viewable_dynamics += 1
				debug += ['(%02dd at (%d, %d))' % (obj.id_, sprite.x, sprite.y)]
			else:
				_statics += 1
				if sprite.is_viewable:
					_viewable_statics += 1
				debug += ['(%02ds at (%d, %d))' % (obj.id_, sprite.x, sprite.y)]
	else:
		pass
		# print ('object #%d is not displayable' % obj.id_)

	GP.sprite_cache[Globs.link - 1].link = 0
	
	log.displayables += [len(debug)]
	log.write(1, '%d displayables: %s' % (len(debug), ', '.join(debug)))
	GP.log_write('dynamic sprites: %d/%d' % (_viewable_dynamics, _dynamics), 0, 16)
	GP.log_write('static sprites: %d/%d' % (_viewable_statics, _statics), 0, 32)
	
	_max_dynamics = max(_max_dynamics, _dynamics)
	_max_viewable_dynamics = max(_max_viewable_dynamics, _viewable_dynamics)
	_max_statics = max(_max_statics, _statics)
	_max_viewable_statics = max(_max_viewable_statics, _viewable_statics)

	GP.log_write('max static sprites: %d/%d' % (_max_viewable_statics, _max_statics), 0, 64)
	GP.log_write('max dynamic sprites: %d/%d' % (_max_viewable_dynamics, _max_dynamics), 0, 80)


def is_near(self, box, objects):
	floor = self.floor
	x, y, w, h = box
	
	y0 = self.y + y
	y1 = y0 + h

	if self.moves_to_left:
		x1 = self.x - x 
		x0 = x1 - w
	else:
		x0 = self.x + x
		x1 = x0 + w
	
	print ('is_near [moves_to_left = %s] : (%s, %s) -> (%s, %s, %s, %s)' % (self.moves_to_left, self.x, self.y, x0, x1, y0, y1))
	
	for obj in objects:
		# print 'ennemy object #%d' % ennemy.id_
		if obj.is_collidable and obj.is_boxed and obj.floor == floor and obj.bbox and  collision_between_boxes((x0, x1, y0, y1), obj.bbox):
			# if x0 <= obj.x <= x1 and y0 <= obj.y <= y1:
			return True
	return False



def __str__(self):
	return self.name
