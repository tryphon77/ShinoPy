from object import *
from tsprite import *

from res.chars.sword_data import *
import random
from chars import common

def init(entry):
	# param2 : True if guardian faces right
	# param3 : pointer to hostage. If None, swordman is free
	# param4 : pointer to state before blocking
	self = common.init(entry, pink_sprite_data)
	self.name = 'pink guardian at (%d, %d)' % (self.org_x, self.org_y)
	
	self.hp_max = 1
	self.global_bbox = (-24, -63, 48, 64)

	self.activate_function = activate
	self.release_function = release
	
	hostage = entry[5]
	self.param2 = dir
	self.param3 = objects[hostage]

def activate(self):
	hostage = self.param3

	if (not self.is_dead): # and ((hostage is None) or hostage.is_initialized):
		# print ('[guardian] activate object#%d (%s)' % (self.id_, self.name))

		common.activate(self, None)
		common.appear(self, init_stand)
		common.faces_object(self, Globs.musashi)
	
	else:
		print ('sword %s missed because : %s' % (self.name, hostage))
		print ('is_dead: %s' % self.is_dead)
		print ('hostage: %s' % hostage)
		if hostage:
			print ('hostage is_initialized: %s' % hostage.is_initialized)


def release(self):
	log.write(2, '[%s] release' % self)
	common.release(self)

def init_hit(self):
	# print ('[sword] init_hit')
	common.init_hit(self, HIT, update_collision, init_death)

def init_hit_shield(self):
	other = self.other_object
	if other.attack_type & 2:
		if self.moves_to_left ^ other.moves_to_left:
			init_block(self)
		else:
			common.init_hit(self, HIT, update_collision, init_death)
	else:
		common.init_hit(self, HIT, update_collision, init_death)

def init_collision(self):
	# print ('[sword] init_collision')
	self.is_dead = False # self.is_hit
	common.init_collision(self, HIT, update_collision)

def update_collision(self):
	# print ('[guardian] update_collision')
	common.update_collision(self, init_death, init_walk_towards_musashi)


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
		init_walk_towards_musashi(self)

	elif hostage and hostage.is_initialized and abs(hostage.org_x - self.x) > 64 :
		init_walk_towards_hostage(self)

	elif self.sprite.is_animation_over:
		if random.random() < .5:
			if self.sprite.animation_id == STAND1:
				set_animation(self.sprite, STAND2)
			else:
				set_animation(self.sprite, STAND1)
			

# walking towards musashi

def towards_musashi(self):
	print ('[%s] hub' % self.name)
	hostage = self.param3

	if self.floor == Globs.musashi.floor:
		if hostage\
		and hostage.is_initialized\
		and abs(self.x - hostage.org_x) >= 128:
			init_walk_towards_hostage(self)
				
		else:
			d = self.x - Globs.musashi.x
			print ('[%s] d = %s' % (self.name, d))
			if d < -64:
				common.moves_right(self, 32)
				# init_walk(self)
			elif d < 0:
				common.moves_right(self, 32)
				init_slash(self)
			elif d < 64:
				common.moves_left(self, -32)
				init_slash(self)
			else:
				common.moves_left(self, -32)
	
	else:
		print ('h')
		init_stand(self)


def init_walk_towards_musashi(self):
	print ('[%s] init_walk' % self.name)

	self.hit_function = init_hit_shield
	set_animation(self.sprite, WALK)
	# towards_musashi(self)
	self.param4 = init_walk_towards_musashi
	self.update_function = update_walk_towards_musashi
		
def update_walk_towards_musashi(self):
	# print ('[%s] update_walk' % self.name)
	common.update_walk_by_steps(self, walk_offsets, towards_musashi, towards_musashi, common.do_nothing, init_fall)


# walking towards hostage

def towards_hostage(self):
	print ('[%s] towards_hostage' % self.name)
	hostage = self.param3

	if hostage\
	and hostage.is_initialized\
	and abs(self.x - hostage.org_x) <= 64:
		if self.floor == Globs.musashi.floor:
			init_walk_towards_musashi(self)
		else:
			init_stand(self)
	
def init_walk_towards_hostage(self):
	print ('[%s] init_walk_towards_hostage' % self.name)

	hostage = self.param3

	if self.x <= hostage.org_x:
		print ('c')
		self.speed_x = 32
	else:
		print ('d')
		self.speed_x = -32

	self.hit_function = init_hit_shield
	set_animation(self.sprite, WALK)
	self.param4 = init_walk_towards_hostage
	self.update_function = update_walk_towards_hostage
		
def update_walk_towards_hostage(self):
	# print ('[%s] update_walk' % self.name)
	common.update_walk_by_steps(self, walk_offsets, towards_hostage, common.do_nothing, common.do_nothing, init_fall)
				

# block

def init_block(self):
	print ('[%s] init_block' % self.name)

	set_animation(self.sprite, BLOCK)
	self.update_function = update_block

def update_block(self):
	print ('[%s] update_block' % self.name)
	
	if self.sprite.is_animation_over:
		if self.param4:
			self.param4(self)
		else:
			init_walk_towards_musashi(self)


# slash

def init_slash(self):
	# set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SLASH)
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_slash

	
def update_slash(self):
	if self.sprite.is_animation_over:
		if self.param4:
			self.param4(self)			
		else:
			init_walk_towards_musashi(self)


def init_fall(self):
	# common.enable_shield(self, sword_box)

	self.accel_y = 0.25
	set_animation(self.sprite, WALK)
	self.update_function = update_fall
	self.hit_function = init_hit_shield

def update_fall(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y

	if handle_fall(self):
		init_walk_towards_musashi(self)


def init_death(self):
	common.init_death(self, DEATH, update_death)
	# release_sword(self)


def update_death(self):
	common.update_death(self, None)
