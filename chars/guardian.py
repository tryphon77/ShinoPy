from object import *
from tsprite import *

from res.chars.sword_data import *
import random
from chars import common

def init(entry):
	# param1 : pointer to hostage. If None, swordman is free
	# param2 : counter for walking animation
	# param3 : pointer to sword object (can block projectiles)
	self = common.init(entry)
	self.name = 'guardian at (%d, %d)' % (self.org_x, self.org_y)

	self.activate_function = activate
	self.release_function = release
	if entry[4]:
		self.param1 = objects[entry[4]]
	else:
		self.param1 = None

def activate(self):
	hostage = self.param1

	if (not self.is_dead) and (hostage is None or hostage.is_initialized):
		print ('[guardian] activate object#%d (%s)' % (self.id_, self.name))

		self.param3 = init_sword(self)
		common.activate(self, None)
		common.appear(self, init_stand)
	
	else:
		print ('sword missed because : %s' % hostage)


def release(self):
	release_sword(self.param3)
	common.release(self)

def init_hit(self):
	print ('[sword] init_hit')
	sword = self.param3
	sword.is_collidable = False

	common.init_hit(self, HIT, update_collision, init_death)


def init_collision(self):
	print ('[sword] init_collision')

	sword = self.param3
	sword.is_collidable = False

	self.is_dead = False # self.is_hit
	common.init_collision(self, HIT, update_collision)

def update_collision(self):
	print ('[guardian] update_collision')

	common.update_collision(self, init_death, init_walk)


def init_stand(self):
	print ('[guardian] init_stand')
	set_animation(self.sprite, random.choice([STAND1, STAND2]))
	set_physics(self, 0, 0, 0, 0)
	self.update_function = update_stand
	self.collision_function = init_collision
	self.hit_function = init_hit

	sword = self.param3
	sword.is_collidable = False
	
def update_stand(self):
	hostage = self.param1
	
	if self.floor == Globs.musashi.floor:
		init_walk(self)

	elif hostage and hostage.is_initialized and abs(hostage.x - self.x) > 64 :
		# init_walk_towards_hostage(self)
		init_walk(self)

	elif self.sprite.is_animation_over:
		if random.random() < .5:
			if self.sprite.animation_id == STAND1:
				set_animation(self.sprite, STAND2)
			else:
				set_animation(self.sprite, STAND1)
			

def init_walk(self):
	self.collision_function = init_collision
	self.hit_function = init_hit

	head_towards(self, Globs.musashi)
	set_physics(self, 0, 0, 0, 0)
	self.param2 = 0
	set_animation(self.sprite, WALK)
	self.update_function = update_walk

	sword = self.param3
	sword.is_collidable = True
	if self.moves_to_left:
		sword.speed_x = -32
	else:
		sword.speed_x = 32
	sword.x = self.x + sword.speed_x
	sword.bbox = compute_box(sword, sword_box)


def guardian_faces_left(self):
	sword = self.param3
	self.moves_to_left = True
	self.sprite.is_flipped = True
	sword.speed_x = -32
	
def guardian_faces_right(self):
	sword = self.param3
	self.moves_to_left = False
	self.sprite.is_flipped = False
	sword.speed_x = 32

def towards_musashi(self):
	d = self.x - Globs.musashi.x
	if d < -64:
		guardian_faces_right(self)
		self.speed_x = 32
	elif d < 0:
		guardian_faces_right(self)
		init_slash(self)
	elif d < 64:
		guardian_faces_left(self)
		init_slash(self)
	else:
		guardian_faces_left(self)
		self.speed_x = -32

def towards_hostage(self):
	hostage = self.param1
	
	if hostage and hostage.is_initialized:
		d = self.x - hostage.x
		if d >= 64:
			guardian_faces_left(self)
			self.speed_x = -32
		elif d <= -64:
			guardian_faces_right(self)
			self.speed_x = 32
		else:
			init_stand(self)
	
def attack_musashi(self):
	hostage = self.param1

	if hostage and hostage.is_initialized:
		d = abs(self.x - hostage.x)
		if d >= 128:
			if self.x <= hostage.x:
				self.speed_x = 32
			else:
				self.speed_x = -32
			
		if d <= 64:
			towards_musashi(self)
	else:
		towards_musashi(self)

def guard_hostage(self):
	hostage = self.param1

	if hostage and hostage.is_initialized:
		towards_hostage(self)
	else:
		init_stand(self)

		
def update_walk(self):
	sword = self.param3
	
	common.update_walk_by_steps(self, walk_offsets, attack_musashi, guard_hostage, common.do_nothing, common.do_nothing, init_fall)

	sword.x = self.x + sword.speed_x
	sword.bbox = compute_box(sword, sword_box)
	

def init_slash(self):
	sword = self.param3
	sword.is_collidable = False

	set_physics(self, 0, 0, 0, 0)
	set_animation(self.sprite, SLASH)
	self.collision_function = init_collision
	self.hit_function = init_hit
	self.update_function = update_slash

	
def update_slash(self):
	if self.sprite.is_animation_over:
		init_stand(self)


def init_fall(self):
	sword = self.param3
	sword.status = ACTIVE

	self.accel_y = 0.25
	set_animation(self.sprite, WALK)
	self.update_function = update_fall

def update_fall(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0)\
			or collides_background(self, self.back, 0):
		fix_vpos(self)
		init_walk(self)


def init_death(self):
	common.init_death(self, DEAD, update_death)
	release_sword(self.param3)


def update_death(self):
	common.update_death(self, None)

# ===============================================================
# sword object

def init_sword(char):
	# param1 : pointer to char
	floor, x, y = char.floor, char.org_x, char.org_y

	print ('init sword at (%d, %d)' % (x, y))
	self = allocate_object(temporary_objects)
	self.name = 'saber of %s' % char.name
	
	ennemy_objects.add(self)
	all_objects.add(self)

	self.release_function = None
	
	if char.moves_to_left:
		self.speed_x = -32
	else:
		self.speed_x = 32
		
	self.x = x + self.speed_x
	self.y = y
	self.floor = floor

	self.back = -8
	self.front = 8

	self.is_initialized = True
	self.is_activated = True
	self.is_collidable = True
	self.sprite = None
	self.update_function = None

	self.collision_function = sword_hit
	self.hit_function = sword_hit
	# self.release_function = release_sword

	self.param1 = char

	return self

def sword_hit(self):
	guardian = self.param1
	if guardian.moves_to_left:
		self.speed_x = -32
	else:
		self.speed_x = 32
	guardian.x -= signate(guardian, 2)
	guardian.sprite.tick += 4

def release_sword(self):
	print ('[sword] release_sword')
	release_object(self)
	ennemy_objects.remove(self)
