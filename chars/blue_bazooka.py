from object import *
from tsprite import *

from res.chars.bazooka_data import *
from chars import common
from chars.rocket import *


def init(entry):
	self = common.init(entry, sprite_data_blue)
	self.name = 'blue bazooka at (%d, %d)' % (self.org_x, self.org_y)
	
	self.param1 = entry[5]

	# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	# priority problem
	
	self.hp_max = 2
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 240
	self.scope = (64, 128)
	
	# param1: range in pixels
	# param2: range_ticks
	self.param2 = self.param1
	
	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)
	self.tick = 0 # ????????????? dans common.activate ?
	self.is_collidable = True
	self.collision_function = init_collision
	self.hit_function = init_hit

def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn

def update_spawn(self):
	print ('update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		if self.org_faces_left and self.x > Globs.musashi.x:
			common.appear(self, init_wait)
			self.speed_x = -1
			self.moves_to_left = True			
		elif (not self.org_faces_left) and self.x < Globs.musashi.x:
			common.appear(self, init_wait)
			self.speed_x = 1
		if self.sprite:
			common.faces_object(self, Globs.musashi)
	

def init_wait(self):
	self.is_collidable = True
	set_animation(self.sprite, WAIT)
	self.update_function = update_wait

def update_wait(self):
	if self.sprite.is_animation_over:
		if self.param1:
			if self.floor == Globs.musashi.floor:
				common.moves_object(self, Globs.musashi, 1)
			else:
				self.param2 -= 1
				if self.param2 <= 0:
					if self.speed_x < 0:
						self.speed_x = 1
					else:
						self.speed_x = -1				
					self.param2 = self.param1
			init_walk(self)
		elif abs(self.x - Globs.musashi.x) < 200:
			common.faces_object(self, Globs.musashi)
			init_shoot_rocket(self)


# collision and death

def init_collision(self):
	print ('[%s] collision' % self.name)
	self.is_dead = False
	common.init_collision(self, HIT, update_collision)

def init_hit(self):
	print ('[%s] hit' % self.name)
	common.init_hit(self, HIT, update_collision, init_death)

def update_collision(self):
	common.update_collision(self, init_death, init_wait)

def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	common.update_death(self, None)

# walk

def init_walk(self):		
	set_animation(self.sprite, WALK)
	self.update_function = update_walk


def update_walk(self):
	common.faces_object(self, Globs.musashi)
	
	self.x += self.speed_x

	if collides_background(self, self.front, 1) == 0 and collides_background(self, self.back, 1) == 0:
		self.update_function = init_fall

	elif collides_background(self, self.front + 1, 0) or collides_background(self, self.back - 1, 0):
		init_jump(self)

	elif self.sprite.is_animation_over:
		init_shoot_rocket(self)


# jump and fall

def init_jump(self):
	self.speed_y = -8
	self.accel_y = .25
	set_animation(self.sprite, JUMP)
	self.update_function = update_jump
	
def init_fall(self):
	common.init_fall(self, None, update_jump)

def update_jump(self):
	print ('bazooka vpos = %X' % self.sprite.vpos)
	common.update_jump(self, next_state = init_walk)

# shoot_rocket

def init_shoot_rocket(self):
	set_animation(self.sprite, SHOOT_ROCKET)
	self.update_function = update_shoot_rocket

def update_shoot_rocket(self):
	if self.sprite.total_ticks_in_animation == 30:
		print('FIRE !')
		throw_rocket(self)
	
	elif self.sprite.is_animation_over:
		init_wait(self)

def throw_rocket(self):
	rocket = init_rocket()
	if rocket.sprite:
		if self.sprite.is_flipped:
			common.moves_left(rocket, -2)
			rocket.x = self.x - 32
		else:
			common.moves_right(rocket, 2)
			rocket.x = self.x + 32
		rocket.y = self.y - 36
		rocket.floor = self.floor


