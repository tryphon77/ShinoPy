import globals

from object import *
from tsprite import *
from genepy import *
from res.chars.splash_data import *

from chars import common




def release_more_object(self):
	release_object(self)
	self.is_initialized = False
	ennemy_projectiles.remove(self)


# splash (when entering water in 2-3)

def init(x, y):
	self = allocate_object(temporary_objects)
	
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = False
	
	self.x = x
	self.y = y
	
	all_objects.add(self)
	
	self.status = ACTIVE

	self.back = -4
	self.front = 4

	self.sprite = sprite = allocate_static_sprite()
	if sprite:
		sprite.vpos = 0x392
		sprite.status = 1
		sprite.x = self.x
		sprite.y = self.y
		
		sprite.data = sprite_data

		sprite.frame = -1

		self.update_function = update_splash
		self.collision_function = None
		self.release_function = release_more_object

	return self

def init_splash(x, y):
	self = init(x, y)
	if self.sprite:
		set_animation(self.sprite, SPLASH)
	
def init_short_splash(x, y):
	self = init(x, y)
	if self.sprite:
		set_animation(self.sprite, SHORT_SPLASH)
	
def init_long_splash(x, y):
	self = init(x, y)
	if self.sprite:
		set_animation(self.sprite, LONG_SPLASH)


def update_splash(self):
	if self.sprite.is_animation_over:
		release_more_object(self)

def check_splash(x, old_y, y):
	if old_y >= 480 and y < 480:
		init_splash(x, 480)
	elif old_y < 480 and y >= 480:
		init_splash(x, 480)
