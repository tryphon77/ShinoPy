from object import *
from tsprite import *

from res.sword_data import *
import random

def init_object(entry):
	# param1 : pointer to hostage. If None, swordman is free
	# param2 : counter for walking animation
	# param3 : pointer to sword object (can block projectiles)
	floor, x, y, hostage = entry[4:]

	if hostage is None or hostage[0] & RESPAWNABLE:
		print ('init swordman at (%d, %d)' % (x, y))
		self = allocate_object()
		self.name = "sword at (%d, %d)" % (x, y)
		
		entry[0] |= ON_SCREEN
		self.object_entry = entry
		ennemy_objects.add(self)
		self.release_function = release
		
		self.status = ACTIVE

		self.x = x
		self.y = y
		self.floor = floor
		self.param1 = hostage

		self.back = -16
		self.front = 16

		self.is_collidable = True

		self.sprite = sprite = allocate_dynamic_sprite()
		sprite.name = "sprite %s" % self.name

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

		self.param3 = init_sword(self)
		
		init_stand(self)
	
	else:
		print ('sword missed because : %s' % hostage)


def release(self):
	sword_object = self.param3
	release_object(sword_object)
	ennemy_objects.remove(sword_object)

	release_object(self)
	self.object_entry[0] &= 0xFE
	ennemy_objects.remove(self)


def init_hit(self):
	# print ('sword init_hit')
	sword = self.param3
	sword.status = DISABLED
	sword.bbox = None
	
	self.is_dead = True

	if collides_background(self, self.front, 1):
		init_death(self)
	else:
		other = self.hit_object
		# print 'other.speed = %f' % other.speed_x

		generic_collision(self)
		
		self.speed_y = -4
		self.accel_y = 0.5

		set_animation(self.sprite, HIT)
		self.update_function = update_collision


def init_collision(self):
	# print ('sword init_collision')

	sword = self.param3
	sword.status = DISABLED
	sword.bbox = None

	self.is_dead = False # self.is_hit
	
	generic_collision(self)

	self.speed_y = -4
	self.accel_y = 0.5

	set_animation(self.sprite, HIT)
	self.update_function = update_collision
	self.collision_function = None
	self.hit_function = None


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


def init_stand(self):
	set_animation(self.sprite, random.choice([STAND1, STAND2]))
	set_physics(self, 0, 0, 0, 0)
	self.update_function = update_stand
	self.collision_function = init_collision
	self.hit_function = init_hit

	sword = self.param3
	sword.status = DISABLED
	sword.bbox = None
	
def update_stand(self):
	if self.floor == Globs.musashi.floor:
		init_walk(self)

	elif self.param1\
		and self.param1[0]\
		and abs(self.param1[1] - self.x) > 64 :
		init_walk_towards_hostage(self)

	elif self.sprite.is_animation_over:
		if random.random() < .5:
			if self.sprite.animation_id == STAND1:
				set_animation(self.sprite, STAND2)
			else:
				set_animation(self.sprite, STAND1)
			

def init_walk(self):
	self.collision_function = init_collision
	self.hit_function = init_hit

	head_towards(self, Globs.musashi)
	set_physics(self, 0, 0, 0, 0)
	self.param2 = 0
	set_animation(self.sprite, WALK)
	self.update_function = update_walk

	sword = self.param3
	sword.status = ACTIVE
	if self.moves_to_left:
		sword.speed_x = -32
	else:
		sword.speed_x = 32
	sword.x = self.x + sword.speed_x
	sword.bbox = compute_box(sword, sword_box)


def init_walk_towards_hostage(self):
	hostage_x = self.param1[1]
	self.moves_to_left = self.sprite.is_flipped = (self.x >= hostage_x)
	set_physics(self, 0, 0, 0, 0)
	self.param2 = 0
	set_animation(self.sprite, WALK)
	self.update_function = update_walk_towards_hostage

def update_walk_towards_hostage(self):
	if self.sprite.new_frame:
		dx = walk_offsets[self.param2]
		if not collides_background(self, self.front + dx, 0):
			self.x += signate(self, dx)
			
			self.param2 += 1
			if self.param2 == 4:
				self.param2 = 0

			if self.param1 and self.param1[0]:
				target_x = self.param1[1]
				if abs(self.x - target_x) <= 64:
					init_stand(self)
					
	elif self.floor == Globs.musashi.floor:
		init_walk(self)


def update_walk_common(self):	
	# print ('sword update_walk_common', self.collision_function, init_collision)
	sword = self.param3

	if collides_background(self, self.front, 1) == 0\
	   and collides_background(self, self.back, 1) == 0:
		init_fall(self)

	elif self.floor != Globs.musashi.floor:
		# if self.param1 and self.param1[0]:
			# init_walk_towards_hostage(self)
		# else:
		init_stand(self)
	
	elif self.moves_to_left:
		d = self.x - Globs.musashi.x
		if d < 0:
			flip(self)
		elif d < 64:
			init_slash(self)
	else:
		d = Globs.musashi.x - self.x
		if d < 0:
			flip(self)
			sword.speed_x = -self.speed_x
		if d < 64:
			init_slash(self)


