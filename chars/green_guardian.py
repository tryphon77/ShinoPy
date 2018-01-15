from object import *
from tsprite import *

from res.chars.sword_data import *
import random
from chars import common
from chars import projectiles

def init(entry):
	# param1 : x range of walk
	# param2 : frequence of throwing blade (0 = never, 9 = always)
	# param3 : pointer to hostage. If None, swordman is free
	# param4 = True if guardian throws low blade
	
	self = common.init(entry, green_sprite_data)
	self.name = 'guardian at (%d, %d)' % (self.org_x, self.org_y)
	
	self.hp_max = 1
	self.global_bbox = (-24, -63, 48, 64)

	self.activate_function = activate
	self.release_function = release
	rng, nerv, hostage_id, low_blade = entry[5]
	self.param1 = rng << 4
	self.param2 = nerv
	self.param3 = objects[hostage_id]
	self.param4 = low_blade

def activate(self):
	hostage = self.param3

	if (not self.is_dead): # and ((hostage is None) or hostage.is_initialized):
		# print ('[guardian] activate object#%d (%s)' % (self.id_, self.name))

		common.activate(self, None)
		common.appear(self, None)
		if self.org_faces_left:
			common.faces_left(self)
		else:
			common.faces_right(self)
		init_stand(self)
		# self.speed_x = 1
	
	else:
		print ('sword %s missed because : %s' % (self.name, hostage))
		print ('is_dead: %s' % self.is_dead)
		print ('hostage: %s' % hostage)
		if hostage:
			print ('hostage is_initialized: %s' % hostage.is_initialized)


def release(self):
	log.write(2, '[%s] release' % self)
	# GP.halt()
	common.release(self)

def init_hit_shield(self):
	# print ('[%s] init_hit_shield' % self.name)	
	other = self.other_object
	if other.attack_type & 2:
		if self.moves_to_left ^ other.moves_to_left:
			init_block(self)
		else:
			common.init_hit(self, HIT, update_collision, init_death)
	else:
		common.init_hit(self, HIT, update_collision, init_death)

def init_hit_shield_2(self):
	# print ('[%s] init_hit_shield_2' % self.name)
	other = self.other_object
	if other.attack_type & 2:
		if not(self.moves_to_left ^ other.moves_to_left):
			common.init_hit(self, HIT, update_collision, init_death)
	else:
		common.init_hit(self, HIT, update_collision, init_death)

def init_hit(self):
	# print ('[%s] init_hit' % self.name)
	common.init_hit(self, HIT, update_collision, init_death, impulsion = -6)

def init_collision(self):
	# print ('[%s] init_collision' % self.name)
	self.is_dead = False # self.is_hit
	common.init_collision(self, next_state =  update_collision, impulsion = -6)
	self.speed_x = 0

def update_collision(self):
	# print ('[guardian] update_collision')
	common.update_collision(self, init_death, init_walk)

def init_collision_no_blade(self):
	print ('[%s] init_collision_no_blade' % self.name)
	self.is_dead = False # self.is_hit
	common.init_collision(self, next_state =  update_collision_no_blade, impulsion = -6)
	self.speed_x = 0

def update_collision_no_blade(self):
	def fun(self):
		self.update_function = None
	# print ('[guardian] update_collision')
	common.update_collision(self, init_death, fun)


def init_stand(self):
	print ('[%s] init_stand' % self.name)
	hostage = self.param3
	
	# if self.floor == Globs.musashi.floor:
		# common.faces_object(self, Globs.musashi)
	# elif hostage:
		# common.faces_object(self, hostage)
	set_animation(self.sprite, random.choice([STAND1, STAND2]))
	# set_physics(self, 0, 0, 0, 0)
	self.speed_x = 0
	self.update_function = update_stand
	self.collision_function = init_collision
	self.hit_function = init_hit
	
def update_stand(self):
	print ('[%s] update_stand' % self.name)
	hostage = self.param3
	
	if self.sprite.new_frame and self.floor == Globs.musashi.floor:
		d = self.x - self.org_x
		if d > self.param1:
			self.speed_x = -1
			init_walk(self)
		elif d < -self.param1:
			self.speed_x = 1
			init_walk(self)
		else:
			attack_musashi(self)

	elif self.sprite.is_animation_over:
		init_stand(self)


