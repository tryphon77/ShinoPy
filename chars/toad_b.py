from object import *
from tsprite import *

from res.chars.toad_b_data import *
from chars import common
from chars import toad_a

def init(entry):
	self = common.init(entry, sprite_data)
	self.name = 'toad B at (%d, %d)' % (self.org_x, self.org_y)

	# friend (other toad)
	if entry[5]:
		self.param1 = objects[entry[5]]
	else:
		self.param1 = None
	
	self.front = 8
	self.back = -8
	
	self.hp_max = 1
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 120
	
	self.scope = (32, 128)
	
	self.accel_y = .25

	self.activate_function = activate
	self.release_function = release

def activate(self):
	# print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)
	self.tick = 0 # ????????????? dans common.activate ?
	self.is_collidable = True
	self.collision_function = None
	self.hit_function = init_hit
	
def release(self):
	# print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn

def update_spawn(self):
	common.update_spawn(self, appear)

def appear(self):
	common.appear(self, None)
	if self.org_faces_left:
		common.faces_left(self)
	if self.param1:
		self.param2 = True
		init_wait(self)
	else:
		init_jump(self)


# wait

def init_wait(self):
	set_animation(self.sprite, WAIT)
	self.update_function = update_wait
	self.speed_y = 0
	self.accel_y = .25

def update_wait(self):
	print ('[%s] update_wait (param1 = %s)' % (self.name, self.param1))
	print ('[%s] pos = (%s, %s) speed = (%s, %s) accel = (%s, %s)' % (self.name, self.x, self.y, self.speed_x, self.speed_y, self.accel_x, self.accel_y))
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if handle_fall(self):
		if abs(Globs.musashi.x - self.x) < 128:
			init_jump(self)
			if not self.param1.is_dead:
				toad_a.init_jump(self.param1)
		elif self.param1.is_dead:
			init_jump(self)
	else:
		self.param1.speed_y = self.speed_y
		self.param1.y = self.y - 22


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


# jump and fall

def init_jump(self):
	set_animation(self.sprite, JUMP_START)
	self.update_function = update_jump
	
def update_jump(self):
	if self.sprite.is_animation_over:
		init_jump_mid(self)

def init_jump_mid(self):
	self.speed_x = 0
	self.speed_y = -10
	self.accel_y = 1
	set_animation(self.sprite, JUMP_MID)
	self.update_function = update_jump_mid

def update_jump_mid(self):
	common.update_jump(self, next_state = init_jump)

