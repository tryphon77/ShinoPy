from globals import Globs
from genepy import *
from layer import *
from camera import *


def init_stage(stage):
	# load background
	GP.load_tile_data(stage.patterns, 0x40) 
	
	# load tileset
	Globs.tileset = stage.tileset

	# load collision map
	Globs.collision_map = stage.collision_map
	Globs.jumps_table = stage.jumps_table
	
	# load objects_map
	Globs.objects_map = stage.objects_map
	Globs.objects_chunks = stage.objects_chunks

	if False:
		Globs.objects_from_left = stage.objects_from_left
		Globs.objects_from_right = stage.objects_from_right
		Globs.objects_from_top = stage.objects_from_top
		Globs.objects_from_bottom = stage.objects_from_bottom
	
	# load tilemap
	layer_A.plane = GP.plane_A
	layer_A.data = stage.tilemap_A
	layer_A.twidth = stage.twidth
	layer_A.theight = stage.theight

#    Globs.layer_a_twidth = stage.twidth;
#    Globs.layer_a_theight = stage.theight;
	Globs.layer_a_pwidth = stage.twidth * 16;
	Globs.layer_a_pheight = stage.theight * 16;

	if stage.drawing_method == 0:
		layer_B.plane = None
		layer_B.data = None    
		layer_B.twidth = 0
		layer_B.theight = 0

		Globs.layer_b_pwidth = 0
		Globs.layer_b_pheight = 0

	elif stage.drawing_method == 1:
		layer_B.plane = GP.plane_B
		layer_B.data = stage.tilemap_B    
		layer_B.twidth = stage.twidth #//2 + 10
		layer_B.theight = stage.theight #//2 + 7
		
		Globs.layer_b_pwidth = stage.twidth * 16
		Globs.layer_b_pheight = stage.theight * 16

	elif stage.drawing_method == 2:
		layer_B.plane = GP.plane_B
		layer_B.data = stage.tilemap_B    
		layer_B.twidth = stage.twidth# // 2 + 10
		layer_B.theight = stage.theight# // 2 #+ 7
		
		# Globs.layer_b_pwidth = layer_B.twidth * 16
		# Globs.layer_b_pheight = layer_B.theight * 16

	Globs.layer_B_drawing_method = stage.drawing_method
	Globs.stage_priority = stage.priority

	camera.is_initialized = False
	# Globs.camera_x = 0
	# Globs.camera_y = 0
	
	# camera.left = 0
	# camera.right = 319
	# camera.top = 0
	# camera.bottom = 223
		
	# draw_rect(layer_A, 0, 0, 21, 15)
	# if Globs.layer_B_drawing_method:
		# draw_rect(layer_B, 0, 0, 21, 15)
	
	Globs.vscroll_mode = 1

	Globs.hostage_vpos = None
	for entry in stage.objects:
		obj_type = entry[0]
		print (obj_type)
		obj_type.init(entry) #[1:])
	
	Globs.objects_hindex = 1
	Globs.n_objects = len(stage.objects)

