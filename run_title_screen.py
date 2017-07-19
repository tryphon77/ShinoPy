import random
from globals import Globs

from genepy import *
from tsprite import *
from object import *
from tsprite import *

from res.title.data import *
from res.misc.data import *
from res.levels.mission_screen import *


logo_pos = [
	(-90, 105), (-74, 153), (-50, 196), (-18, 234), (20, 264), (64, 286), (111, 300), (160, 304), 
	(208, 298), (254, 283), (296, 259), (332, 228), (362, 191), (383, 148), (396, 103), (400, 55), 
	(394, 9), (379, -35), (357, -75), (326, -110), (290, -139), (249, -160), (205, -172), (160, -176), 
	(114, -170), (71, -156), (32, -134), (-1, -105), (-28, -70), (-48, -30), (-60, 12), (-64, 56), 

	(-58, 99), (-45, 140), (-23, 178), (4, 211), (38, 238), (76, 257), (117, 268), (160, 272), 
	(201, 266), (241, 253), (278, 233), (309, 205), (335, 173), (354, 136), (364, 96), (368, 56),
	(363, 15), (350, -22), (330, -57), (304, -88), (272, -112), (237, -130), (199, -141), (160, -144), 
	(121, -139), (84, -126), (50, -107), (21, -82), (-2, -52), (-19, -18), (-29, 18), (-32, 56), 

	(-27, 93), (-15, 128), (2, 161), (27, 188), (56, 211), (88, 227), (123, 237), (160, 240), 
	(195, 235), (229, 224), (260, 206), (287, 183), (308, 155), (324, 124), (333, 90), (336, 55), 
	(331, 21), (320, -10), (303, -40), (281, -65), (255, -86), (225, -101), (192, -109), (160, -112), 
	(127, -107), (96, -97), (68, -81), (44, -59), (24, -34), (10, -5), (2, 24), (0, 56), 

	(4, 87), (14, 116), (29, 143), (49, 166), (73, 184), (101, 198), (130, 206), (160, 208), 
	(189, 204), (217, 194), (242, 179), (264, 160), (282, 137), (294, 111), (302, 84), (304, 55), 
	(300, 28), (291, 1), (277, -22), (258, -42), (237, -59), (212, -71), (186, -78), (160, -80), 
	(133, -76), (108, -67), (86, -54), (66, -37), (51, -16), (39, 6), (33, 30), (32, 56), 

	(35, 80), (43, 104), (56, 125), (72, 143), (91, 158), (113, 168), (136, 174), (160, 176), 
	(183, 172), (205, 165), (225, 153), (242, 138), (255, 119), (265, 99), (270, 78), (272, 55), 
	(268, 34), (261, 13), (250, -4), (236, -20), (219, -32), (200, -41), (180, -46), (160, -48), 
	(139, -45), (120, -38), (103, -27), (89, -14), (77, 0), (69, 18), (64, 37), (64, 56), 

	(66, 74), (73, 91), (82, 107), (94, 121), (109, 131), (125, 139), (142, 143), (160, 144), 
	(176, 141), (192, 135), (207, 126), (219, 115), (229, 102), (235, 87), (239, 71), (240, 55), 
	(237, 40), (232, 26), (224, 13), (213, 2), (201, -6), (188, -12), (174, -15), (159, -16), 
	(146, -13), (133, -8), (121, -1), (111, 7), (104, 18), (99, 30), (96, 43), (96, 56), 

	(98, 68), (102, 79), (109, 89), (117, 98), (127, 105), (137, 109), (148, 111), (160, 112), 
	(170, 109), (180, 105), (189, 100), (196, 92), (202, 84), (206, 75), (208, 65), (208, 55), 
	(206, 46), (202, 38), (197, 30), (191, 24), (183, 20), (176, 17), (167, 15), (160, 16), 
	(152, 17), (145, 20), (139, 25), (134, 30), (130, 36), (128, 42), (127, 49), (128, 56), 

	(129, 62), (132, 67), (135, 72), (140, 75), (144, 78), (150, 80), (155, 80), (160, 80), 
	(164, 78), (168, 76), (171, 73), (174, 70), (175, 66), (176, 62), (176, 59), (176, 56), 
	(174, 53), (172, 50), (170, 48), (168, 47), (166, 46), (163, 46), (161, 47), (160, 48), 
	(158, 49), (157, 50), (157, 51), (157, 53), (157, 54), (158, 55), (159, 55), (160, 56)
]


