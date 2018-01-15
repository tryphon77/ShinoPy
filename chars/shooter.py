import random
from chars import common

from object import *
from tsprite import *
from chars import projectiles

from res.chars.shooter_data import *


# param1 = counter for stopping walk
# param2 = number of bullets
# param3 = 
#	0: standing shooter
#	1: sitting shooter
#	2: lying shooter

def init(entry):
	print('init shooter')

	self = common.init(entry)
	self.name = "shooter at (%d, %d)" % (self.org_x, self.org_y)

	self.activate_function = activate
	self.release_function = release
	
	self.hp_max = 1
	self.param2 = 3
	self.param3 = entry[5]

def activate(self):
	
	if self.org_faces_left != Globs.musashi.moves_to_left:
		common.activate(self, None)
		common.appear(self, None)	
		common.faces_object(self, Globs.musashi)
		[init_walk, init_walk, init_laid][self.param3](self)


def release(self):
	print ('shooter release: %s' % self.name)
	common.release(self)

	
def shoot(self, dx, dy):
	bullet = projectiles.init_bullet()
	bullet.x = self.x + signate(self, dx)
	bullet.y = self.y + dy
	bullet.floor = self.floor
	bullet.speed_x = signate(self, 2)
	bullet.sprite.is_flipped = self.sprite.is_flipped
	bullet.sprite.vpos |= (self.sprite.vpos & 0xF800)
	# print 'throw .x = %d, .speed = %d, .front = %d' % (bullet.x, bullet.speed_x, bullet.front)


def init_walk(self):
	set_animation(self.sprite, WALK)
	set_physics(self, 1, 0, 0, 0)
	self.param1 = 1 << (random.randint(0, 7))
	self.update_function = update_walk
	self.collision_function = init_collision
	self.hit_function = init_hit

	
# lay

def init_laid(self):
	set_animation(self.sprite, LAID)
	set_physics(self, 0, 0, 0, 0)
	self.update_function = update_laid
	self.collision_function = init_collision
	self.hit_function = init_hit

def update_laid(self):
	if self.sprite.is_animation_over and self.floor == Globs.musashi.floor:
		d = abs(self.x - Globs.musashi.x)
		if d <= 80:
			init_stand_up(self)
		else:
			init_shoot_laid(self)

def init_stand_up(self):
	set_animation(self.sprite, STAND_UP)
	self.update_function = update_stand_up
	self.param3 = 0

def update_stand_up(self):
	if self.sprite.is_animation_over:
		init_shoot(self)

def init_shoot_laid(self):
	set_animation(self.sprite, SHOOT_LAID)
	self.update_function = update_shoot_laid
	shoot(self, 64, -10)

def update_shoot_laid(self):
	if self.sprite.is_animation_over:
		init_laid(self)


# walk
def walk_same_level_action(self):
	common.faces_object(self, Globs.musashi)
	if abs(self.x - Globs.musashi.x) < 160:
		[init_shoot, init_shoot_sat][self.param3](self)

def walk_different_level_action(self):
	if self.sprite.is_animation_over:
		self.param1 -= 1
		if self.param1 <= 0:
			init_reload(self)

def update_walk(self):
	# common.update_walk(self, walk_same_level_action, walk_different_level_action, init_jump, common.half_turn, init_fall)
	common.update_walk(self, walk_same_level_action, walk_different_level_action, init_jump, common.half_turn, init_fall)


def init_reload(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, RELOAD)
	self.param2 = 3
	self.update_function = update_reload

def update_reload(self):
	if self.sprite.is_animation_over:
		init_walk(self)


def init_shoot(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, PREPARATION_SHOOT_STAND)
	self.update_function = update_shoot

def update_shoot(self):
	if self.sprite.is_animation_over:
		init_shoot1(self)
		

def init_shoot1(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SHOOT_STAND)
	self.update_function = update_shoot1

def update_shoot1(self):
	if self.sprite.total_ticks_in_animation == 4:
		shoot(self, 40, -40)
	elif self.sprite.is_animation_over:
		init_shoot1(self)
		self.param2 -= 1
		print('bullets left: %d' % self.param2)
		if self.param2 == 0:
			init_reload(self)

def init_shoot_sat(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SHOOT_SAT)
	self.update_function = update_shoot_sat

def update_shoot_sat(self):
	if self.sprite.total_ticks_in_animation == 4:
		shoot(self, 40, -24)
	elif self.sprite.is_animation_over:
		init_shoot_sat(self)
		self.param2 -= 1
		print('bullets left: %d' % self.param2)
		if self.param2 == 0:
			init_reload(self)


def init_collision(self):
	if self.param3 == 2:
		self.param3 = 0
	common.init_collision(self, HIT, update_collision)

def init_hit(self):
	common.init_hit(self, HIT, update_collision, init_death)

def update_collision(self):
	common.update_collision(self, init_death, init_walk)


def init_jump(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, IMPULSE)
	self.update_function = update_jump

def update_jump(self):
	if self.sprite.is_animation_over:
		init_jump1(self)


def init_jump1(self):
	set_physics(self, 1, 0, -5, 0.25)
	set_animation(self.sprite, JUMP)
	self.update_function = update_jump1


def update_jump1(self):
	# common.update_jump(self, init_fall)
	common.update_jump(self, next_state = init_walk)


def init_fall(self):
	common.init_fall(self, FALL, update_jump1)

# def update_fall(self):
	# common.update_fall(self, init_walk)

def init_death(self):
	common.init_death(self, DEAD, update_death)

def update_death(self):
	common.update_death(self, None)
