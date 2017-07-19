from object import *
from tsprite import *
from globals import Globs
from genepy import GP

from res.chars.punk_data import *
from chars import common

def init(entry):
	self = common.init(entry)
	self.name = "punk at (%d, %d)" % (self.org_x, self.org_y)

	self.activate_function = activate
	self.release_function = release
	
	self.update_function = None

def activate(self):
	print ('[punk] activate object#%d (%s)' % (self.id_, self.name))
	common.activate(self, update_spawn)

def release(self):
	print ('[punk] release: %s' % self.name)
	release_object(self)
	ennemy_objects.remove(self)


def init_walk_towards_musashi(self):
	if self.x > Globs.musashi.x:
		flip(self)
	
	init_walk(self)

def update_spawn(self):
	# print ('update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		common.appear_on_edge(self, init_walk_towards_musashi)


def init_hit(self):
	# print('punk init_hit')
	common.init_hit(self, HIT, update_collision, init_death)


def init_walk(self):
	# print 'punk init_walk'
	self.moves_to_left = self.sprite.is_flipped
	set_physics(self, 1, 0, 0, 0)
	# set_physics(self, 0, 0, 0, 0)	# DEBUG ONLY !!!!!!!!!!!!
	set_animation(self.sprite, WALK)
	self.update_function = update_walk
	self.collision_function = init_collision
	self.hit_function = init_hit


def attacks_musashi(self):
	if self.moves_to_left:
		d = self.x - Globs.musashi.x
		if d > 0:
			if d < 32:
				init_punch(self)
			elif d < 48:
				init_kick(self)
	else:
		d = Globs.musashi.x - self.x
		if d > 0:
			if d < 32:
				init_punch(self)
			elif d < 48:
				init_kick(self)

				
def update_walk(self):
	common.update_walk(self, attacks_musashi, common.do_nothing, init_jump, common.half_turn, init_fall)


def init_collision(self):
	# print 'punk init_collision'
	self.is_dead = False # self.is_hit
	# print 'other.speed = %f' % other.speed_x

	common.init_collision(self, HIT, update_collision)


def update_collision(self):
	# print 'punk update_collision [moves_to_left = %s, front = %s]' % (self.moves_to_left, self.front)
	common.update_collision(self, init_death, init_walk)

def init_jump(self):
	set_physics(self, 1, 0, -5, 0.25)
	set_animation(self.sprite, JUMP)
	self.update_function = update_jump


def update_jump(self):
	common.update_jump(self, init_fall)

def init_fall(self):
	# print 'punk init_fall'
	common.init_fall(self, FALL, update_fall)


def update_fall(self):
	# print 'punk update_fall'
	common.update_fall(self, init_walk)

def init_death(self):
	# print ('[punk.init_death] %s' % self.name)

	# print ('all_objects:')
	# for o in all_objects:
		# print (o.name, o.is_initialized, o.is_activated, o.is_displayable, o.is_collidable)
	# print ('ennemy_objects:')
	# for o in ennemy_objects:
		# print (o.name, o.is_initialized, o.is_activated, o.is_displayable, o.is_collidable)

	common.init_death(self, DEAD, update_death)


def update_death(self):
	common.update_death(self, update_spawn)


def init_punch(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, PUNCH)
	self.update_function = update_attack


def init_kick(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, KICK)
	self.update_function = update_attack


def update_attack(self):
	if self.sprite.is_animation_over:
		init_walk(self)
