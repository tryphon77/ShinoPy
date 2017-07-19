import sys
sys.path.append('../../pygato')

import pygame

from map import *
from tmx import *

def fmt(tile):
	res = tile.id_
	if tile.hflip:
		res |= 0x800
	if tile.vflip:
		res |= 0x1000
	if tile.priority:
		res |= 0x8000
	return res

def split_with_tags(s, open_tag = '[', close_tag = ']'):
	res = []
	i = 0
	while i < len(s):
		c = s[i]
		i += 1
		print (c)
		if c == open_tag:
			while s[i] != close_tag:
				print (c)
				c += s[i]
				i += 1
			c += s[i]
			i += 1
		res += [c]
	return res

def get_collmap(map_):
	# print ('get_collmap')
	impulsion = [1, 1, 2, 3, 4, 5, 5, 5, 6, 6, 7, 7, 7]
	res = [[ x.id_ if x.id_ < 8 else 0 for x in row] for row in map_]
	for y, row in enumerate(map_):
		for x, tile in enumerate(row):
			code = tile.id_
			# print ('code %X' % code)
			if 8 <= code < 16:
				# print ('code %X' % code)
				floor = code - 8
				for y1 in range(y + 1, 100):
					trg = (map_[y1][x].id_ & 7)
					# print ('trg %X' % trg)
					if trg == floor + 1:
						# print ('jump H at %d, %d | height = %d | impulsion = %s' % (x, y1, y1 - y - 1, impulsion[y1 - y - 2]))
						# res[y1][x] += impulsion[y1 - y - 2] << 6
						res[y1][x] += (y1 - y - 1) << 8
					if trg == floor:
						# print ('jump L at %d, %d | height = %d | impulsion = %s' % (x, y1, y1 - y - 1, impulsion[y1 - y - 2]))
						# res[y1][x] += impulsion[y1 - y - 2] << 3
						res[y1][x] += (y1 - y - 1) << 4
						break
	
	return res

	
if True:
	# generate map from tmx
	tmx = load_tmx('level00.tmx')
	layer_a, collisions = tmx
	patterns = []
	base = 0x40
	tiles_data = []
	
	for image in layer_a.tileset:
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		tile_data = []
		for row in tiled.map:
			tile_data += row
		tiles_data += [tile_data]

	print ('%s patterns generated' % len(patterns))

	print ('tileset = [')
	for tile in tiles_data:
		print ('\t' + (', '.join(['0x%04X' % (base + fmt(x)) for x in tile])) + ',')
	print (']\n')
	
	export_tileset(patterns, 'patterns00.png')

	print ('tilemap_A = [')
	for row in layer_a.map:
		print ('\t' + (', '.join([('0x%04X' % (x.id_)) for x in row])) + ',')
	print (']\n')
	
	print ('tilemap_B = None\n')
			
	print ('collision_map = [')
	for row in get_collmap(collisions.map):
		print ('\t' + (', '.join([('0x%04X' % x) for x in row])) + ',')
	print (']\n')

	exit()

	
if False:
	# generate map from tmx
	tmx = load_tmx('level11a.tmx')
	layer_a, collisions, effects, objects = tmx
	layer_b = load_tmx('level11b.tmx')
	patterns = []
	base = 0x40
	tiles_data = []
	
	for image in layer_a.tileset:
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		tile_data = []
		for row in tiled.map:
			tile_data += row
		tiles_data += [tile_data]

	print ('%s patterns generated' % len(patterns))

	print ('tileset = [')
	for tile in tiles_data:
		print ('\t' + (', '.join(['0x%04X' % (base + fmt(x)) for x in tile])) + ',')
	print (']\n')
	
	export_tileset(patterns, 'patterns11a.png')

	print ('tilemap_A = [')
	for row in layer_a.map:
		print ('\t' + (', '.join([('0x%04X' % x.id_) for x in row])) + ',')
	print (']\n')
	
	print ('tilemap_B = [')
	for row in layer_b.map:
		print ('\t' + (', '.join([('0x%04X' % x.id_) for x in row])) + ',')
	print (']\n')
			

	print ('collision_map = [')
	for row in get_collmap(collisions.map):
		print ('\t' + (', '.join([('0x%04X' % x) for x in row])) + ',')
	print (']\n')

	exit()

	
if False:
	# generate map from tmx
	tmx = load_tmx('level22.tmx')
	layer_a, collisions = tmx
	patterns = []
	base = 0x40
	tiles_data = []
	
	for image in layer_a.tileset:
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		tile_data = []
		for row in tiled.map:
			tile_data += row
		tiles_data += [tile_data]

	print ('%s patterns generated' % len(patterns))

	print ('tileset = [')
	for tile in tiles_data:
		print ('\t' + (', '.join(['0x%04X' % (base + fmt(x)) for x in tile])) + ',')
	print (']\n')
	
	export_tileset(patterns, 'patterns33.png')

	print ('tilemap_A = [')
	for row in layer_a.map:
		print ('\t' + (', '.join([('0x%04X' % (x.id_)) for x in row])) + ',')
	print (']\n')
	
	print ('tilemap_B = None\n')
			
	print ('collision_map = [')
	for row in get_collmap(collisions.map):
		print ('\t' + (', '.join([('0x%04X' % x) for x in row])) + ',')
	print (']\n')

	exit()