def init_walk(self):
	print ('[%s] init_walk' % self.name)
	self.hit_function = init_hit_shield
	# self.param2 = 0
	set_animation(self.sprite, WALK)
	self.update_function = update_walk
	
	if self.x > Globs.musashi.x:
		common.faces_left(self)
	else:
		common.faces_right(self)
		

def attack_musashi(self):
	if abs(Globs.musashi.x - self.x) < 64:
		init_slash(self)
	else:
		n = random.randint(0, 9) - self.param2
		if n == 0:
			init_slash(self)
		elif n < 0:
			init_throw(self)


def update_walk_(self):

	if self.floor == Globs.musashi.floor:
		common.faces_object(self, Globs.musashi)
		d = self.x - self.org_x
		if d > self.param1:
			self.speed_x = -1
		elif d < -self.param1:
			self.speed_x = 1
		else:
			attack_musashi(self)
		
	else:
		init_stand(self)

def turn(self):
	fix_hpos(self)
	self.speed_x = -self.speed_x
	
def update_walk(self):
	print ('[%s] update_walk' % self.name)
	common.update_walk_by_steps(self, walk_offsets, update_walk_, turn, turn, init_fall)

# def update_back_walk(self):
	# print ('[%s] update_back_walk' % self.name)
	# common.update_walk_by_steps(self, walk_offsets, init_wait, common.do_nothing, common.do_nothing, init_fall)
	

# block

def init_block(self):
	print ('[%s] init_block' % self.name)

	set_animation(self.sprite, BLOCK)
	self.update_function = update_block

def update_block(self):
	print ('[%s] update_block' % self.name)
	
	if self.sprite.is_animation_over:
		init_walk(self)


def init_slash(self):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SLASH)
	self.collision_function = init_collision
	self.hit_function = init_hit_shield_2
	self.update_function = update_slash

	
def update_slash(self):
	if self.sprite.total_ticks_in_animation == 30:
		self.hit_function = init_hit
	if self.sprite.is_animation_over:
		init_stand(self)

def init_throw(self):
	print ('[%s] init_throw' % self.name)
	# set_physics(self, 0, 0, 0, 0)
	self.speed_x = 0
	set_animation(self.sprite, THROW)
	self.collision_function = init_collision
	self.hit_function = init_hit_shield_2
	self.update_function = update_throw


# general (move to common ?)

def throw_blade(self, dx, dy):
	print ('[%s] throw_blade' % self.name)
	blade = projectiles.init_blade(self)
	# self.param1 = blade
	blade.x = self.x + signate(self, dx)
	blade.y = self.y + dy
	blade.floor = self.floor
	blade.sprite.vpos |= (self.sprite.vpos & 0xF800)
	blade.param1 = self
	
	if self.moves_to_left:
		common.moves_left(blade, -2.5)
	else:
		common.moves_right(blade, 2.5)

def update_throw(self):
	# print ('[%s] update_throw' % self.name)
	if self.sprite.is_animation_over:
		if self.param4:
			throw_blade(self, 24, -21)
		else:
			throw_blade(self, 24, -45)
		set_animation(self.sprite, THROW_WAIT)
		self.hit_function = init_hit
		self.collision_function = init_collision_no_blade
		self.update_function = None # update_throw_wait

# def update_throw_wait(self):
	# # print ('[%s] update_throw_wait' % self.name)
	# if not self.param1.is_activated:
		# projectiles.release_blade(self.param1)
		# set_animation(self.sprite, THROW_END)
		# self.update_function = update_throw_end

def init_throw_end(self):
	print ('[%s] init_throw_end' % self.name)
	set_animation(self.sprite, THROW_END)
	self.update_function = update_throw_end
	self.collision_function = init_collision
	self.hit_function = init_hit_shield

def update_throw_end(self):
	# print ('[%s] update_throw_end' % self.name)
	if self.sprite.is_animation_over:
		init_walk(self)

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
		init_walk(self)


def init_death(self):
	# print ('[%s] init_death' % self.name)
	common.init_death(self, DEATH, update_death)
	# release_sword(self)


def update_death(self):
	common.update_death(self, None)
