from object import *
from tsprite import *

from res.chars.ninja_data import *
from chars import common
from chars import ninja_common

import random

class RollingParams:
	def __init__(self, entry):
		self.dx, self.dy, self.delay = entry

def init(entry):
	self = common.init(entry, sprite_data_blue)
	self.name = "rolling ninja at (%d, %d)" % (self.org_x, self.org_y)

	# params :
	self.params = RollingParams(entry[5])
	
	self.activate_function = activate
	self.release_function = release
	self.collision_function = None
	self.hit_function = init_hit_blade_front

	self.hp_max = 1
	self.spawn_counter = 3000
	
	self.update_function = None

	return self

def activate(self):
	print ('[%s] activate' % self.name)
	GP.halt()
	common.activate(self, update_spawn)

def release(self):
	print ('[%s] release' % self.name)
	GP.halt()
	common.release(self)

def update_spawn(self):
	common.update_spawn(self, appear)

def appear(self):
	common.appear(self, None)
	init_roll(self)

def init_roll(self):
	log.write(2, '[%s] init_roll' % self.name)
	set_animation(self.sprite, ROLL)
	self.speed_x = self.params.dx
	self.speed_y = self.params.dy
	self.update_function = update_roll

def update_roll(self):
	self.x += self.speed_x
	self.y += self.speed_y

	if collides_background(self, 8, -16): # or collides_background(self, 16, -27):
		self.y = ((int(self.y)) & 0xFFF0) - 1
		self.speed_y = -self.speed_y
		# print ('v coll')
		# GP.halt()
		
	if collides_background(self, 16, -16): # or collides_background(self, 16, -50):
		common.half_turn(self)
		# print ('h coll')
		# GP.halt()
		
	if self.sprite.frame in [11, 12]:
		self.hit_function = init_hit_blade_back
	else:
		self.hit_function = init_hit_blade_back
		

# collision and death

def init_hit(self):
	common.init_hit(self, HIT, update_collision, init_death)

def init_hit_blade_front(self):
	blade_box = compute_box(self, (16, -50, 8, 24))
	# print (self.moves_to_left)
	# print (self.x, blade_box)
	# GP.halt()
	other = self.other_object
	if other.attack_type & 2 and collision_between_boxes(blade_box, other.hitbox):
		print ('shield')
	else:
		init_hit(self)
	
def init_hit_blade_back(self):
	blade_box = compute_box(self, (-24, -50, 8, 24))
	# print (self.moves_to_left)
	# print (self.x, blade_box)
	# GP.halt()
	other = self.other_object
	if other.attack_type & 2 and collision_between_boxes(blade_box, other.hitbox):
		print ('shield')
	else:
		init_hit(self)
	

# def init_collision(self):
	# ninja_common.init_collision(self, HIT, update_collision)

def update_collision(self):
	common.update_collision(self, init_death, None)

def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	ninja_common.update_death(self, update_spawn)
