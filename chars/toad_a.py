from object import *
from tsprite import *

from res.chars.toad_a_data import *
from chars import common


def init(entry):
	self = common.init(entry, sprite_data)
	self.name = 'toad A at (%d, %d)' % (self.org_x, self.org_y)
	self.scope = (32, 40)

	# param1 : friend
	# param2 : is friend on back
	friend_id = entry[5]
	if friend_id:
		self.param1 = objects[friend_id]
	else:
		self.param1 = None
	self.param2 = False
	
	self.front = 8
	self.back = -8
	
	self.hp_max = 1
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 120
	
	self.accel_y = .25

	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)
	# self.tick = 0 # ????????????? dans common.activate ?
	self.is_collidable = True
	self.collision_function = None
	self.hit_function = init_hit
	
def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn

def update_spawn(self):
	print ('[%s] update_spawn (tick = %d)' % (self.name, self.tick))
	common.update_spawn(self, appear)

def appear(self):
	common.appear(self, None)
	if self.org_faces_left:
		common.faces_left(self)
	if self.param1:
		self.param2 = True
		init_wait(self)
	else:
		init_jump_mid(self)


# wait

def init_wait(self):
	set_animation(self.sprite, WAIT)
	self.update_function = update_wait

def update_wait(self):
	if self.param1.is_dead:
		self.update_function = update_jump_mid
	# print ('[%s] update_wait pos = (%d, %d)' % (self.name, self.x, self.y))
	pass

# collision and death

def init_collision(self):
	# print ('[%s] collision' % self.name)
	self.is_dead = False
	common.init_collision(self, HIT, update_collision)

def init_hit(self):
	# print ('[%s] hit' % self.name)
	common.init_hit(self, HIT, update_collision, init_death)

def update_collision(self):
	common.update_collision(self, init_death, init_wait)

def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	common.update_death(self, None)


def init_jump(self):
	set_animation(self.sprite, JUMP_START)
	self.update_function = update_jump
	
def update_jump(self):
	if self.sprite.is_animation_over:
		init_jump_mid(self)

def init_jump_mid(self):
	print ('[%s] init_jump_mid' % self.name)
	self.speed_x = signate(self, 4)
	self.accel_y = 9/8
	self.speed_y = -13.5
	set_animation(self.sprite, JUMP_MID)
	self.update_function = update_jump_mid

def update_jump_mid(self):
	print ('[%s] update_jump_mid pos = (%d, %d) speed = (%d, %d) accel = (%d, %d)' % (self.name, self.x, self.y, self.speed_x, self.speed_y, self.accel_x, self.accel_y))
	common.update_jump(self, next_state = init_jump_end)

def init_jump_end(self):
	set_animation(self.sprite, JUMP_END)
	self.update_function = update_jump_end

def update_jump_end(self):
	if self.sprite.is_animation_over:
		init_jump(self)	




