from object import *
from tsprite import set_animation

from res.hostage_data import *

import tsprite

hostage_tiles_pos = 0

def allocate_tiles():
	global hostage_tiles_pos
	hostage_tiles_pos = tsprite.allocate_tiles(patterns)


def init_object(entry):
	# param1 : pointer to hostage. If None, swordman is free
	# param2 : counter for walking animation
	floor, x, y, keeper = entry[4:]
	print('init hostage')
	print ('tiles allocated at: %X' % hostage_tiles_pos)
	self = allocate_object()
	self.name = "hostage at (%d, %d)" % (x, y)

	entry[0] |= ON_SCREEN
	self.object_entry = entry
	print ('init: object_entry: % s' % self.object_entry)
	hostage_objects.add(self)
	self.collision_function = init_free
	self.release_function = release
	
	self.status = ACTIVE

	self.x = x
	self.y = y
	self.floor = floor
	self.param1 = keeper

	self.back = -10
	self.front = 10

	self.sprite = sprite = allocate_static_sprite()
	sprite.name = "sprite %s" % self.name

	sprite.vpos = hostage_tiles_pos
	sprite.status = 1
	sprite.x = self.x
	sprite.y = self.y
	sprite.patterns = patterns
	sprite.frames_table = frames_table
	sprite.animations_table = animations_table
	sprite.bboxes_table = bounding_boxes
	sprite.hitboxes = hitboxes

	sprite.frame = -1
	sprite.patterns_blocks = patterns_blocks
#	sprite.bbox = (-12, 0, 24, 28)

	init_wait(self)


def release(self):
	release_object(self)
	self.object_entry[0] &= 0xFE
	print ('release : object_entry: % s' % self.object_entry)
	hostage_objects.remove(self)


def init_wait(self):
	set_animation(self.sprite, WAIT)
	self.collision_function = init_free
	print ('hostage object_entry: % s' % self.object_entry)

def init_free(self):
	set_animation(self.sprite, FREE)
	self.update_function = update_free
	self.object_entry[0] &= 0xFD
	print ('free : object_entry: % s' % self.object_entry)

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

