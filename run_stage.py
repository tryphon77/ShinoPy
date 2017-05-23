from globals import Globs

from genepy import *
from tsprite import *
from object import *

from stage import init_stage
from camera import set_camera_focus_to

# Organization needed
from res.levels import level_0_0
from res.levels import level_1_1
from res.levels import level_2_2
from res.levels import level_3_3
from res import musashi_data
from res.states import musashi_states
from res.states import punk_states
from res.states import shooter_states
from res.states import knife_states
from res.states import sword_states
from res.states import spidey_states
from res.states import hostage_states
from res import projectile_data 

stages = [level_1_1, level_2_2, level_3_3, level_0_0]

def init():
	clear_all_objects()
	clear_all_sprites()
	
	print ('init stage: %d' % Globs.lvl)
	stage = stages[Globs.lvl]
	init_stage(stage)
	musashi_states.init_object()
	Globs.musashi = objects[0]
	Globs.musashi.x, Globs.musashi.y = stage.musashi_pos
	set_camera_focus_to(Globs.musashi)

	Globs.base_id = 0

	GP.load_tile_data(projectile_data.patterns, 0x300)
	GP.load_tile_data(hostage_states.patterns, 0x400)
	

def main():
	init()

	# old_joy = 0
	Globs.forward = BUTTON_RIGHT
	Globs.backward = BUTTON_LEFT

	while True:
		Globs.is_refresh_available = 3
		joy = GP.read_joypad(0)
		Globs.joy_pressed = (~Globs.old_joy) & joy
		Globs.old_joy = joy
		Globs.joy = joy

		# print ('Globs.joy = %X, Globs.joy_pressed = %X, old_joy = %X' % (Globs.joy, Globs.joy_pressed, Globs.old_joy))
		if Globs.joy_pressed & BUTTON_START:
			print ('break')
			break

		update_all_objects()

		set_camera_focus_to(objects[0])
		# print 'x: %d -> %d\ty: %d -> %d' % (camera.left, camera.right, camera.top, camera.bottom)

		update_all_sprites()

		# print 'musashi bounding box:', objects[0].bbox
		# print 'punk bounding box:', objects[1].bbox
		# if objects[0].floor == objects[1].floor\
				# and objects[0].bbox and objects[1].bbox\
				# and collision_between_boxes(objects[0].bbox, objects[1].bbox):
			# print 'collision'
			# objects[0].collided_object = objects[1]
			# objects[1].collided_object = objects[0]
			# if objects[0].collision_function:
				# objects[0].collision_function(objects[0])
			# if objects[1].collision_function:
				# objects[1].collision_function(objects[1])

	# print 'x = %s, front = %s, back = %s' % (objects[0].x, objects[0].front, objects[0].back)
		GP.wait_vblank()


if __name__ == '__main__':
	GP.init()
	
	Globs.lvl = 0
	
	while True:
		main()
		Globs.lvl = (Globs.lvl + 1) % 4
