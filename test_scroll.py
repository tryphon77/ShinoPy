from globals import Globs

from genepy import *
from tsprite import *
from object import *

from stage import init_stage
from camera import set_camera

import log

from res.levels.all_levels import *

def init():
	log.set_state(0xFF)
	
	clear_all_objects()
	clear_all_sprites()
	
	init_stage(level_3_2)

	
def main():

	for x0 in range(16):
		for y0 in range(16):			
			for dx, dy in [(2, .25), (2, .5), (2, .75)]:

				GP.plane_A[0].fill(0xFF00DC)
				GP.plane_B[0].fill(0xFF00DC)
				init()
				set_camera(x0, y0)

				x = y = 0				
				for i in range(64):
					x += dx
					y += dy
					set_camera(int(x), int(y))
					GP.plane_A_offset = -int(x), int(y)
					GP.plane_B_offset = -int(x), int(y)
					GP.log_write('x = %.2f (%d)    y = %.2f (%d)' % (x, int(x), y, int(y)), 0, 0)
					GP.log_write('dx = %.2f    dy = %.2f' % (dx, dy), 0, 16)
					GP.wait_vblank()


if __name__ == '__main__':
	GP.init()
	
	main()