if False:
	# generate map from tmx
	tmx = load_tmx('level33.tmx')
	layer_b, layer_a, collisions = tmx
	patterns = []
	base = 0x40
	tiles_data = []
	
	base_b = 0
	
	for image in layer_b.tileset:
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		tile_data = []
		for row in tiled.map:
			tile_data += row
		tiles_data += [tile_data]

	base_a = len(layer_b.tileset)
		
	for image in layer_a.tileset:
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		tile_data = []
		for row in tiled.map:
			tile_data += row
		for t in tile_data:
			t.priority = True
		tiles_data += [tile_data]

	print ('%s patterns generated' % len(patterns))

	print ('tileset = [')
	for tile in tiles_data:
		print ('\t' + (', '.join(['0x%04X' % (base + fmt(x)) for x in tile])) + ',')
	print (']\n')
	
	export_tileset(patterns, 'patterns33.png')

	print ('tilemap_A = [')
	for row in layer_a.map:
		print ('\t' + (', '.join([('0x%04X' % (base_a + x.id_)) for x in row])) + ',')
	print (']\n')
	
	print ('tilemap_B = [')
	for row in layer_b.map:
		print ('\t' + (', '.join([('0x%04X' % (base_b + x.id_)) for x in row])) + ',')
	print (']\n')
			
	print ('collision_map = [')
	for row in get_collmap(collisions.map):
		print ('\t' + (', '.join([('0x%04X' % x) for x in row])) + ',')
	print (']\n')

	exit()

	
if False:
	raw = pygame.image.load('font_raw.png')

	
	tiled = PTiledMap.from_surface(raw, (8, 8), ignore_flips)
	export_tileset(tiled.tileset, 'unordered_font.png')
	
	encoding = split_with_tags(
		""" [back].'"/()-[male][female][dot][shuriken][ed]=0"""\
		"""123456789ABCDEFG"""\
		"""HIJKLMNOPQRSTUVW"""\
		"""XYZ[quote1][quote2],[hyphen][quote3]![square]"""
	)
		
	new_encoding = split_with_tags(
		""" !"[quote1][quote2][quote3][square]'()[dot][shuriken],-./"""\
		"""0123456789[male][female][hyphen]=>?"""\
		"""@ABCDEFGHIJKLMNO"""\
		"""PQRSTUVWXYZ[back][ed]]^_"""
	)
	
	ordered = []
	for c in new_encoding:
		if c in encoding:
			j = encoding.index(c)
		else:
			j = encoding.index('[square]')
		ordered += [tiled.tileset[j]]
	
	export_tileset(ordered, 'ordered_font.png')
	
	
if False:
	base_dir = 'C:\\Users\\fterr\\Documents\\hack\\Shinobi\\maps\\3-3'
	image = pygame.image.load('%s/wip2b.png' % base_dir)
	
	tiled = PTiledMap.from_surface(image, (16, 16), ignore_flips)
	print ('%s tiles generated' % len(tiled.tileset))
			
	save_as_tmx(tiled, '%s/tiled2b.tmx' % base_dir)

	exit()


if False:
	patterns = []
	for image_path, base in [('spark1.png', 0), ('spark2.png', 0), ('spark3.png', 0)]:
		image = pygame.image.load(image_path)
		
		tiled = PTiledMap.from_surface(image, (8, 8), ignore, sprite_order, tileset = patterns)
		print ('%s patterns generated' % len(patterns))
				
	export_tileset(patterns, 'sparks.png')

	exit()

if False:
	patterns = []
	for image_path, base in [('map1.png', 0x40)]:
		image = pygame.image.load(image_path)
		
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		print ('%s patterns generated' % len(patterns))
		
		for row in tiled.map:
			print ('\t' + (', '.join(['0x%04X' % (base + fmt(x)) for x in row])) + ',')
		print ('====')
		
	export_tileset(patterns, 'patterns.png')

	exit()
	
if False:
	image = pygame.image.load('kanji.png')

	tiled = PTiledMap.from_surface(image, (32, 32), ignore)

	patterns = []
	for spr in tiled.tileset:
		s = PTiledMap.from_surface(spr, (8, 8), ignore, sprite_order, tileset = patterns)
		print (len(patterns))
	
	export_tileset(patterns, 'kanji_patterns.png')
	exit()
