import sys
sys.path.append('../../pygato')

import pygame

from map import *
from tmx import *

obj_name = ['musashi', 'punk', 'shooter', 'guardian', 'hostage', 'knife', 'spider', '', 'kenoh', '', '', 'green_guardian', 'green_ninja', 'blue_ninja', 'red_ninja']

base_dir = 'C:/Users/fterr/Documents/hack/shinobi/maps/2-2'

tmx = load_tmx('%s/level22.tmx' % base_dir)
objects = tmx[2].map

w, h = tmx[2].get_size()

for y in range(h - 1, -1, -1):
	for x in range(w):
		t = objects[y][x].id_
		if t:
			print ('[%s, ?, %d, %d]' % (obj_name[t], x * 16 + 10, y * 16 + 15))
			