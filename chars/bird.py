from object import *
from tsprite import *

from res.chars.bird_data import *
from chars import common


def init(entry):
	self = common.init(entry, sprite_data)
	self.name = 'bird at (%d, %d)' % (self.org_x, self.org_y)

	self.front = 8
	self.back = -8
	
	self.hp_max = 1
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 600
	
	self.accel_y = .25
	self.scope = (128, 255)

	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)
	self.is_collidable = True
	self.collision_function = None
	self.hit_function = init_hit
	
def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn

def update_spawn(self):
	common.update_spawn(self, appear)

def appear(self):
	common.appear(self, None)
	if self.org_faces_left:
		common.faces_left(self)
	
	if self.y >= camera.bottom:
		init_wait(self)
	else:
		init_fly(self)

# dive

def init_dive(self):
	print ('[%s] init_dive' % self.name)
	self.speed_y = 0
	self.accel_y = .25
	set_animation(self.sprite, FALL)
	self.update_function = update_dive

def update_dive(self):
	self.speed_y += self.accel_y
	self.speed_y = min(self.speed_y, 3)
	self.y += self.speed_y
	if handle_fall(self):
		init_fly_up(self)
	elif self.y - camera.bottom >= 64:
		init_wait(self)

def init_fly_up(self):
	self.speed_y = 0
	self.accel_y = -.25
	set_animation(self.sprite, FALL)
	self.update_function = update_fly_up

def update_fly_up(self):
	self.speed_y += self.accel_y
	self.speed_y = max(self.speed_y, -3)
	self.y += self.speed_y
	if self.sprite.total_ticks_in_animation >= 32:
		init_turn_down(self)
	

# turn

def init_turn_down(self):
	common.faces_object(self, Globs.musashi)
	self.speed_x = 0
	self.speed_y = 0
	self.accel_y = 1/8
	set_animation(self.sprite, TURN_DOWN)
	self.update_function = update_turn_down

def init_turn_up(self):
	common.faces_object(self, Globs.musashi)
	self.speed_x = 0
	self.accel_y = -1/8
	set_animation(self.sprite, TURN_UP)
	self.update_function = update_turn_up

def update_turn_down(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y
	handle_fall(self)
	
	# print (self.x, self.y)
	# GP.halt()
	
	if self.sprite.is_animation_over:
		init_fly(self)
		
def update_turn_up(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y
	
	# print (self.x, self.y)
	# GP.halt()
	
	if self.sprite.is_animation_over:
		init_dive(self)

# fly
		
def init_fly(self):
	print ('[%s] init_fly' % self.name)
	self.accel_y = -1/16
	self.speed_y = 2
	self.speed_x = signate(self, 2)
	set_animation(self.sprite, FLY)
	self.update_function = update_fly
	# pendant 64 frames

def update_fly(self):	
	self.x += self.speed_x
	if collides_background(self, 8, 0):
		fix_hpos(self)
	
	self.speed_y += self.accel_y
	self.y += self.speed_y
	handle_fall(self)
	
	# print (self.sprite.total_ticks_in_animation, self.x, self.y)
	# GP.halt()

	if self.sprite.total_ticks_in_animation >= 64:
		init_turn_up(self)

# wait and attack

def init_wait(self):
	print ('[%s] init_wait' % self.name)
	set_animation(self.sprite, FLY)
	self.update_function = update_wait

def update_wait(self):
	print ('[%s] update_wait' % self.name)
	print (self.moves_to_left, self.x, Globs.musashi.x)
	
	if self.sprite.is_animation_over and (abs(self.x - Globs.musashi.x) < 64):
		init_attack(self)

def init_attack(self):
	print ('[%s] init_attack' % self.name)
	self.speed_x = signate(self, 2)
	self.speed_y = -8
	self.accel_y = -.25
	self.update_function = update_attack

def update_attack(self):
	print ('[%s] update_attack' % self.name)

	self.x += self.speed_x
	if collides_background(self, 8, 0):
		fix_hpos(self)

	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.y < camera.top:
		init_turn_down(self)

# collision and death

def init_hit(self):
	print ('[%s] hit' % self.name)
	common.init_hit(self, HIT, update_collision, init_death)

def update_collision(self):
	common.update_collision(self, init_death, init_wait)

def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	common.update_death(self, release)