def print_at(plane, x, y, text):
	for c in text:
			GP.set_tilemap(plane, ord(c) + 0x7FE0, x, y)
			x += 1


def init_logo_sprite(vpos):
	logo_sprite = allocate_static_sprite()
	logo_sprite.vpos = vpos

	logo_sprite.status = 1
	logo_sprite.x = -90
	logo_sprite.y = 105
	# logo_sprite.patterns = kanji
	logo_sprite.frames_table = frames_table
	logo_sprite.animations_table = animations_table
	logo_sprite.bboxes_table = bounding_boxes
	logo_sprite.hitboxes = hitboxes

	logo_sprite.frame = -1
	# logo_sprite.patterns_blocks = patterns_blocks

	set_animation(logo_sprite, 0)
	return logo_sprite


def init_spark_sprite():
	spark_sprite = allocate_static_sprite()
	spark_sprite.vpos = 0x400

	spark_sprite.status = 1
	spark_sprite.x = 128
	spark_sprite.y = 128
	spark_sprite.frames_table = spark_frames_table
	spark_sprite.animations_table = spark_animations_table
	spark_sprite.bboxes_table = spark_bounding_boxes
	spark_sprite.hitboxes = spark_hitboxes

	spark_sprite.frame = -1

	set_animation(spark_sprite, 0)
	return spark_sprite


def main():
	GP.load_tile_data(patterns, 0x40)
	GP.load_tile_data(kanji, 0x200)
	GP.load_tile_data(sparks, 0x400)
    
	font_patterns = load_data_from_png('res/small_font.png')
	GP.load_tile_data(font_patterns, 0)

	GP.set_tilemap_data_rect(GP.plane_A, tilemap_a, 0, 0, 40, 28)
	GP.set_tilemap_data_rect(GP.plane_B, tilemap_b, 0, 0, 40, 28)

	for i in range(6):
		if i & 1:
			init_logo_sprite(0x290)
		else:
			init_logo_sprite(0x200)

	# first loop : rolling kanji
	ticks = 0
	old_joy = 0
	while True:
		Globs.link = 0

		joy = GP.read_joypad(0)
		Globs.joy_pressed = (~old_joy) & joy
		old_joy = joy
		Globs.joy = joy
		if joy & BUTTON_START:
			break

		if ticks == 60:
			GP.set_tilemap_data_rect(GP.plane_A, tilemap_a1, 15, 15, 11, 2)
		elif ticks == 150:
			GP.set_tilemap_data_rect(GP.plane_A, tilemap_a0, 15, 15, 11, 2)
		elif ticks == 156:
			GP.set_tilemap_data_rect(GP.plane_A, tilemap_a2, 15, 15, 11, 2)
		elif ticks == 246:
			GP.set_tilemap_data_rect(GP.plane_A, tilemap_a0, 15, 15, 11, 2)
		elif ticks == 268:
			break

		GP.sprite_cache[Globs.link - 1].link = 0

		k = ticks
		for j in range(6):
			logo_sprite = static_sprites[j]
			if 0 < k < 256:
				logo_sprite.x, logo_sprite.y = logo_pos[k]
			k += 2

			sprite_update(logo_sprite)

		GP.wait_vblank()
		ticks += 1

	# 2nd loop : select screen
	
	clear_all_sprites()
	ticks = 0
	
	logo_sprite = init_logo_sprite(0x290)
	logo_sprite.x, logo_sprite.y = 160, 56
	spark_sprite = init_spark_sprite()

	GP.set_tilemap_data_rect(GP.plane_A, tilemap_a0, 15, 15, 11, 2)
	print_at(GP.plane_B, 18, 18, "START")
	print_at(GP.plane_B, 17, 20, "OPTIONS")
	
	Globs.selector = 0
	while not Globs.next_state:
		
		joy = GP.read_joypad(0)
		Globs.joy_pressed = (~old_joy) & joy
		old_joy = joy
		Globs.joy = joy

		if Globs.joy_pressed & (BUTTON_UP | BUTTON_DOWN):
			ticks = 0
			Globs.selector ^= 1
		if Globs.joy_pressed & (BUTTON_C | BUTTON_START):
			Globs.next_state = run_selection

		if spark_sprite.is_animation_over:
			release_sprite(spark_sprite)
		elif ticks == 64:
			Globs.next_state = run_demo

		Globs.link = 0
		for s in static_sprites:
			if s.status == 0:
				break
			sprite_update(s)
		GP.sprite_cache[Globs.link - 1].link = 0

		ticks += 1
		GP.wait_vblank()
	
	Globs.next_state()


