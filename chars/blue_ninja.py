from object import *
from tsprite import *

from res.chars.ninja_data import *
from chars import common
from chars import ninja_common

import random


def init(entry):
	self = ninja_common.init(entry, sprite_data_blue, activate, release, init_collision, init_hit, 'blue ninja')

def activate(self):
	print ('[%s] blue_ninja.activate' % self.name)
	ninja_common.activate(self, update_spawn)
	# print (self.x, camera.left, camera.right)
	# GP.halt()

def release(self):
	ninja_common.release(self)

def update_spawn(self):
	ninja_common.update_spawn(self, init_appear)

def init_appear(self):
	log.write(2, '[%s] init_appear' % self.name)
	ninja_common.init_appear(self, APPEAR, update_appear)

def update_appear(self):
	log.write(2, '[%s] update_appear' % self.name)
	ninja_common.update_appear(self, after_appear)

def after_appear(self):
	self.is_collidable = True
	if self.floor == Globs.musashi.floor:
		init_crouch(self)
	elif self.floor < Globs.musashi.floor and get_hijump_impulsion(self):
		init_hijump_up_start(self)
	elif self.floor > Globs.musashi.floor and get_hijump_down_impulsion(self):
		init_hijump_down_start(self)
	else:
		# init_jump_back_start(self)
		# for the red ninja in 2-2
		init_crouch(self)

# collision and death

def init_hit(self):
	ninja_common.init_hit(self, HIT, update_collision, init_death)

def init_hit_blade_high(self):
	ninja_common.init_hit_blade_high(self, HIT, update_collision, init_death)

def init_hit_blade_low(self):
	ninja_common.init_hit_blade_low(self, HIT, update_collision, init_death)

def init_collision(self):
	ninja_common.init_collision(self, HIT, update_collision)

def update_collision(self):
	ninja_common.update_collision(self, init_death, init_crouch)

def init_death(self):
	ninja_common.init_death(self, DEATH, update_death)

def update_death(self):
	ninja_common.update_death(self, update_spawn)


# crouch and crawl

def init_crouch(self):
	self.hit_function = init_hit_blade_low
	ninja_common.init_crouch(self, init_fall, update_crouch)

def update_crouch(self):
	ninja_common.update_crouch(self, init_air_attack, init_crawl, init_jump_back_start)

def init_crawl(self):
	# print ('[%s] init_crawl' % self.name)
	common.moves_object(self, Globs.musashi, 1)
	set_animation(self.sprite, CRAWL)
	self.update_function = update_crawl
	self.hit_function = init_hit_blade_low
	self.param2 = 0

def crawl_action(self):
	if self.sprite.is_animation_over:
		init_crouch(self)
		
def update_crawl(self):
	# print ('[%s] update_crawl' % self.name)
	# print (self.param2)
	common.update_walk_by_steps(self, crawl_offsets, crawl_action,  init_jump, init_jump, init_fall)

	
# air attack
def init_air_attack(self):
	if self.x < Globs.musashi.x:
		common.faces_right(self)
	else:
		common.faces_left(self)
	set_animation(self.sprite, JUMP_START)
	self.update_function = update_air_attack_1
	self.hit_function = init_hit_blade_high

def update_air_attack_1(self):
	if self.sprite.is_animation_over:
		dx = (Globs.musashi.x - self.x) / 64
		self.speed_x = dx
		self.speed_y = -8
		self.accel_y = 0.25
		set_animation(self.sprite, AIR_ATTACK)
		self.update_function = update_air_attack_2
		# ninja_common.disable_blade(self)

def disable_guard(self):
	if self.sprite.total_ticks_in_animation == 8:
		self.hit_function = init_hit

def update_air_attack_2(self):
	# self.x += self.speed_x

	# if collides_background(self, self.front, 0):
		# fix_hpos(self)
		# self.speed_x = signate(self, 1)

	# self.speed_y += self.accel_y
	# self.y += self.speed_y

	# if self.speed_y >= 0 and (collides_background(self, self.front, 0) or collides_background(self, self.back, 0)):
		# fix_vpos(self)
		# self.speed_y = 0
		# self.accel_y = 0
		# set_animation(self.sprite, JUMP_END)
		# self.update_function = update_air_attack_3
	common.update_jump(self, next_state = init_air_attack_3, action = disable_guard)

