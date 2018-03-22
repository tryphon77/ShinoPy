from object import *
from tsprite import *

from res.chars.monk_data import *
from chars import common


# vulnérable attaques basses : 1*
# invulnérable attaques basses : frames 

# vulnérable attaques hautes : frame 3, 7
# invulnérable attaques hautes : frames 0, 1, 8

def init(entry):
	self = common.init(entry, sprite_data)
	self.name = 'monk at (%d, %d)' % (self.org_x, self.org_y)

	self.hp_max = 2
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 6000
	
	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)
	self.tick = 0
	self.is_collidable = True
	self.collision_function = init_collision
	self.hit_function = init_hit

def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn

def update_spawn(self):
	print ('update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		common.appear(self, init_walk)
	
# collision and death

def init_collision(self):
	print ('[%s] collision' % self.name)
	self.is_dead = False
	common.init_collision(self, HIT, update_collision)

def init_hit(self):
	print ('[%s] hit' % self.name)
	common.init_hit(self, HIT, update_collision, init_death)

def update_collision(self):
	common.update_collision(self, init_death, init_walk)

def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	common.update_death(self, None)

# guard

def init_guard_and_jump(self):
	other = self.other_object
	if (self.moves_to_left ^ other.moves_to_left):
		if other.y > self.y - 32:
			init_jump(self)
	else:
		init_hit(self)

def init_guard(self):
	other = self.other_object
	if (self.moves_to_left ^ other.moves_to_left):
		if other.y > self.y - 32:
			init_hit(self)
	else:
		init_hit(self)
	
# walk

def init_walk_to_musashi(self):
	common.faces_object(self, Globs.musashi)
	init_walk(self)

def init_walk(self):
	self.is_collidable = True
	set_animation(self.sprite, WALK)
	self.hit_function = init_guard_and_jump
	self.update_function = update_walk
	self.speed_x = signate(self, 2)


def update_walk(self):	
	self.x += self.speed_x

	if collides_background(self, self.front + 1, 0) or collides_background(self, self.back - 1, 0):
		fix_hpos(self)
		if get_hijump_down_impulsion(self):
			init_hijump_down_start(self)
		elif get_hijump_impulsion(self):
			init_hijump_up_start(self)
		else:
			common.half_turn(self)
	
	elif collides_background(self, self.front, 1) == 0 and collides_background(self, self.back, 1) == 0:
		init_fall(self)
	
	elif self.floor == Globs.musashi.floor and abs(self.x - Globs.musashi.x) < 80:
		init_attack(self)



# jump and fall

def init_jump(self):
	self.hit_function = init_guard
	set_animation(self.sprite, JUMP_START)
	self.update_function = update_jump_start
	
def update_jump_start(self):
	if self.sprite.is_animation_over:
		init_jump_mid(self)

def init_jump_mid(self):
	set_animation(self.sprite, JUMP_MID)
	self.speed_x = signate(self, 1)
	self.speed_y = -7.5
	self.accel_y = .5
	self.update_function = update_jump

def init_jump_end(self):
	set_animation(self.sprite, JUMP_END)
	self.update_function = update_jump_end

def update_jump_end(self):
	if self.sprite.is_animation_over:
		init_walk(self)

def init_fall(self):
	common.init_fall(self, None, update_jump)

def update_jump(self):
	common.update_jump(self, next_state = init_jump_end)

# hijump

def init_hijump_up_start(self):
	self.hit_function = init_hit
	common.init_hijump_up_start(self, HIJUMP_UP_START, update_hijump_up_start)

def update_hijump_up_start(self):
	common.update_hijump_up_start(self, init_hijump_up_mid)

def init_hijump_up_mid(self):
	common.init_hijump_up_mid(self, HIJUMP_UP_MID, update_hijump_up_mid)

def update_hijump_up_mid(self):
	common.update_hijump_up_mid(self, init_hijump_up_end)

def init_hijump_up_end(self):
	common.init_hijump_up_end(self, HIJUMP_UP_END, update_hijump_up_end)

def update_hijump_up_end(self):
	common.update_hijump_up_end(self, init_walk_to_musashi)

	
def init_hijump_down_start(self):
	self.hit_function = init_hit
	common.init_hijump_down_start(self, HIJUMP_DOWN_START, update_hijump_down_start)

def update_hijump_down_start(self):
	common.update_hijump_down_start(self, init_hijump_down_mid)

def init_hijump_down_mid(self):
	common.init_hijump_down_mid(self, HIJUMP_DOWN_MID, update_hijump_down_mid)

def update_hijump_down_mid(self):
	common.update_hijump_down_mid(self, init_hijump_down_end)

def init_hijump_down_end(self):
	common.init_hijump_down_end(self, HIJUMP_DOWN_END, update_hijump_down_end)

def update_hijump_down_end(self):
	common.update_hijump_down_end(self, init_walk_to_musashi)


# attack

def init_attack(self):
	self.hit_function = init_guard
	set_animation(self.sprite, ATTACK)
	self.update_function = update_attack

def update_attack(self):
	if self.sprite.is_animation_over:
		init_walk_to_musashi(self)

