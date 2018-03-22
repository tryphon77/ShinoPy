from genepy import *
from globals import *
from layer import layer_A, layer_B, draw_rect

class Camera():
	def __init__(self):
		is_initialized = False # if False, whole screen is drawn
		
		self.left = 0
		self.right = 0
		self.top = 0
		self.bottom = 0
		
		self.delta_x = 128
		self.delta_y = 128

		# self.virtual_left = 0
		# self.virtual_right = 0
		# self.virtual_top = 0
		# self.virtual_bottom = 0
		
		self.moves_left = False
		self.moves_right = False
		self.moves_up = False # up, not top
		self.moves_down = False
		
		focus = None
		

camera = Camera()

def draw_layer_b(x, y, shiftx, shifty):
	cx = x >> shiftx
	cy = y >> shifty
	dx = cx - (camera.left >> shiftx)
	dy = cy - (camera.top >> shifty)

	# print ('[layer B] x=%d y=%d dx=%d dy=%d' % (cx, cy, dx, dy))

	if dx > 0:
		draw_rect(layer_B, cx + 20, cy, 1, 15)
	elif dx < 0:
		draw_rect(layer_B, cx, cy, 1, 15)

	if dy > 0:
		draw_rect(layer_B, cx, cy + 14, 21, 1)
	elif dy < 0:
		draw_rect(layer_B, cx, cy, 21, 1)
	
