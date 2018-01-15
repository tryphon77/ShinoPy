from object import *
from tsprite import *

from res.chars.spider_data import *
from chars import common


def init(entry):
	self = common.init(entry)
	self.name = 'spider at (%d, %d)' % (self.org_x, self.org_y)
	
	self.org_faces_left = entry[4]

	self.hp_max = 1
	self.global_display_box = (-16, -63, 32, 64) # a modifier
	self.spawn_counter = 240
	
	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, None)
	common.appear(self, None)
	common.faces_object(self, Globs.musashi)
	init_climb(self)

def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

# climb

def init_climb(self):
	print ('[%s] init_climb' % self.name)

	if self.x > Globs.musashi.x:
		self.speed_x = -.5
	else:
		self.speed_x = .5
	self.speed_y = 1
	set_animation(self.sprite, CLIMB)
	self.collision_function = init_death_1
	self.hit_function = init_death_1
	self.update_function = update_climb

def update_climb(self):
	print ('[%s] update_climb' % self.name)

	self.x += self.speed_x
	self.y += self.speed_y
	
	if self.sprite.is_animation_over:
		if Globs.musashi.y - self.y < 128:
			init_wait(self)


# wait

def init_wait(self):
	print ('[%s] init_wait' % self.name)

	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, WAIT)
	self.update_function = update_wait

def update_wait(self):
	if abs(self.x - Globs.musashi.x) < 56:
		init_flop(self)

# flop

def init_flop(self):
	print ('[%s] init_flop' % self.name)

	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, FLOP)
	self.update_function = update_flop

def update_flop(self):
	if self.sprite.is_animation_over:
		init_fall(self)

def init_fall(self):		
	print ('[%s] init_fall' % self.name)

	if self.x < Globs.musashi.x:
		self.speed_x = 1
	else:
		self.speed_x = -1
	
	self.speed_y = 5
	self.accel_y = .5
	set_animation(self.sprite, FALL)
	self.update_function = update_jump

# def update_fall(self):
	# common.update_fall(self, init_fall_end)

def init_fall_end(self):
	print ('[%s] init_fall_end' % self.name)

	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, RECEPTION)
	self.hit_function = init_death_2
	self.update_function = update_fall_end
	
def update_fall_end(self):
	if self.sprite.is_animation_over:
		init_crouch(self)
	
def init_crouch(self):
	print ('[%s] init_crouch' % self.name)

	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, CROUCH)
	self.update_function = update_crouch

def update_crouch(self):
	if self.sprite.is_animation_over:
		init_jump(self)


# jump

def init_jump(self):
	common.moves_object(self, Globs.musashi, 4)
	self.speed_y = -7.5
	self.accel_y = .5
	set_animation(self.sprite, JUMP)
	self.update_function = update_jump

def update_jump(self):
	common.update_jump(self, next_state = init_fall_end)
	



	
def init_death_1(self):
	common.init_death(self, DEATH1, update_death)

def init_death_2(self):
	common.init_death(self, DEATH2, update_death)

def update_death(self):
	common.update_death(self, None)


