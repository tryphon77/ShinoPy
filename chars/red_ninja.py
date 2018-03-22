from object import *
from tsprite import *

from res.chars.ninja_data import *
from chars import common
from chars import ninja_common

import random


def init(entry):
	self = ninja_common.init(entry, sprite_data_red, activate, release, init_collision, init_hit, 'red ninja')
	log.write(2, '[%s] init' % self.name)

def activate(self):
	log.write(2, '[%s] activate(' % self.name)
	ninja_common.activate(self, update_spawn)

def release(self):
	log.write(2, '[%s] release(' % self.name)
	ninja_common.release(self)

def update_spawn(self):
	log.write(2, '[%s] update_spawn' % self.name)
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
	log.write(2, '[%s] init_hit' % self.name)
	ninja_common.init_hit(self, HIT, update_collision, init_death)

def init_hit_blade_high(self):
	log.write(2, '[%s] init_hit_blade_high' % self.name)
	ninja_common.init_hit_blade_high(self, HIT, update_collision, init_death)

def init_hit_blade_low(self):
	log.write(2, '[%s] init_hit_blade_low' % self.name)
	ninja_common.init_hit_blade_low(self, HIT, update_collision, init_death)

def init_collision(self):
	log.write(2, '[%s] init_collision' % self.name)
	ninja_common.init_collision(self, HIT, update_collision)

def update_collision(self):
	log.write(2, '[%s] update_collision' % self.name)
	ninja_common.update_collision(self, init_death, init_crouch)

def init_death(self):
	log.write(2, '[%s] init_death' % self.name)
	ninja_common.init_death(self, DEATH, update_death)

def update_death(self):
	log.write(2, '[%s] update_death' % self.name)
	ninja_common.update_death(self, None)


# crouch and crawl

def init_crouch(self):
	log.write(2, '[%s] init_crouch' % self.name)
	self.hit_function = init_hit_blade_low
	ninja_common.init_crouch(self, init_fall, update_crouch)

# red ninja in 2-2 doesn't seem to jump backward when on different floor
def update_crouch(self):
	log.write(2, '[%s] update_crouch' % self.name)
	ninja_common.update_crouch(self, init_walk, init_crawl, init_crawl)

def init_crawl(self):
	print ('[%s] init_crawl' % self.name)
	common.moves_object(self, Globs.musashi, 1)
	set_animation(self.sprite, CRAWL)
	self.update_function = update_crawl
	self.hit_function = init_hit_blade_low
	self.param2 = 0

def crawl_action(self):
	if self.sprite.is_animation_over:
		init_crouch(self)
		
def update_crawl(self):
	print ('[%s] update_crawl' % self.name)
	print (self.param2)
	common.update_walk_by_steps(self, crawl_offsets, crawl_action,  init_jump, init_jump, init_fall)

	
# walk

def init_walk(self):
	log.write(2, '[%s] init_walk' % self.name)
	self.hit_function = init_hit_blade_high
	ninja_common.init_walk(self, WALK, update_walk)
	# GP.halt()

def attacks_musashi(self):
	log.write(2, '[%s] attacks_musashi' % self.name)
	if self.moves_to_left:
		d = self.x - Globs.musashi.x
		if 0 < d < 48:
			init_jump(self)
	else:
		d = Globs.musashi.x - self.x
		if 0 < d < 48:
			init_jump(self)

def jump_back(self):
	log.write(2, '[%s] jump_back' % self.name)
	if abs(self.x - Globs.musashi.x) < 64:
		init_jump_back_start(self)
				
def update_walk(self):
	log.write(2, '[%s] update_walk' % self.name)
	ninja_common.update_walk(self, attacks_musashi, jump_back, init_jump, common.half_turn, init_fall)


# slash

def init_turn_and_slash(self):
	log.write(2, '[%s] init_turn_and_slash' % self.name)
	if Globs.musashi.x < self.x:
		common.faces_left(self)
	else:
		common.faces_right(self)
	init_slash(self)

def init_slash(self):
	log.write(2, '[%s] init_slash' % self.name)
	self.hit_function = init_hit
	ninja_common.init_slash(self, ATTACK, update_slash)
	
def update_slash(self):
	log.write(2, '[%s] update_slash' % self.name)
	ninja_common.update_slash(self, init_walk)

		
# jumping back
def init_jump_back_start(self):
	log.write(2, '[%s] init_jump_back_start' % self.name)
	self.hit_function = init_hit
	ninja_common.init_jump_back_start(self, JUMP_START, update_jump_back_start)

def update_jump_back_start(self):
	log.write(2, '[%s] update_jump_back_start' % self.name)
	ninja_common.update_jump_back_start(self, JUMP_BACK, update_jump)