def set_camera(camera_new_x, camera_new_y):
	dx = camera_new_x - camera.left #Globs.camera_x
	dy = camera_new_y - camera.top #Globs.camera_y

	camera.moves_left = (dx < 0)
	camera.moves_right = (dx > 0)
	camera.moves_up = (dy < 0)
	camera.moves_down = (dy > 0)

	dx = camera_new_x//16 - camera.left//16
	dy = camera_new_y//16 - camera.top//16

	# print ('[layer A] x=%d y=%d dx=%d dy=%d' % (camera_new_x//16, camera_new_y//16, dx, dy))

	if dx > 0:
		draw_rect(layer_A, camera_new_x//16 + 20, camera_new_y//16, 1, 15)
	elif dx < 0:
		draw_rect(layer_A, camera_new_x//16, camera_new_y//16, 1, 15)

	if dy > 0:
		draw_rect(layer_A, camera_new_x//16, camera_new_y//16 + 14, 21, 1)
	elif dy < 0:
		draw_rect(layer_A, camera_new_x//16, camera_new_y//16, 21, 1)

	if Globs.layer_B_drawing_method == 0:
		pass
	elif Globs.layer_B_drawing_method == 1:
		draw_layer_b(camera_new_x, camera_new_y, 4, 4)
	elif Globs.layer_B_drawing_method == 2:
		draw_layer_b(camera_new_x, camera_new_y, 5, 4)

	# camera.old_left = camera.left
	# camera.old_top = camera.top
	# Globs.camera_x = camera_new_x
	# Globs.camera_y = camera_new_y

	camera.left = camera_new_x
	# camera.virtual_left = camera_new_x - camera.delta_x
	camera.right = camera_new_x + 319
	# camera.virtual_right = camera_new_x + 319 + camera.delta_x
	camera.top = camera_new_y
	# camera.virtual_top = camera_new_y - camera.delta_y
	camera.bottom = camera_new_y + 223
	# camera.virtual_bottom = camera_new_y + 223 + camera.delta_y


def set_camera_focus_to(obj):
	camera.focus = obj

	camera_x = int(obj.x) - 128 #160

	camera_x = max(0, camera_x)
	camera_x = min(Globs.layer_a_pwidth - 320, camera_x)

	camera_y = int(obj.y) - 119

	camera_y = max(0, camera_y)
	camera_y = min(Globs.layer_a_pheight - 223, camera_y)
	
	# set_camera(camera_x, camera_y)
	draw_rect(layer_A, camera_x // 16, camera_y // 16, 21, 15)
	if Globs.layer_B_drawing_method == 0:
		pass
	elif Globs.layer_B_drawing_method == 1:
		draw_rect(layer_B, camera_x // 16, camera_y // 16, 21, 15)
	elif Globs.layer_B_drawing_method == 2:
		draw_rect(layer_B, camera_x // 32, camera_y // 16, 21, 15)

	# Globs.old_camera_x = camera_x
	# Globs.old_camera_y = camera_y
	# Globs.camera_x = camera_x
	# Globs.camera_y = camera_y

	camera.left = camera_x
	# camera.virtual_left = camera_x - camera.delta_x
	camera.right = camera_x + 319
	# camera.virtual_right = camera_x + 319 + camera.delta_x
	camera.top = camera_y
	# camera.virtual_top = camera_y - camera.delta_y
	camera.bottom = camera_y + 223
	# camera.virtual_bottom = camera_y + 223 + camera.delta_y

def clamp(x, a, b):
	return min(max(a, x), b)

def update_camera():
	obj = camera.focus

	
	# camera_x = clamp(int(obj.x) - 160, 0, Globs.layer_a_pwidth - 320)
	camera_x = clamp(int(obj.x) - 128, 0, Globs.layer_a_pwidth - 320)

	# adjust camera_y
	camera_y = camera.top
	y = int(obj.y)
	sy = y - camera_y

	if sy < 64:
		camera_y = y - 64
	elif sy < 120:# and camera_y > 0:
		camera_y -= 1
	elif sy == 120:
		pass
	elif sy <= 208: # and camera_y < Globs.layer_a_pheight - 224:
		camera_y += 1
	else:
		camera_y = y - 208
	# print ('y = %s, sy = %s, camera_y = %s' % (y, sy, camera_y))
	
	# camera_y = clamp(sy, 64, 208)
	# if camera_y < 120:
		# camera_y -= 1
	# elif camera_y > 120:
		# camera_y += 1
		
	# # print ('camera: vscroll_mode = %d' % Globs.vscroll_mode)
	# if Globs.vscroll_mode == 0:
		# # when musashi walks
		# # try to have y = 128
		# # if not, move by 1 pixel
		# if sy < 120 and camera_y > 0:
			# camera_y -= 1
		# elif sy > 120 and camera_y < Globs.layer_a_pheight - 224:
			# camera_y += 1
		
	# elif Globs.vscroll_mode == 1:
		# if sy < 64:
			# Globs.vscroll_mode = 2
			# sy = 64
			# camera_y = y - 64
			# if camera_y < 0:
				# camera_y = 0
				# sy = y
		# elif sy > 208:
			# sy = 208
			# camera_y = y - 208
			# if camera_y >= Globs.layer_a_pheight - 224:
				# camera_y = Globs.layer_a_pheight - 224
				# sy = y - camera_y
			# GP.vscroll_mode = 2
				
	# elif Globs.vscroll_mode == 2:
		# if sy < 64:
			# sy = 64
			# camera_y = y - 64
			# if camera_y < 0:
				# camera_y = 0
				# sy = y
		# elif sy > 208:
			# sy = 208
			# camera_y = y - 208
			# if camera_y >= Globs.layer_a_pheight - 224:
				# camera_y = Globs.layer_a_pheight - 224
				# sy = y - camera_y
			# GP.halt()
		
		# elif Globs.musashi.speed_y < 0:
			# camera_y -= 1
		
		# elif Globs.musashi.speed_y > 0:
			# camera_y += 1

	camera_y = clamp(camera_y, 0, Globs.layer_a_pheight - 224)

	set_camera(camera_x, camera_y)
	# print ('camera = (%d, %d, %d, %d) // object = (%d, %d)' % (camera.left, camera.right, camera.top, camera.bottom, obj.x, obj.y))

	GP.plane_A_offset = -camera_x, camera_y
	if Globs.layer_B_drawing_method == 0:
		pass
	if Globs.layer_B_drawing_method == 1:
		GP.plane_B_offset = -camera_x, camera_y
	if Globs.layer_B_drawing_method == 2:
		GP.plane_B_offset = -camera_x//2, camera_y#//2
