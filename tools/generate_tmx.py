import pygame, numpy

def print_array(a):
	print ('\n'.join(
		[' '.join(['%08X' % x for x in row])
		for row in a]))

# pygame.init()
# display = pygame.display.set_mode((320, 224))

# blank_tile_1 = pygame.image.load('blank.png').convert_alpha()

# blank_tile_2 = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
# blank_tile_2.fill(pygame.Color(0xFF, 0x00, 0xDC, 0xFF))

# b1 = pygame.surfarray.pixels2d(blank_tile_1)
# p1 = pygame.PixelArray(blank_tile_1)
# print_array(b1)

# b2 = pygame.surfarray.pixels2d(blank_tile_2)
# p2 = pygame.PixelArray(blank_tile_2)
# print_array(b2)

# exit()

from map_from_scratch import *

def generate_tmx(input_path, output_path):
	image = pygame.image.load(input_path).convert_alpha()

	blank_tile = pygame.Surface((16, 16), flags = pygame.SRCALPHA).convert_alpha()
	blank_tile.fill(pygame.Color(0xFF, 0x00, 0xDC, 0xFF))
	
	tiled = PTiledMap.from_surface(image, (16, 16), ignore_flips, tileset = [blank_tile])
	print ('%s tiles generated' % len(tiled.tileset))
			
	save_as_tmx(tiled, output_path)

# ======================================================

pygame.init()
display = pygame.display.set_mode((320, 224))

map_id = '5-4'
source_dir = 'C:\\Users\\fterr\\Documents\\hack\\Shinobi\\maps'

if False:
	input_path = '%s/%s/2-3b.png' % (source_dir, map_id)
	output_path = '%s/%s/tileset.tmx' % (source_dir, map_id)
	print (os.path.exists(input_path))
	image = pygame.image.load(input_path) #.convert_alpha()

	tiled = PTiledMap.from_surface(image, (8, 8), ignore_flips, tileset = [])
	print ('%s tiles generated' % len(tiled.tileset))
			
	save_as_tmx(tiled, output_path)
	exit()

generate_tmx(
	'%s/%s/layer_a.png' % (source_dir, map_id), 
	'%s/%s/%sa.tmx' % (source_dir, map_id, map_id)
)

if True:
	generate_tmx(
		'%s/%s/layer_b.png' % (source_dir, map_id), 
		'%s/%s/%sb.tmx' % (source_dir, map_id, map_id)
	)

