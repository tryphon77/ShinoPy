from object import *
from tsprite import *

from res.levels import all_levels
from chars import more_objects

from res.chars.frogman_data import *
from chars import common
from chars import more_objects

def init(entry):
	self = common.init(entry)
	self.name = 'frogman at (%d, %d)' % (self.org_x, self.org_y)
	
	self.org_faces_left = True

	self.hp_max = 1
	self.global_display_box = (-16, -63, 32, 64)
	self.spawn_counter = 300

	# param1 : delay before jumping
	# param2 : tick
	self.param1 = self.param2 = entry[4]	
	
	self.activate_function = activate
	self.release_function = release

def activate(self):
	print ('[%s] activate' % self.name)
	common.activate(self, update_spawn)

def release(self):
	print ('[%s] release' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

	
# spawn
def update_spawn(self):
	print ('[%s] update_spawn: %d' % (self.name, self.tick))
	self.tick -= 1
	if self.tick < 0:
		common.appear(self, None)
		if self.sprite:
			common.faces_object(self, Globs.musashi)
			# self.update_function = update_spawn
			init_wait(self)
		else:
			print ('no sprite')
			exit()

# wait

def init_wait(self):
	print ('[%s] init_wait' % self.name)
	self.is_collidable = True
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, HIDDEN)
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_wait

def update_wait(self):
	if abs(Globs.musashi.x - self.x) < 64:
		if self.param2 == 0:
			if self.param1:
				more_objects.init_long_splash(self.x, 480)
				self.param1 = 0
				self.param2 = 20
			else:
				init_jump(self)
		else:
			self.param2 -= 1


# collision, hit, death

def init_hit(self):
	print ('[%s] hit' % self.name)
	self.is_dead = True
	common.init_collision(self, HIT, update_fall)

def init_hit_blade(self):
	other = self.other_object
	if other.attack_type & 2:
		if self.moves_to_left ^ other.moves_to_left:
			pass
		else:
			init_hit(self)
	else:
		init_hit(self)

def init_collision(self):
	#@TODO : fix and factorize for all chars
	print ('[%s] collision' % self.name)
	self.is_dead = False # self.is_hit
	common.init_collision(self, HIT, update_fall)

def update_fall(self):
	common_update_jump(self)

def hub(self):
	print ('[%s] next_action' % self.name)
	if self.y < 496:
		init_crouch(self)	
	elif self.y >= 536:
		self.y = 537
		self.param2 = 16
		init_wait(self)

	
def init_death(self):
	common.init_death(self, DEATH, update_death)

def update_death(self):
	common.update_death(self, update_spawn)


# jump

def init_jump(self):
	print ('[%s] init_jump' % self.name)
	common.faces_object(self, Globs.musashi)
	set_physics(self, .5, 0, -8, 0.25)
	set_animation(self.sprite, JUMP)
	more_objects.init_short_splash(self.x, 480)
	self.update_function = update_jump

# def update_jump(self):
	# common.update_jump(self, init_fall)

# def init_fall(self):
	# common.init_fall(self, None, update_fall)

def common_update_jump(self, action = common.do_nothing):
	print ('[%s] bbox: %s' % (self.name, self.bbox))
	if self.y < 496:
		self.x += self.speed_x

		if collides_background(self, self.front, 0)\
		or collides_background(self, self.back, 0)\
		or collides_background(self, self.front, -32)\
		or collides_background(self, self.back, -32):
			print ('fix_hpos', self.x, self.y)
			print ('before: ', self.x, self.speed_x)
			fix_hpos(self)
			print ('after: ', self.x, self.speed_x)

	old_y = self.y
	self.speed_y += self.accel_y
	self.y += self.speed_y
	
	if self.speed_y > 0:
		if self.y < 496 and handle_fall(self):
			if self.is_dead:
				init_death(self)
			else:
				init_crouch(self)
			
		elif self.y >= 537:
			self.y = 537
			self.param2 = 16
			if self.is_dead:
				init_death(self)
			else:
				init_wait(self)
			
		else:
			more_objects.check_splash(self.x, old_y, self.y)
			action(self)

def attack(self):
	if abs(self.x - Globs.musashi.x) < 48:
		set_animation(self.sprite, ATTACK)

def update_jump(self):
	common_update_jump(self, attack)

# crouch

def init_crouch(self):
	print ('[%s] init_crouch' % self.name)
	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, CROUCH)
	self.hit_function = init_hit_blade
	self.update_function = update_crouch

def update_crouch(self):
	if self.sprite.is_animation_over:
		init_leap(self)


# leap

def init_leap(self):
	print ('[%s] init_leap' % self.name)
	common.faces_object(self, Globs.musashi)
	set_physics(self, .5, 0, -4.5, 0.25)
	set_animation(self.sprite, LEAP)
	self.hit_function = init_hit
	self.update_function = update_jump




