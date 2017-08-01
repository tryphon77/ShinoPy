from object import *
from tsprite import *


def init(entry, sprite_data = None):
	obj_type, floor, x, y, _ = entry

	self = allocate_object(objects)
	
	self.is_initialized = True
	
	self.org_x = x
	self.org_y = y
	self.org_floor = floor

	if sprite_data:
		self.sprite_data = sprite_data
	else:
		self.sprite_data = obj_type.sprite_data
	
	self.back = -10
	self.front = 10

	self.tick = 0
	self.update_function = None
	
	return self


def activate(self, next_state):
	print ('[common] activate object#%d (%s)' % (self.id_, self.name))	

	self.is_activated = True
	all_objects.add(self)

	self.floor = self.org_floor
	self.x = float(self.org_x)
	self.y = float(self.org_y)
	
	self.update_function = next_state


def update_spawn(self, next_state):
	# print ('update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		
		next_state(self)


def appear_on_edge(self, next_action):
	if (camera.right <= self.org_x < camera.virtual_right)\
		or (camera.virtual_left < self.org_x <= camera.left):
			appear(self, next_action)
		
def appear(self, next_action, list_ = ennemy_objects, is_dynamic = True):
	self.is_dead = False
	
	self.x = self.org_x
	self.y = self.org_y
	self.floor = self.org_floor
	self.hp = self.hp_max

	if is_dynamic:
		self.sprite = sprite = allocate_dynamic_sprite()
	else:
		self.sprite = sprite = allocate_static_sprite()	

	if sprite:
		print ('object %s appears' % self.name)
		self.is_displayable = True
		self.is_collidable = True
		
		list_.add(self)
		sprite.name = "sprite %s" % self.name

		sprite.status = 1
		sprite.x = self.x
		sprite.y = self.y

		sprite.data = self.sprite_data
		
		sprite.frame = -1
		sprite.bbox = (-6, 0, 16, 64)
		
		next_action(self)
	else:
		print ('object %s sprite could not be allocated' % self.name)


def release(self):
	release_object(self)
	ennemy_objects.remove(self)


def faces_left(self, speed):
	self.moves_to_left = True
	self.sprite.is_flipped = True
	self.speed_x = speed
	
def faces_right(self, speed):
	self.moves_to_left = False
	self.sprite.is_flipped = False
	self.speed_x = speed




def init_hit(self, hit_anim, next_state, death_action):
	self.hp -= 1
	self.is_dead = (self.hp == 0)

	self.is_collidable = False

	if self.is_dead and collides_background(self, self.front, 1):
		death_action(self)
	else:
		init_collision(self, hit_anim, next_state)
		
##########
def do_nothing(self):
	pass

def half_turn(self):
	fix_hpos(self)
	
	self.moves_to_left = not self.moves_to_left
	self.sprite.is_flipped = not self.sprite.is_flipped
	
	self.speed_x = -self.speed_x
		
def update_walk(self, same_level_action, different_level_action, face_obstacle_action, face_wall_action, hole_action):

	self.x += self.speed_x

	if collides_background(self, self.front, 1) == 0\
	   and collides_background(self, self.back, 1) == 0:
		hole_action(self)

	elif collides_background(self, self.front + 1, -32):
		face_wall_action(self)

	elif collides_background(self, self.front + 1, 0):
		face_obstacle_action(self)

	elif self.floor == Globs.musashi.floor:
		same_level_action(self)
	
	else:
		different_level_action(self)

def update_walk_by_steps(self, offset_table, end_anim_action, face_obstacle_action, face_wall_action, hole_action):
	if self.sprite.new_frame:

		dx = offset_table[self.param2]
		if dx == 0:
			self.param2 = 0
			end_anim_action(self)
		else:
			self.param2 += 1
			
			if collides_background(self, self.front + dx, 0):
				face_obstacle_action(self)
		
			elif collides_background(self, self.front + 1, -32):
				face_wall_action(self)

			else:
				if self.speed_x < 0:
					self.x -= dx
				else:
					self.x += dx
					
				if collides_background(self, self.front, 1) == 0\
				and collides_background(self, self.back, 1) == 0:
					hole_action(self)

		
