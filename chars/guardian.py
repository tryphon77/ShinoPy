from object import *
from tsprite import *

from res.chars.sword_data import *
import random
from chars import common

def init(entry):
	# param2 : counter for walking animation
	# param3 : pointer to hostage. If None, swordman is free
	self = common.init(entry)
	self.name = 'guardian at (%d, %d)' % (self.org_x, self.org_y)
	
	self.hp_max = 1

	self.activate_function = activate
	self.release_function = release
	if entry[4]:
		self.param3 = objects[entry[4]]
	else:
		self.param3 = None

def activate(self):
	hostage = self.param3

	if (not self.is_dead) and (hostage is None or hostage.is_initialized):
		# print ('[guardian] activate object#%d (%s)' % (self.id_, self.name))

		common.activate(self, None)
		common.appear(self, init_stand)
	
	else:
		print ('sword missed because : %s' % hostage)


def release(self):
	common.release(self)

def init_hit(self):
	# print ('[sword] init_hit')
	common.init_hit(self, HIT, update_collision, init_death)

def init_hit_shield(self):
	other = self.other_object
	if other.attack_type & 2:
		if self.moves_to_left ^ other.moves_to_left:
			print ('shield')
			self.x -= signate(self, 2)
			self.sprite.tick += 4
		else:
			common.init_hit(self, an)
	else:
		common.init_hit(self, HIT, update_collision, init_death)

def init_collision(self):
	# print ('[sword] init_collision')
	self.is_dead = False # self.is_hit
	common.init_collision(self, HIT, update_collision)

def update_collision(self):
	# print ('[guardian] update_collision')
	common.update_collision(self, init_death, init_wait)


def init_stand(self):
	# print ('[guardian] init_stand')
	set_animation(self.sprite, random.choice([STAND1, STAND2]))
	set_physics(self, 0, 0, 0, 0)
	self.update_function = update_stand
	self.collision_function = init_collision
	self.hit_function = init_hit
	
def update_stand(self):
	hostage = self.param3
	
	if self.floor == Globs.musashi.floor:
		init_wait(self)

	elif hostage and hostage.is_initialized and abs(hostage.x - self.x) > 64 :
		init_wait(self)

	elif self.sprite.is_animation_over:
		if random.random() < .5:
			if self.sprite.animation_id == STAND1:
				set_animation(self.sprite, STAND2)
			else:
				set_animation(self.sprite, STAND1)
			
def towards_musashi(self):
	d = self.x - Globs.musashi.x
	if d < -64:
		common.faces_right(self, 32)
		init_walk(self)
	elif d < 0:
		common.faces_right(self, 32)
		init_slash(self)
	elif d < 64:
		common.faces_left(self, -32)
		init_slash(self)
	else:
		common.faces_left(self, -32)
		init_walk(self)

def towards_hostage(self):
	hostage = self.param3
	
	if hostage and hostage.is_initialized:
		d = self.x - hostage.x
		if d >= 64:
			common.faces_left(self, -32)
		elif d <= -64:
			common.guardian_faces_right(self, 32)
		else:
			init_stand(self)

def init_wait(self):
	self.hit_function = init_hit_shield
	head_towards(self, Globs.musashi)
	set_physics(self, 0, 0, 0, 0)
	self.param2 = 0
	set_animation(self.sprite, WAIT)
	self.update_function = update_wait

def update_wait(self):
	hostage = self.param3
	if self.sprite.is_animation_over:
		if self.floor == Globs.musashi.floor:
			if hostage and hostage.is_initialized:
				d = abs(self.x - hostage.x)
				if d >= 128:
					if self.x <= hostage.x:
						self.speed_x = 32
					else:
						self.speed_x = -32
					
				if d <= 64:
					towards_musashi(self)
			else:
				towards_musashi(self)
		
		elif hostage and hostage.is_initialized:
			towards_hostage(self)
		else:
			init_stand(self)

def init_walk(self):
	self.hit_function = init_hit_shield
	self.param2 = 0
	set_animation(self.sprite, WALK)
	self.update_function = update_walk
		
def update_walk(self):
	common.update_walk_by_steps(self, walk_offsets, init_wait, common.do_nothing, common.do_nothing, init_fall)
	

def init_slash(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SLASH)
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_slash

	
def update_slash(self):
	if self.sprite.is_animation_over:
		init_stand(self)


def init_fall(self):
	# common.enable_shield(self, sword_box)

	self.accel_y = 0.25
	set_animation(self.sprite, WALK)
	self.update_function = update_fall
	self.hit_function = init_hit_shield

def update_fall(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0)\
			or collides_background(self, self.back, 0):
		fix_vpos(self)
		init_wait(self)


def init_death(self):
	common.init_death(self, DEAD, update_death)
	# release_sword(self)


def update_death(self):
	common.update_death(self, None)