def run_demo():
	print ('Demo game : not yet implemented!')
	exit()


def blink(x, y, txt1, txt2):

	for _ in range(4):
		for _ in range(4):
			print_at(GP.plane_B, x, y, txt1)
			GP.wait_vblank()
		for _ in range(4):
			print_at(GP.plane_B, x, y, txt2)
			GP.wait_vblank()

def run_selection():
	if Globs.selector == 0:
		blink(18, 18, "START", "     ")
		run_start_game()
	else:
		blink(17, 20, "OPTIONS", "       ")
		run_option()


level_table = [
	(1, 1), (1, 2), (1, 3),
	(2, 1), (2, 2), (2, 3), (2, 4),
	(3, 1), (3, 2), (3, 3), (3, 4),
	(4, 1), (4, 2), (4, 3), (4, 4),
	(5, 1), (5, 2), (5, 3), (5, 4)
]

mission_text = [
	(8, 14, '"PURSUE THE TERRORISTS"')
]

def type_print(x, y, txt):
	for c in txt:
		print_at(GP.plane_B, x, y, c)
		for _ in range(5):
			GP.wait_vblank()
		x += 1

def run_mission_text():
	GP.load_tile_data(mission_patterns, 0x40)
	GP.fill_tilemap_rect(GP.plane_A, 0x40, 0, 0, 40, 28)
	GP.fill_tilemap_rect(GP.plane_B, 0, 0, 0, 40, 28)
	GP.set_tilemap_data_rect(GP.plane_A, mission_tilemap, 13, 7, 15, 2)
	
	for x, y, txt in mission_text:
		type_print(x, y, txt)
	
	for _ in range(35):
		GP.wait_vblank()

stage_presentation = [
	(mission_screen_1_patterns, mission_screen_1_tilemap)
]

def move_stage_presentation(dir, offset):
	if dir == 0:
		GP.plane_A_offset = offset, offset
	elif dir == 1:
		GP.plane_A_offset = -offset, offset
	elif dir == 2:
		GP.plane_A_offset = -offset, -offset
	elif dir == 3:
		GP.plane_A_offset = offset, -offset
		
def run_stage_presentation():
	direction = random.randint(0, 3)
	patterns, tilemap = stage_presentation[Globs.mission - 1]
	GP.load_tile_data(patterns, 0x40)
	GP.fill_tilemap_rect(GP.plane_A, 0, 0, 0, 64, 64)
	GP.fill_tilemap_rect(GP.plane_B, 0, 0, 0, 64, 64)
	GP.set_tilemap_data_rect(GP.plane_A, tilemap, 10, 1, 20, 26)
	offset = 240
	old_joy = 0

	for _ in range(15):
		offset -= 16
		move_stage_presentation(direction, offset)
		GP.wait_vblank()
	
	for _ in range(120):
		joy = GP.read_joypad(0)
		Globs.joy_pressed = (~old_joy) & joy
		old_joy = joy
		Globs.joy = joy

		if Globs.joy_pressed & (BUTTON_A | BUTTON_B | BUTTON_C | BUTTON_START):
			break
		
		GP.wait_vblank()

	for _ in range(15):
		offset -= 16
		move_stage_presentation(direction, offset)
		GP.wait_vblank()
	
	exit()
	

def run_init_level():
	Globs.mission, Globs.stage = level_table[Globs.lvl]
	if Globs.stage == 1 and Globs.show_mission_text:
		run_mission_text()
		show_mission_text = False
	
	run_stage_presentation()
	
	exit()
	
def run_start_game():
	clear_all_sprites()
	Globs.lvl = 0
	run_init_level()


def run_option():
	print ('option : not yet implemented!')
	exit()

if __name__ == '__main__':
	GP.init()
	main()
