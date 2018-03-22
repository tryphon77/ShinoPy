from object import *
from tsprite import *

from res.chars.skeleton_data import *
from chars import common
from chars.bone import init_bone


def init(entry):
	self = common.init(entry, sprite_data)
	self.name = 'skeleton at (%d, %d)' % (self.org_x, self.org_y)
		
	# param1 : range in pixels
	# param2 : number of bones before moving
	self.param1, self.param2 = entry[5]
	
	self.hp_max = 1
	self.global_display_box = (-24, -63, 48, 64) # a modifier
	self.spawn_counter = 600
	self.scope = (64, 64)
	
	self.accel_y = .25

	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, None)
	self.is_collidable = True
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_spawn
	
def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn

def update_spawn(self):
	common.update_spawn(self, init_hidden)

def init_hidden(self):
	# print ('[%s] init_hidden' % self.name)
	
	common.appear(self, None)
	
	if self.sprite:
		if self.org_faces_left:
			common.faces_left(self)
		self.is_collidable = True
		set_animation(self.sprite, APPEAR)
		self.update_function = update_hidden

def update_hidden(self):
	if self.sprite.is_animation_over:
		init_pop(self)


# pop

def init_pop(self):
	self.is_collidable = True
	set_animation(self.sprite, POPUP)
	self.update_function = update_pop

def update_pop(self):
	if self.sprite.is_animation_over:
		init_walk(self)
		

# collision and death

def init_collision(self):
	print ('[%s] collision' % self.name)
	self.is_dead = False
	set_animation(self.sprite, HIT)
	self.accel_y = .25
	self.update_function = update_collision

def init_hit(self):
	print ('[%s] hit' % self.name)
	self.accel_y = .25
	common.init_hit(self, HIT, update_collision, init_death)

def _handle_gravity(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y
		
	if not handle_fall(self):
		self.process_gravity = False

def update_collision(self):
	common.update_collision(self, init_death, init_pop_down)

def init_pop_down(self):
	set_animation(self.sprite, POP_DOWN)
	self.update_function = update_pop_down

def update_pop_down(self):
	if self.sprite.is_animation_over:
		init_pop(self)

# def _update_collision(self):
	# if self.process_gravity:
		# handle_gravity(self)
	# elif collides_background(self, self.front, 1) == 0 and collides_background(self, self.back, 1) == 0:
		# self.process_gravity = True
	# if self.sprite.is_animation_over:
		# if self.is_dead:
			# self.is_displayable = False
			# release_sprite(self.sprite)
			# ennemy_objects.remove(self)
			# self.sprite = None
			# self.update_function = None
		# else:
			# init_pop(self)

def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	common.update_death(self, update_spawn)

# walk

def init_walk(self):		
	common.faces_object(self, Globs.musashi)

	self.speed_x = signate(self, 1)
	set_animation(self.sprite, WALK)
	self.update_function = update_walk
# ========================================

def update_walk(self):
	self.x += self.speed_x

	if collides_background(self, self.front, 1) == 0 and collides_background(self, self.back, 1) == 0:
		self.accel_y = .25
		self.update_function = update_jump_mid

	elif collides_background(self, 21, -48):
		common.half_turn(self)

	# elif collides_background(self, self.front + 1, 0) or collides_background(self, self.back - 1, 0):
	elif collides_background(self, 21, 0):
		init_jump(self)

	elif self.floor < Globs.musashi.floor and get_hijump_impulsion(self) and abs(self.x - Globs.musashi.x) > 64:
		init_hijump_up_start(self)
	
	elif self.floor > Globs.musashi.floor and get_hijump_down_impulsion(self) and abs(self.x - Globs.musashi.x) > 64:
		init_hijump_down_start(self)
	
	elif self.param1 and self.floor == Globs.musashi.floor and abs(self.x - Globs.musashi.x) < self.param1:
		self.param3 = self.param2
		init_shoot(self)
	
	elif self.sprite.is_animation_over:
		init_walk(self)


# jump and fall

def init_jump(self):
	set_animation(self.sprite, JUMP_START)
	self.update_function = update_jump
	
# def init_fall(self):
	# common.init_fall(self, None, update_jump)

def update_jump(self):
	if self.sprite.is_animation_over:
		init_jump_mid(self)

def init_jump_mid(self):
	self.speed_x = signate(self, 1)
	self.speed_y = -6
	self.accel_y = .25
	set_animation(self.sprite, JUMP_MID)
	self.update_function = update_jump_mid

def update_jump_mid(self):
	common.update_jump(self, next_state = init_jump_end)

def init_jump_end(self):
	set_animation(self.sprite, JUMP_END)
	self.update_function = update_jump_end

def update_jump_end(self):
	if self.sprite.is_animation_over:
		init_walk(self)	


# hijump

def init_hijump_up_start(self):
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
	common.update_hijump_up_end(self, init_walk)

	
def init_hijump_down_start(self):
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
	common.update_hijump_down_end(self, init_walk)
	

# shoot

def init_shoot(self):
	set_animation(self.sprite, SHOOT)
	self.update_function = update_shoot

def update_shoot(self):
	if self.sprite.total_ticks_in_animation == 32:
		print('FIRE !')
		throw_bone(self)
	
	elif self.sprite.is_animation_over:
		self.param3 -= 1
		if self.param3 == 0:
			init_walk(self)
		else:
			init_shoot(self)

def throw_bone(self):
	bone = init_bone()
	if bone.sprite:
		if self.sprite.is_flipped:
			common.moves_left(bone, -2)
			bone.x = self.x - 12
		else:
			common.moves_right(bone, 2)
			bone.x = self.x + 12
		bone.y = self.y - 36
		bone.floor = self.floor


