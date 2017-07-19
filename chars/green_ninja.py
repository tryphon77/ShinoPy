from object import *
from tsprite import *

from res.chars.ninja_data import *
import random
from chars import common

def init(entry):
	self = common.init(entry)
	self.name = "green ninja at (%d, %d)" % (self.org_x, self.org_y)

	self.activate_function = activate
	self.release_function = release
	
	self.update_function = None

def activate(self):
	print ('[ninja] activate object#%d (%s)' % (self.id_, self.name))
	common.activate(self, update_spawn)

def release(self):
	print ('[ninja] release: %s' % self.name)
	release_object(self)
	ennemy_objects.remove(self)

def update_spawn(self):
	print ('[ninja] update_spawn: %d' % self.tick)
	self.tick -= 1
	if self.tick < 0:
		common.appear_on_edge(self, None)
