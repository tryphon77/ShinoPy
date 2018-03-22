import globals

from object import *
from tsprite import *
from genepy import *
from res.chars.rocket_data import *
from res.chars import projectile_data

from chars import common


def init_rocket():
	self = allocate_object(temporary_objects)
	self.name = 'rocket'
	self.scope = (16, 64)
	
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = True
	
	all_objects.add(self)
	ennemy_projectiles.add(self)
	
	self.status = ACTIVE

	self.back = -4
	self.front = 4

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		sprite.vpos = projectile_data.MORE_VPOS
		sprite.status = 1
		
		sprite.data = sprite_data

		sprite.frame = -1

		set_animation(sprite, ROCKET)
		self.update_function = update_rocket
		self.collision_function = init_explosion
		self.release_function = release
	return self


def release(self):
	release_object(self)
	self.is_initialized = False
	ennemy_projectiles.remove(self)


def update_rocket(self):
	self.x += self.speed_x
	if collides_background(self, self.front, 0):
		init_explosion(self)

def init_explosion(self):
	self.speed_x = 0
	set_animation(self.sprite, EXPLOSION)
	self.update_function = update_explosion

def update_explosion(self):
	if self.sprite.is_animation_over:
		release(self)


def init_ball():
	self = allocate_object(temporary_objects)
	
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = True
	
	all_objects.add(self)
	ennemy_projectiles.add(self)
	
	self.status = ACTIVE

	self.back = -4
	self.front = 4

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		sprite.vpos = projectile_data.MORE_VPOS
		sprite.status = 1
		
		sprite.data = sprite_data

		sprite.frame = -1

		self.speed_y = -6
		self.accel_y = 0.25
		set_animation(sprite, BALL)
		self.update_function = update_ball
		self.collision_function = init_explosion
		self.release_function = release
	return self


def release(self):
	release_object(self)
	self.is_initialized = False
	ennemy_projectiles.remove(self)


def update_ball(self):
	self.x += self.speed_x
	if collides_background(self, self.front, 0):
		init_explosion(self)
	
	self.speed_y += self.accel_y
	self.y += self.speed_y

	if self.speed_y > 0 and collides_background(self, 0, 1):
		init_explosion(self)
