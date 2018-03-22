import globals

from object import *
from tsprite import *
from genepy import *
from res.chars.projectile_data import *

from chars import common
from chars import green_guardian


def init_object():
	# print ('init shuriken')
	self = allocate_object(temporary_objects)
	self.name = 'shuriken'
	
	self.scope = (16, 16)
	
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = False
	self.is_drawn = True
	
	print ('shuriken id = %d' % self.id_)
	all_objects.add(self)
	friend_projectiles.add(self)
	
	# self.status = ACTIVE

	self.back = -4
	self.front = 4

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		# print ('shuriken sprite allocated')
		sprite.vpos = PROJECTILE_VPOS
		sprite.status = 1
		sprite.x = self.x
		sprite.y = self.y

		sprite.data = sprite_data
		self.global_display_box = (-16, -63, 32, 64)
		
		sprite.frame = -1

		self.hitting_object = None
		set_animation(sprite, SHURIKEN)
		self.update_function = update
		self.collision_function = init_vanish
		self.release_function = release_shuriken

		sprite.is_flipped = self.moves_to_left = Globs.musashi.moves_to_left
		
	return self


def release_shuriken(self):
	release_object(self)
	self.is_initialized = False
	self.name = 'cleared'
	friend_projectiles.remove(self)


def update(self):
	if not self.sprite.is_viewable:
		release_shuriken(self)
	else:
		self.is_collidable = True
		self.x += self.speed_x
		if self.hitting_object:
			init_vanish(self)
		if collides_background(self, self.front, 0):
			# print 'projectile .x = %d, .speed_x = %d, .front = %d' % (self.x, self.speed_x, self.front)
			init_vanish(self)

		
def init_vanish(self):
	self.is_collidable = False
	self.speed_x = 0
	set_animation(self.sprite, SHURIKEN_VANISH)
	self.update_function = update_vanish

def update_vanish(self):
	if self.sprite.is_animation_over:
		release_shuriken(self)


def init_bullet():
	# print 'init bullet'
	self = allocate_object(temporary_objects)
	self.name = "bullet"
	self.scope = (16, 128)
	
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = True
	
	# print 'shuriken id = %d' % self.id_
	all_objects.add(self)
	ennemy_projectiles.add(self)
	
	self.status = ACTIVE

	self.back = -4
	self.front = 4

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		sprite.vpos = PROJECTILE_VPOS
		sprite.status = 1
		sprite.x = self.x
		sprite.y = self.y
		
		sprite.data = sprite_data

		sprite.frame = -1

		set_animation(sprite, BULLET)
		self.update_function = update_bullet
		self.collision_function = init_bullet_vanish
		self.release_function = release_bullet

	return self


def release_bullet(self):
	release_object(self)
	self.is_initialized = False
	ennemy_projectiles.remove(self)


def update_bullet(self):
	self.x += self.speed_x
	if not self.sprite.is_viewable:
		release_shuriken(self)
	elif self.hitting_object:
		init_bullet_vanish(self)
	elif collides_background(self, self.front, 0):
		# print 'projectile .x = %d, .speed_x = %d, .front = %d' % (self.x, self.speed_x, self.front)
		init_bullet_vanish(self)

def init_bullet_vanish(self):
	self.speed_x = 0
	set_animation(self.sprite, BULLET_VANISH)
	self.update_function = update_bullet_vanish

def update_bullet_vanish(self):
	if self.sprite.is_animation_over:
		release_bullet(self)


# green guardians' blade

def init_blade(owner):
	# param1 : owner of the blade
	# param2 : timer 
	self = allocate_object(temporary_objects)
	self.name = 'blade'
	# print ('[%s] init_blade' % self.name)
	
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = True
	
	all_objects.add(self)
	ennemy_projectiles.add(self)
	
	self.back = -4
	self.front = 4
	self.scope = (256, 128)

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		sprite.vpos = PROJECTILE_VPOS
		sprite.status = 1
		sprite.x = self.x
		sprite.y = self.y
		
		sprite.data = sprite_data

		sprite.frame = -1

		set_animation(sprite, BLADE)
		self.param1 = owner
		self.update_function = update_blade
		self.collision_function = None
		self.release_function = release_blade
		
		self.param2 = 0

	return self


def release_blade(self):
	release_object(self)
	self.is_initialized = False
	ennemy_projectiles.remove(self)


def update_blade(self):
	# print ('[%s] update_blade' % self.name)
	self.x += self.speed_x
	coll = collides_background(self, self.front, 0)
	
	if coll:
		print ('collision')
		if self.param1.is_dead:
			release_blade(self)
		else:
			fix_hpos(self)
			if self.moves_to_left:
				common.moves_right(self, 2.5)
			else:
				common.moves_left(self, -2.5)
			self.update_function = update_blade_back
	
	elif not self.param1.is_dead:
		self.param2 += 1

		if self.param2 >= 48:
			if self.moves_to_left:
				common.moves_right(self, 2.5)
			else:
				common.moves_left(self, -2.5)
			self.update_function = update_blade_back

	# if self.iscollides_background(self, self.front, 0):
		# release_blade(self)
	# if (not self.param1.is_dead) and (self.param2 >= 48 or collides_background(self, self.front, 0)):
		# if self.moves_to_left:
			# common.moves_right(self, 2.5)
		# else:
			# common.moves_left(self, -2.5)
		# self.update_function = update_blade_back
	# self.x += self.speed_x
	print ('blade.x = %d' % self.x)

def update_blade_back(self):
	self.param2 -= 1
	if self.param1.is_dead:
		if collides_background(self, self.front, 0):
			release_blade(self)
		else:
			self.x += self.speed_x
	elif self.param2 <= 0 and self.param1.is_activated:
		green_guardian.init_throw_end(self.param1)
		release_blade(self)
	else:
		self.x += self.speed_x
		print ('blade.x = %d' % self.x)

