from object import *
from tsprite import *
from camera import camera

from res.chars.ninja_data import *
import random
from chars import common

def init(entry, sprite_data, activate_fun, release_fun, collision_fun, hit_fun, name):
	# param1 = pointer to sword
	self = common.init(entry, sprite_data)
	self.name = "%s at (%d, %d)" % (name, self.org_x, self.org_y)

	# param1 : coord of appearance (!= coords of triggering)
	# self.param1 = entry[4]
	
	self.activate_function = activate_fun
	self.release_function = release_fun
	self.collision_function = collision_fun
	self.hit_function = hit_fun

	self.hp_max = 2
	# self.global_display_box = (-16, -63, 32, 64)
	
	self.update_function = None

	# self.param1 = init_blade(self)
	return self
	

def activate(self, next_state):
	# print ('[%s] activate object #%d' % (self.name, self.id_))
	common.activate(self, None)
	common.appear(self, next_state)
	# print (self.param1)
	# common.activate_shield(self.param1)

def release(self):
	# print ('[ninja] release: %s' % self.name)
	# release_blade(self)
	common.release(self)

def update_spawn(self, next_state):
	# print ('[ninja] update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		common.appear_on_edge(self, next_state)


def init_appear(self, anim, next_state):
	set_animation(self.sprite, anim)

	# dx, dy = self.param1
	# if camera.moves_left:
		# self.x += dx
	# else:
		# self.x -= dx
	# self.y += dy

	common.faces_object(self, Globs.musashi)
	
	self.update_function = next_state
	self.is_collidable = False

def update_appear(self, next_action):
	if self.sprite.is_animation_over:
		next_action(self)


# collision and death

def init_hit_blade_high(self, anim, next_state, death_state):
	other = self.other_object
	if other.attack_type & 2:
		if (self.moves_to_left ^ other.moves_to_left) and (self.y - other.y > 32):
			print ('shield')
		else:
			common.init_hit(self, anim, next_state, death_state, impulsion = -8)
	else:
		common.init_hit(self, anim, next_state, death_state, impulsion = -8)

def init_hit_blade_low(self, anim, next_state, death_state):
	other = self.other_object
	if other.attack_type & 2:
		if (self.moves_to_left ^ other.moves_to_left) and (self.y - other.y < 32):
			print ('shield')
			if self.sprite.is_flipped:
				self.speed_x = -1
			else:
				self.speed_x = 1
		else:
			common.init_hit(self, anim, next_state, death_state, impulsion = -8)
	else:
		common.init_hit(self, anim, next_state, death_state, impulsion = -8)

def init_hit(self, anim, next_state, death_state):
	# print ('[%s] init_hit' % self.name)
		common.init_hit(self, anim, next_state, death_state, impulsion = -8)

def init_collision(self, anim, next_state):
	# print ('[%s] init_collision')
	# disable_blade(self)
	self.is_dead = False # self.is_hit
	common.init_collision(self, anim, next_state, impulsion = -8)

def update_collision(self, death_state, next_state):
	# print ('[green ninja] update_collision')
	common.update_collision(self, death_state, next_state)

def init_death(self, anim, next_state):
	# print ('[%s] init_death' % self.name)
	common.init_death(self, anim, next_state)

def update_death(self, next_state):
	# print ('[%s] update_death' % self.name)
	common.update_death(self, next_state)


# crouch and crawl

def init_crouch(self, hole_action, update_fun):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, CROUCH)
	self.is_collidable = True

	if collides_background(self, self.front, 1) == 0 and collides_background(self, self.back, 1) == 0:
		hole_action(self)
	else:
		self.update_function = update_fun

def hub_action(self, attack_fun, crawl_fun, different_floor_fun):
	if self.floor == Globs.musashi.floor:
		if self.moves_to_left:
			d = self.x - Globs.musashi.x
			if d < 0:
				common.faces_right(self)
			elif d < 160:
				attack_fun(self)
			else:
				crawl_fun(self)
		else:
			d = Globs.musashi.x - self.x
			# print ('d = %d' % d)
			# GP.halt()
			if d < 0:
				common.faces_left(self)
			elif d < 160:
				attack_fun(self)
			else:
				crawl_fun(self)
	else:
		different_floor_fun(self)

def update_crouch(self, attack_fun, crawl_fun, different_floor_fun):
	if self.sprite.is_animation_over:
		hub_action(self, attack_fun, crawl_fun, different_floor_fun)

# def init_crawl(self, anim, next_state):
	# if self.x < Globs.musashi.x:
		# common.faces_right(self, 1)
	# else:
		# common.faces_left(self, -1)

	# self.param2 = 0
	# set_animation(self.sprite, anim)
	# self.update_function = next_state
	# self.is_collidable = True
	
# def update_crawl(self, same_floor, different_floor, obstacle_action, wall_action, fall_action):
	# print (self.param2)
	# common.update_walk_by_steps(self, crawl_offsets, same_floor, different_floor, obstacle_action, wall_action, fall_action)

	
# walk

def init_walk(self, anim, next_state):
	common.moves_object(self, Globs.musashi, 2)

	set_animation(self.sprite, anim)
	self.update_function = next_state
	self.is_collidable = True
			
