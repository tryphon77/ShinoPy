from object import *
from tsprite import *

from res.chars.knife_data import *
from chars import common


def init(entry):
	self = common.init(entry)
	self.name = 'knife at (%d, %d)' % (self.org_x, self.org_y)
	
	self.org_faces_left = entry[4]

	self.hp_max = 1
	self.global_display_box = (-16, -63, 32, 64)
	self.spawn_counter = 240
	
	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[knife] activate object#%d (%s)' % (self.id_, self.name))
	common.activate(self, update_spawn)

def release(self):
	print ('[knife] release: %s' % self.name)
	release_object(self)
	ennemy_objects.remove(self)


def update_spawn(self):
	print ('update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		# common.appear_on_edge(self, init_wait)
		# if self.is_displayable:
		# common.faces_object(self, Globs.musashi, 0)
		if self.org_faces_left and self.x > Globs.musashi.x:
			common.appear_on_edge(self, init_wait)
		elif (not self.org_faces_left) and self.x < Globs.musashi.x:
			common.appear_on_edge(self, init_wait)
		if self.sprite:
			common.faces_object(self, Globs.musashi)


def init_wait(self):
	self.is_collidable = True
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, WAIT)
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_wait

def update_wait(self):
	print ('[%s] update_wait' % self.name)
	print (self.floor, Globs.musashi.floor, self.moves_to_left)
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
	common.half_turn(self)
	set_animation(self.sprite, TURN)
	self.update_function = update_turn

def update_turn(self):
	if self.sprite.is_animation_over:
		init_walk(self)


def init_hit(self):
	print ('[%s] hit' % self.name)
	common.init_hit(self, HIT, update_collision, init_death)
	# self.is_dead = True

	# if collides_background(self, self.front, 1):
		# init_death(self)
	# else:
		# common.init_collision(self, HIT, update_collision)


def init_walk(self):
	self.moves_to_left = self.sprite.is_flipped
	set_physics(self, 2, 0, 0, 0)
	set_animation(self.sprite, WALK)
	self.update_function = update_walk


def attacks_musashi(self):
	#@TODO : factorize
	if self.moves_to_left:
		d = self.x - Globs.musashi.x
	else:
		d = Globs.musashi.x - self.x
	if d < 0 and self.y == Globs.musashi.y:
		init_turn(self)
	elif 0 < d < 48:
		init_stab(self)

def update_walk(self):
	common.update_walk(self, attacks_musashi, init_wait, init_jump, common.half_turn, init_fall)


def init_collision(self):
	#@TODO : fix and factorize for all chars
	print ('[%s] collision' % self.name)
	self.is_dead = False # self.is_hit
	common.init_collision(self, HIT, update_collision)

def update_collision(self):
	common.update_collision(self, init_death, init_walk)


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
	common.update_jump(self, next_state = init_jump_end)

def init_fall(self):
	# print 'punk init_fall'
	common.init_fall(self, JUMP_MAIN, update_jump_main)

def init_jump_end(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, JUMP_END)
	self.update_function = update_jump_end

def update_jump_end(self):
	if self.sprite.is_animation_over:
		init_walk(self)


def init_death(self):
	common.init_death(self, DEAD, update_death)

def update_death(self):
	common.update_death(self, update_spawn)


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

		elif collides_background(self, self.front + 1, 0):
			fix_hpos(self)
			self.speed_x = 0
