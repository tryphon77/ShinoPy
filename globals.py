STATIC_TILES_START = 0x580

class Globs():
	tileset = None
	tilemap = None
	tilemap_A = None
	tilemap_B = None

	objects_map = None
	objects_chunk = 0

	layer_a_twidth = 0
	layer_a_theight = 0
	layer_a_pwidth = 0
	layer_a_pheight = 0
	layer_b_twidth = 0
	layer_b_theight = 0
	layer_b_pwidth = 0
	layer_b_pheight = 0

	is_refresh_available = 0
	
	# camera_x = 0
	# camera_y = 0
	vscroll_mode = True

	link = 0

	old_joy = 0
	joy = 0
	joy_pressed = 0
	forward = 0
	backward = 0

	musashi = None

	n_objects = 0
	objects_hlist = []
	objects_hindex = 0
	
	static_tiles = STATIC_TILES_START
	
	next_state = None
	
	level = 0
	mission = 0
	stage = 0
	show_mission_text = True

	hostage_vpos = None