def init_air_attack_3(self):
	set_animation(self.sprite, JUMP_END)
	self.update_function = update_air_attack_3

def update_air_attack_3(self):
	self.x += self.speed_x
	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = signate(self, 1)

	if self.sprite.is_animation_over:
		init_crouch(self)
		
# jumping back
def init_jump_back_start(self):
	self.hit_function = init_hit
	ninja_common.init_jump_back_start(self, JUMP_START, update_jump_back_start)

def update_jump_back_start(self):
	ninja_common.update_jump_back_start(self, JUMP_BACK, update_jump)

def init_jump(self):
	self.hit_function = init_hit
	ninja_common.init_jump(self, JUMP, update_jump)

def update_jump(self):
	ninja_common.update_jump(self, init_fall)

def init_fall(self):
	ninja_common.init_fall(self, update_fall)

def update_fall(self):
	ninja_common.update_jump(self, next_state =  init_jump_end)

def init_jump_end(self):
	ninja_common.init_jump_end(self, JUMP_END, update_jump_end)

def update_jump_end(self):
	ninja_common.update_jump_end(self, init_hijump_up_start, init_hijump_down_start, init_crawl)
	

# hijump up

def init_hijump_up_start(self):
	# print ('[%s] init_hijump_up_start' % self.name)
	# GP.halt()
	self.hit_function = init_hit
	ninja_common.init_hijump_up_start(self, HIJUMP_UP_START, update_hijump_up_start)

def update_hijump_up_start(self):
	# print ('[%s] update_hijump_up_start' % self.name)
	# GP.halt()
	ninja_common.update_hijump_up_start(self, init_hijump_up_mid)

def init_hijump_up_mid(self):
	# print ('[%s] init_hijump_down_mid' % self.name)
	# GP.halt()
	ninja_common.init_hijump_up_mid(self, HIJUMP_UP, update_hijump_up_mid)

def update_hijump_up_mid(self):
	# print ('[%s] update_hijump_up_mid' % self.name)
	# GP.halt()
	ninja_common.update_hijump_up_mid(self, init_hijump_up_end)

def init_hijump_up_end(self):
	# print ('[RED] init_hijump_up_end' % self.name)
	# GP.halt()
	ninja_common.init_hijump_up_end(self, HIJUMP_UP_END, update_hijump_up_end)

def update_hijump_up_end(self):
	print ('[RED] update_hijump_up_end')
	# GP.halt()
	ninja_common.update_hijump_up_end(self, init_crouch)

# hijump down

def init_hijump_down_start(self):
	# print ('[%s] init_hijump_down_start' % self.name)
	# GP.halt()
	self.hit_function = init_hit
	ninja_common.init_hijump_down_start(self, HIJUMP_DOWN_START, update_hijump_down_start)

def update_hijump_down_start(self):
	# print ('[%s] update_hijump_down_start' % self.name)
	# GP.halt()
	ninja_common.update_hijump_down_start(self, init_hijump_down_mid)

def init_hijump_down_mid(self):
	# print ('[%s] init_hijump_down_mid')
	# GP.halt()
	ninja_common.init_hijump_down_mid(self, HIJUMP_DOWN, update_hijump_down_mid)

def update_hijump_down_mid(self):
	# print ('[%s] update_hijump_down_mid')
	# GP.halt()
	ninja_common.update_hijump_down_mid(self, init_hijump_down_end)

def init_hijump_down_end(self):
	# print ('[%s] init_hijump_down_end')
	# GP.halt()
	ninja_common.init_hijump_down_end(self, HIJUMP_DOWN_END, update_hijump_down_end)

def update_hijump_down_end(self):
	# print ('[%s] update_hijump_down_end')
	# GP.halt()
	ninja_common.update_hijump_down_end(self, init_crouch)