def init_collision(self, hit_anim, next_state):
	print('[common.init_collision] on object %s' % self.name)
	
	print ('all_objects:')
	for o in all_objects:
		print (o.name, o.is_initialized, o.is_activated, o.is_displayable, o.is_collidable)
	print ('ennemy_objects:')
	for o in ennemy_objects:
		print (o.name, o.is_initialized, o.is_activated, o.is_displayable, o.is_collidable)
	# self.is_dead = False # self.is_hit

	# generic_collision(self)

	# other = self.other_object
	# if other.moves_to_left:
		# self.speed_x = -2
	# else:
		# self.speed_x = 2

	self.speed_y = -4
	self.accel_y = 0.5

	set_animation(self.sprite, hit_anim)
	self.update_function = next_state
	# self.collision_function = None
	# self.hit_function = None


def update_collision(self, death_state, next_state):

	self.x += self.speed_x

	if collides_background(self, self.front, 0)\
	or collides_background(self, self.back, 0):
		fix_hpos(self)

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0) or\
			collides_background(self, self.back, 0):
		fix_vpos(self)
		if self.is_dead:
			death_state(self)
		else:
			self.is_collidable = True
			next_state(self)


def update_jump(self, fall_state):
	self.x += self.speed_x

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = signate(self, 1)

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if self.speed_y >= 0:
		fall_state(self)


def init_fall(self, fall_anim, update_state):
	self.accel_y = 0.25
	if fall_anim:
		set_animation(self.sprite, fall_anim)
	self.update_function = update_state


def update_fall(self, next_state):
	self.x += self.speed_x

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = 0

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0)\
			or collides_background(self, self.back, 0):
		fix_vpos(self)
		next_state(self)


def init_death(self, death_anim, next_state):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, death_anim)
	self.update_function = next_state
	self.is_collidable = False

def update_death(self, next_state):
	if self.sprite.is_animation_over:
		self.is_displayable = False
		release_sprite(self.sprite)
		ennemy_objects.remove(self)
		self.sprite = None
		self.tick = 80
		self.update_function = next_state




# shield

def init_shield(char, collision_function):
	# param1 : pointer to char
	floor, x, y = char.floor, char.org_x, char.org_y
	self = allocate_object(auxiliary_objects)
	self.name = 'saber of %s' % char.name
	
	self.param1 = char

	self.is_initialized = True
	self.is_activated = False
	self.is_displayable = False
	self.is_collidable = False

	print ('[common.init_shield] from %s at (%d, %d)' % (char.name, x, y))

	self.x = x
	self.y = y
	self.floor = floor

	self.back = -8
	self.front = 8

	self.release_function = None	
	self.collision_function = collision_function
	self.hit_function = collision_function

	return self
	
def activate_shield(self):
	print ('[%s] activate_shield' % self.name)
	ennemy_objects.add(self)
	all_objects.add(self)

	self.is_activated = True
	self.is_collidable = True
	
	self.sprite = None
	self.update_function = None

	# self.release_function = release_sword

def release_shield(self):
	# print ('[sword] release_sword')
	shield = self.param1
	release_object(shield)
	ennemy_objects.remove(shield)

# =================

def enable_shield(self, box):
	shield = self.param1
	shield.is_collidable = True
	shield.global_bbox = box
	shield.global_hitbox = box
	shield.floor = self.floor
	shield.moves_to_left = self.moves_to_left
	shield.x = self.x
	shield.y = self.y
	
def update_shield(self):
	shield = self.param1
	shield.moves_to_left = self.moves_to_left
	shield.x = self.x
	shield.y = self.y
	
def disable_shield(self):
	shield = self.param1
	shield.is_collidable = False
