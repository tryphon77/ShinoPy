from globals import Globs

from genepy import *
from tsprite import *
from object import *

from stage import init_stage
from camera import set_camera_focus_to, update_camera

import log

# Organization needed
# from res.levels import level_0_0
from res.levels.all_levels import *

from res.chars import projectile_data 
from res.chars import splash_data 
from res.chars import rocket_data 
from res.chars import bone_data 


def init():
	log.set_state(0xFF)
	
	clear_all_objects()
	clear_all_sprites()
	
	print ('init stage: %d' % Globs.level)
	stage = all_levels[Globs.level]
	init_stage(stage)
	set_camera_focus_to(Globs.musashi)
	
	Globs.base_id = 0

	GP.load_tile_data(projectile_data.patterns, projectile_data.PROJECTILE_VPOS)
	
	# @TODO : conditionnal loading
	if Globs.level == LEVEL_2_3:
		GP.load_tile_data(splash_data.patterns, projectile_data.MORE_VPOS)

	elif Globs.level in [LEVEL_3_1, LEVEL_3_2] :
		GP.load_tile_data(rocket_data.patterns, projectile_data.MORE_VPOS)

	elif Globs.level in [LEVEL_0_1, LEVEL_4_1, LEVEL_5_1, LEVEL_5_2, LEVEL_5_3] :
		GP.load_tile_data(bone_data.patterns, projectile_data.MORE_VPOS)
	
	# init chunk (always 1)
	# introduce_new_object_chunk(1)
	# print ('init_chunk')
	introduce_new_chunk_full_rect(1)
	print ('/init_chunk')
	# GP.halt()

	
def main():
	init()

	Globs.forward = BUTTON_RIGHT
	Globs.backward = BUTTON_LEFT

	while True:
		Globs.is_refresh_available = 3
		joy = GP.read_joypad(0)
		Globs.joy_pressed = (~Globs.old_joy) & joy
		Globs.old_joy = joy
		Globs.joy = joy

		if Globs.joy_pressed & BUTTON_START:
			print ('break')
			break

		update_all_objects()
		update_camera()
		update_all_sprites()
		GP.wait_vblank()


if __name__ == '__main__':
	GP.init()
	
	Globs.level = LEVEL_5_3
	
	while True:
		main()
		Globs.level = (Globs.level + 1) % 4
