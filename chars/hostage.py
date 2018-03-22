from object import *
from tsprite import *

from res.chars.hostage_data import *
from chars import common
import tsprite


def init(entry):
	# param1 : pointer to guardian
	
	if Globs.hostage_vpos is None:
		Globs.hostage_vpos = tsprite.allocate_tiles(patterns)

	self = common.init(entry)
	self.name = "hostage at (%d, %d)" % (self.org_x, self.org_y)
	self.param1 = entry[5]
	
	self.scope = (40, 32)
	self.global_display_box = (-16, -31, 32, 32)

	self.activate_function = activate
	self.release_function = release

def activate(self):
	common.activate(self, None)
	common.appear(self, init_wait, hostage_objects, False)
	if self.sprite:
		self.sprite.vpos &= 0xF800
		self.sprite.vpos |= Globs.hostage_vpos

		self.collision_function = init_free
	self.release_function = release
	# GP.halt()
	

def release(self):
	release_object(self)
	hostage_objects.remove(self)
	# GP.halt()


def init_wait(self):
	set_animation(self.sprite, WAIT)
	self.collision_function = init_free

def init_free(self):
	print ('[hostage] init_free')
	set_animation(self.sprite, FREE)
	self.update_function = update_free

def update_free(self):
	if self.sprite.is_animation_over:
		init_free_2(self)

def init_free_2(self):
	set_animation(self.sprite, FREE_2)
	self.speed_y = -6
	self.accel_y = .25
	self.update_function = update_free_2

def update_free_2(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y > -2:
		release(self)
		self.is_initialized = False
