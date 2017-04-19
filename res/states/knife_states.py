from object import *
from tsprite import *

from res.knife_data import *


def init_object(entry):
	floor, x, y, _ = entry[4:]
	print ('init knife at (%d, %d)' % (x, y))

	self = allocate_object()
	self.name = "knife at (%d, %d)" % (x, y)
	
	entry[0] |= ON_SCREEN
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
	
	init_wait(self)


def release(self):
	release_object(self)
	self.object_entry[0] &= 0xFE
	print ('knife release: %s' % self.object_entry)
	ennemy_objects.remove(self)


def init_wait(self):
	self.is_collidable = True
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, WAIT)
	self.update_function = update_wait

def update_wait(self):
	if self.floor == Globs.musashi.floor:
		if self.moves_to_left:
			if Globs.musashi.x > self.x:
				init_turn(self)
			else:
				init_walk(self)
		else:
			if Globs.musashi.x > self.x:
				init_walk(self)
			else:
				init_turn(self)


def init_turn(self):
	flip(self)
	set_animation(self.sprite, TURN)
	self.update_function = update_turn

def update_turn(self):
	if self.sprite.is_animation_over:
		init_walk(self)


def init_hit(self):
	print ('knife hit_function')
	self.is_dead = True

	if collides_background(self, self.front, 1):
		init_death(self)
	else:
		other = self.hit_object

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


def init_walk(self):
	self.moves_to_left = self.sprite.is_flipped
	set_physics(self, 2, 0, 0, 0)
	set_animation(self.sprite, WALK)
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
		init_turn(self)

	elif collides_background(self, self.front + 1, 0):
		fix_hpos(self)
		init_jump(self)

	elif self.floor != Globs.musashi.floor:
		init_wait(self)
	
	else:
		#@TODO : factorize
		if self.moves_to_left:
			d = self.x - Globs.musashi.x
		else:
			d = Globs.musashi.x - self.x
		if d < 0 and self.y == Globs.musashi.y:
			init_turn(self)
		elif 0 < d < 48:
			init_stab(self)


def init_collision(self):
	#@TODO : fix and factorize for all chars
	print ('knife collision')
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


def init_jump(self):
	set_physics(self, 1, 0, 0, 0)
	set_animation(self.sprite, JUMP_BEGIN)
	self.update_function = update_jump

def update_jump(self):
	if self.sprite.is_animation_over:
		init_jump_main(self)

def init_jump_main(self):
	self.speed_y = -5.5
	self.accel_y = 0.25
	set_animation(self.sprite, JUMP_MAIN)
	self.update_function = update_jump_main

def update_jump_main(self):
	#@TODO : factorize
	if self.moves_to_left:
		d = self.x - Globs.musashi.x
	else:
		d = Globs.musashi.x - self.x
	if 0 < d < 48:
		set_animation(self.sprite, STAB_JUMP)

	self.x += self.speed_x

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		print (self.speed_x)

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if self.speed_y >= 0:
		init_fall(self)


def init_fall(self):
	# print 'punk init_fall'
	self.accel_y = 0.25
	set_animation(self.sprite, JUMP_MAIN)
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
		init_jump_end(self)

def init_jump_end(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, JUMP_END)
	self.update_function = update_jump_end

def update_jump_end(self):
	if self.sprite.is_animation_over:
		init_walk(self)


def init_death(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, DEAD)
	self.update_function = update_death
	self.collision_function = None
	self.hit_function = None


def update_death(self):
	if self.sprite.is_animation_over:
		# print 'dead'
		release(self)


def init_stab(self):
	set_animation(self.sprite, STAB_STAND)
	self.update_function = update_attack


def update_attack(self):
	if self.sprite.is_animation_over:
		init_walk(self)
	
	else:
		self.x += self.speed_x
		if collides_background(self, self.front, 1) == 0\
		   and collides_background(self, self.back, 1) == 0:
			init_fall(self)

		elif collides_background(self, self.front + 1, -32):
			fix_hpos(self)
			self.speed_x = 0
