from object import *
from tsprite import *

from res.chars.bazooka_data import *
from chars import common
from chars.rocket import *


def init(entry):
	self = common.init(entry, sprite_data_green)
	self.name = 'green bazooka at (%d, %d)' % (self.org_x, self.org_y)

	# self.param1 : True if mobile
	self.param1 = entry[5]
	
	self.hp_max = 2
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 240
	
	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)
	self.tick = 0
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
	common.faces_object(self, Globs.musashi)
	if self.sprite.is_animation_over:
		if self.param1:
			init_walk(self)
		elif abs(Globs.musashi.x - self.x) < 64:
			init_attack(self)
		else:
			init_shoot_ball(self)


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

	else:
		d = Globs.musashi.x - self.x
		
		if d <= -112:
			init_shoot_ball(self)
		elif d < 0:
			self.speed_x = 1
		elif d < 112:
			self.speed_x = -1
		else:
			init_shoot_ball(self)		


# jump and fall

def init_jump(self):
	self.speed_y = -8
	self.accel_y = .25
	set_animation(self.sprite, JUMP)
	self.update_function = update_jump
	
def init_fall(self):
	common.init_fall(self, None, update_jump)

def update_jump(self):
	common.update_jump(self, next_state = init_walk)

# shoot_rocket

def init_shoot_ball(self):
	set_animation(self.sprite, SHOOT_BALL)
	self.update_function = update_shoot_ball

def update_shoot_ball(self):
	if self.sprite.total_ticks_in_animation == 48:
		print('FIRE !')
		throw_ball(self)
	
	elif self.sprite.is_animation_over:
		init_wait(self)

def throw_ball(self):
	ball = init_ball()
	if ball.sprite:
		if self.sprite.is_flipped:
			common.moves_left(ball, -2)
			ball.x = self.x - 8
		else:
			common.moves_right(ball, 2)
			ball.x = self.x + 8
		ball.y = self.y - 60
	ball.floor = self.floor


# attack

def init_attack(self):
	self.speed_x = 0
	set_animation(self.sprite, ATTACK)
	self.update_function = update_attack

def update_attack(self):
	if self.sprite.is_animation_over:
		init_wait(self)