def update_walk(self):
	sword = self.param3

	if self.sprite.new_frame:
		dx = walk_offsets[self.param2]
		if not collides_background(self, self.front + dx, 0):
			self.x += signate(self, dx)
			
			sword.x = self.x + sword.speed_x
			sword.bbox = compute_box(sword, sword_box)
			
			self.param2 += 1
			if self.param2 == 4:
				self.param2 = 0

			if self.param1 and self.param1[0]:
				target_x = self.param1[1]
				if abs(self.x - target_x) >= 128:
					self.update_function = update_walk_towards_target

	update_walk_common(self)


def update_walk_towards_target(self):
	sword = self.param3

	if self.sprite.new_frame:
		dx = walk_offsets[self.param2]
		if not collides_background(self, self.back - dx, 0):
			self.x -= signate(self, dx)

			sword.x = self.x + sword.speed_x
			sword.bbox = compute_box(sword, sword_box)

			self.param2 += 1
			if self.param2 == 4:
				self.param2 = 0

			if self.param1 and self.param1[0]:
				target_x = self.param1[1]
				if abs(self.x - target_x) <= 96:
					self.update_function = update_walk

	update_walk_common(self)


def init_slash(self):
	sword = self.param3
	sword.status = DISABLED
	sword.bbox = None

	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SLASH)
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_slash

	
def update_slash(self):
	if self.sprite.is_animation_over:
		init_stand(self)


def init_fall(self):
	sword = self.param3
	sword.status = ACTIVE

	self.accel_y = 0.25
	set_animation(self.sprite, WALK)
	self.update_function = update_fall


def update_fall(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0)\
			or collides_background(self, self.back, 0):
		fix_vpos(self)
		init_walk(self)


def init_death(self):
	print ('sword death')
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, DEAD)
	self.object_entry[0] &= 0xFD
	self.update_function = update_death
	self.collision_function = None
	self.hit_function = None

	sword = self.param3
	sword.status = DISABLED
	sword.bbox = None


def update_death(self):
	if self.sprite.is_animation_over:
		# print 'dead'
		release(self)






















def init_walk2(self):
	head_towards(self, Globs.musashi)
	set_physics(self, 3, 0, 0, 0)
	set_animation(self.sprite, WALK)
	self.update_function = update_walk2

def update_walk2(self):
	target = self.param1
	
	if self.new_frame:
		self.x += self.speed_x

	if collides_background(self, self.front, 1) == 0\
	   and collides_background(self, self.back, 1) == 0:
		init_fall(self)

	elif collides_background(self, self.front + 1, -32):
		fix_hpos(self)
		self.speed_x = -self.speed_x
		# init_walk(self)

	elif self.floor != Globs.musashi.floor:
		init_stand(self)
	
	elif target:
		if self.moves_to_left:
			d = target.x - self.x
			if x > 128:
				init_back(self)
		else:
			d = self.x - target.x
			if x > 128:
				init_back(self)
			
	elif self.moves_to_left:
		d = self.x - Globs.musashi.x
		if d < 0:
			flip(self)
		elif d < 32:
			init_slash(self)
	else:
		d = Globs.musashi.x - self.x
		if d < 0:
			flip(self)
		if d < 32:
			init_slash(self)

def init_back(self):
	self.speed_x = -self.speed_x
	self.update_function = update_back

def update_back(self):
	target = self.param1
	
	if self.new_frame:
		self.x += self.speed_x

	if self.floor == Globs.musashi.floor:
		head_towards(Globs.musashi)
		
		# check if near enough to hostage
		if self.moves_to_left:
			d = target.x - self.x
			if d < 96:
				init_walk2(self)
		else:
			d_target = self.x - target.x
			if x < 96:
				init_walk2(self)

		# check if near to Musashi and attack
		d = abs(Globs.musashi.x - self.x)
		if d < 32:
			head_towards(Globs.musashi)
			init_slash(self)

	else:
		init_stand(self)
	
	# à réfléchir : on se tourne vers musashi
	
			

def init_sword(char):
	# param1 : pointer to char
	floor, x, y = char.floor, char.x, char.y

	print ('init sword at (%d, %d)' % (x, y))
	self = allocate_object()
	
	ennemy_objects.add(self)

	self.release_function = None
	
	self.status = ACTIVE

	if char.moves_to_left:
		self.speed_x = -32
	else:
		self.speed_x = 32
		
	self.x = x + self.speed_x
	self.y = y
	self.floor = floor

	self.back = -8
	self.front = 8

	self.is_collidable = True

	self.sprite = None
	
	self.update_function = None
	
	return self