def update_walk(self, same_floor, different_floor, obstacle_action, wall_action, fall_action):
	self.speed_x = common.signate(self, 2)
	common.update_walk(self, same_floor, different_floor, obstacle_action,wall_action, fall_action)


# slash
def init_slash(self, anim, next_state):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, anim)
	self.update_function = next_state
	
def update_slash(self, next_state):
	if self.sprite.is_animation_over:
		next_state(self)


# jumping back
def init_jump_back_start(self, anim, next_state):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, anim)
	self.update_function = next_state
	# disable_blade(self)

def update_jump_back_start(self, anim, next_state):
	if self.sprite.is_animation_over:
		set_physics(self, -2, 0, -7.5, 0.25)
		set_animation(self.sprite, anim)
		self.update_function = next_state

def init_jump(self, anim, next_state):
	set_physics(self, 2, 0, -7.5, 0.25)
	set_animation(self.sprite, anim)
	self.update_function = next_state

def update_jump(self, next_state):
	common.update_jump(self, next_state = next_state)

def init_fall(self, next_state):
	# print ('[green ninja] init_fall')
	common.init_fall(self, None, next_state)

def update_fall(self, next_state):
	# print ('[green ninja] update_fall')
	common.update_jump(self, next_state = next_state)

def init_jump_end(self, anim, next_state):
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, anim)
	self.update_function = next_state

def update_jump_end(self, hijump_up, hijump_down, next_state):
	if self.sprite.is_animation_over:
		if self.floor < Globs.musashi.floor and get_hijump_impulsion(self):
			hijump_up(self)
		elif self.floor > Globs.musashi.floor and get_hijump_down_impulsion(self):
			hijump_down(self)
		else:
			next_state(self)
	

# hijump up

def init_hijump_up_start(self, anim, next_state):
	# print ('[%s] init_hijump_up_start' % self.name)
	self.speed_y = self.accel_y = 0
	set_animation(self.sprite, anim)
	self.update_function = next_state

def update_hijump_up_start(self, next_state):
	# print ('[%s] update_hijump_up_start' % self.name)
	if self.sprite.is_animation_over:
		next_state(self)

def init_hijump_up_mid(self, anim, next_state):
	# print ('[%s] init_hijump_up_mid' % self.name)
	self.speed_y = get_hijump_impulsion(self)
	self.accel_y = 0.5
	set_animation(self.sprite, anim)
	self.update_function = next_state
	# self.floor |= 0x80

def update_hijump_up_mid(self, next_state):
	# print ('[%s] update_hijump_up_mid' % self.name)
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y == 0:
		self.floor += 1
		# self.floor &= 0x7F
		self.sprite.vpos &= 0x7FFF
	elif handle_fall(self):
		next_state(self)

def init_hijump_up_end(self, anim, next_state):
	# print ('[%s] init_hijump_up_end' % self.name)
	self.speed_y = self.accel_y = 0
	set_animation(self.sprite, anim)
	self.update_function = next_state

def update_hijump_up_end(self, next_state):
	# print ('[%s] update_hijump_up_end' % self.name)
	if self.sprite.is_animation_over:
		next_state(self)

# hijump down

def init_hijump_down_start(self, anim, next_state):
	print ('[%s] init_hijump_down_start' % self.name)
	# GP.halt()
	self.speed_y = self.accel_y = 0
	set_animation(self.sprite, anim)
	self.update_function = next_state
	# disable_blade(self)

def update_hijump_down_start(self, next_state):
	print ('[%s] update_hijump_down_start' % self.name)
	# GP.halt()
	if self.sprite.is_animation_over:
		next_state(self)

def init_hijump_down_mid(self, anim, next_state):
	print ('[%s] init_hijump_down_mid' % self.name)
	# GP.halt()
	self.speed_y = get_hijump_down_impulsion(self)
	self.accel_y = 0.5
	set_animation(self.sprite, anim)
	self.update_function = next_state
	# self.is_collidable = False
	# self.floor |= 0x80

def update_hijump_down_mid(self, next_state):
	print ('[%s] update_hijump_down_mid' % self.name)
	# GP.halt()
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y == 0:
		self.floor -= 1
		# self.floor &= 0x7F
		if self.floor == 1:
			self.sprite.vpos |= 0x8000
		else:
			self.sprite.vpos &= 0x7FFF
	elif handle_fall(self):
		next_state(self)

def init_hijump_down_end(self, anim, next_state):
	print ('[%s] init_hijump_up_end' % self.name)
	# GP.halt()
	self.speed_y = self.accel_y = 0
	set_animation(self.sprite, anim)
	self.update_function = next_state

def update_hijump_down_end(self, next_state):
	print ('[%s] update_hijump_down_end' % self.name)
	# GP.halt()
	if self.sprite.is_animation_over:
		next_state(self)


# blade

# def init_blade(char):
	# print ('[%s] init_blade' % char.name)
	# # GP.halt()
	# self = common.init_shield(char, blade_hit)
	# return self
	
# def blade_hit(self):
	# pass

# def release_blade(self):
	# print ('[%s] release_blade' % self.name)
	# # GP.halt()
	# common.release_shield(self)

