import globals

from object import *
from tsprite import *
from genepy import *
from res.chars.bone_data import *
from res.chars import projectile_data

from chars import common


def init_bone():
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
	self.scope = (16, 64)

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		sprite.vpos = projectile_data.MORE_VPOS
		sprite.status = 1
		
		sprite.data = sprite_data

		sprite.frame = -1

		set_animation(sprite, BONE)
		self.update_function = update_bone
		self.collision_function = release
		self.release_function = release
	return self


def release(self):
	release_object(self)
	self.is_initialized = False
	ennemy_projectiles.remove(self)


def update_bone(self):
	self.x += self.speed_x
	if collides_background(self, self.front, 0):
		release(self)