def init_jump(self):
	log.write(2, '[%s] init_jump' % self.name)
	self.hit_function = init_hit
	ninja_common.init_jump(self, JUMP, update_jump)

def update_jump(self):
	log.write(2, '[%s] update_jump' % self.name)
	log.write(2, 'before: x = %d, y = %d' % (self.x, self.y))
	ninja_common.update_jump(self, init_fall)
	log.write(2, 'after: x = %d, y = %d\n' % (self.x, self.y))

def init_fall(self):
	log.write(2, '[%s] init_fall' % self.name)
	log.write(2, 'before: x = %d, y = %d' % (self.x, self.y))
	ninja_common.init_fall(self, update_fall)
	log.write(2, 'after: x = %d, y = %d\n' % (self.x, self.y))

def update_fall(self):
	log.write(2, '[%s] update_fall' % self.name)
	log.write(2, 'before: x = %d, y = %d' % (self.x, self.y))
	# print ('[%s] update_fall (%d, %d)' % (self.name, self.x, self.y))
	ninja_common.update_fall(self, init_jump_end)
	log.write(2, 'after: x = %d, y = %d\n' % (self.x, self.y))

def init_jump_end(self):
	log.write(2, '[%s] init_jump_end' % self.name)
	ninja_common.init_jump_end(self, JUMP_END, update_jump_end)

def update_jump_end(self):
	log.write(2, '[%s] update_jump_end' % self.name)
	ninja_common.update_jump_end(self, init_hijump_up_start, init_hijump_down_start, init_turn_and_slash)
	
	
# hijump up

def init_hijump_up_start(self):
	log.write(2, '[%s] init_hijump_up_start' % self.name)
	# GP.halt()
	self.hit_function = init_hit
	ninja_common.init_hijump_up_start(self, HIJUMP_UP_START, update_hijump_up_start)

def update_hijump_up_start(self):
	log.write(2, '[%s] update_hijump_up_start' % self.name)
	print ('[RED] update_hijump_up_start')
	# GP.halt()
	ninja_common.update_hijump_up_start(self, init_hijump_up_mid)

def init_hijump_up_mid(self):
	log.write(2, '[%s] init_hijump_up_mid' % self.name)
	print ('[RED] init_hijump_down_mid')
	# GP.halt()
	ninja_common.init_hijump_up_mid(self, HIJUMP_UP, update_hijump_up_mid)

def update_hijump_up_mid(self):
	log.write(2, '[%s] update_hijump_up_mid' % self.name)
	print ('[RED] update_hijump_up_mid')
	# GP.halt()
	ninja_common.update_hijump_up_mid(self, init_hijump_up_end)

def init_hijump_up_end(self):
	log.write(2, '[%s] init_hijump_up_end' % self.name)
	print ('[RED] init_hijump_up_end')
	# GP.halt()
	ninja_common.init_hijump_up_end(self, HIJUMP_UP_END, update_hijump_up_end)

def update_hijump_up_end(self):
	log.write(2, '[%s] update_hijump_up_end' % self.name)
	print ('[RED] update_hijump_up_end')
	# GP.halt()
	ninja_common.update_hijump_up_end(self, init_crouch)

# hijump down

def init_hijump_down_start(self):
	log.write(2, '[%s] init_hijump_down_start' % self.name)
	print ('[RED] init_hijump_down_start')
	# GP.halt()
	self.hit_function = init_hit
	ninja_common.init_hijump_down_start(self, HIJUMP_DOWN_START, update_hijump_down_start)

def update_hijump_down_start(self):
	log.write(2, '[%s] update_hijump_down_start' % self.name)
	print ('[RED] update_hijump_down_start')
	# GP.halt()
	ninja_common.update_hijump_down_start(self, init_hijump_down_mid)

def init_hijump_down_mid(self):
	log.write(2, '[%s] init_hijump_down_mid' % self.name)
	print ('[RED] init_hijump_down_mid')
	# GP.halt()
	ninja_common.init_hijump_down_mid(self, HIJUMP_DOWN, update_hijump_down_mid)

def update_hijump_down_mid(self):
	log.write(2, '[%s] update_hijump_down_mid' % self.name)
	print ('[RED] update_hijump_down_mid')
	# GP.halt()
	ninja_common.update_hijump_down_mid(self, init_hijump_down_end)

def init_hijump_down_end(self):
	log.write(2, '[%s] init_hijump_down_end' % self.name)
	print ('[RED] init_hijump_down_end')
	# GP.halt()
	ninja_common.init_hijump_down_end(self, HIJUMP_DOWN_END, update_hijump_down_end)

def update_hijump_down_end(self):
	log.write(2, '[%s] update_hijump_down_end' % self.name)
	print ('[RED] update_hijump_down_end')
	# GP.halt()
	ninja_common.update_hijump_down_end(self, init_crouch)
