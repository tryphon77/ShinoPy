from map_from_scratch import *
from make_objects_list_4 import *


source_dir = 'C:\\Users\\fterr\\Documents\\hack\\Shinobi\\maps'


def print_map(map_, n_digits = 2):
	printed_lines = []
	f_str = '0x%0' + str(n_digits) + 'X'
	for row in map_:
		printed_lines += ['\t' + (', '.join([(f_str) % x for x in row]))]
	return ',\n'.join(printed_lines)

def print_tilemap(layer, base, prioritized_tiles = []):			
	def fmt(v):
		if v is None:
			return '0'
		elif v.id_ in prioritized_tiles:
			return ('0x%04X' % (0x8000 + base + v.id_))			
		else:
			return ('0x%04X' % (base + v.id_))

	printed_lines = []
	for row in layer.map:
		printed_lines += ['\t' + (', '.join([fmt(x) for x in row]))]
	return ',\n'.join(printed_lines)
	
def fmt_attrs(attrs):
	i = 0
	res = []
	while i < len(attrs):
		res += ['\t' + ', '.join(['0x%02X' % x for x in attrs[i : i + 8]])]
		i += 8
	return ',\n'.join(res)

def generate(mission, stage, drawing_method = 0, high_priority_tiles = [], priority = False, special_effect = 'None'):
	map_id = '%d-%d' % (mission, stage)
	tmx = load_tmx('%s/%s/%s.tmx' % (source_dir, map_id, map_id))

	header = 'from genepy import load_data_from_png\nfrom tsprite import allocate_tiles\n'


	# prioritized_patterns = set()

	def fmt(v):
		if v is None:
			return '0'
		# elif v.id_ in prioritized_patterns:
			# return ('0x%04X' % (0x8000 + base + v.id_))
		else:
			attr = 0
			if v.hflip:
				attr |= 0x800
			elif v.vflip:
				attr |= 0x1000
			return ('0x%04X' % (base + attr + v.id_))
			
	layer_b = tmx.get_layer_by_name('layer b')
	layer_a = tmx.get_layer_by_name('layer a')
	collision_layer = tmx.get_layer_by_name('collisions')
	collisions = get_collmap(collision_layer)
		
	blank_tile = pygame.Surface((8, 8))
	blank_tile.fill(pygame.Color(0xFF, 0x00, 0xDC, 0xFF))
	patterns = []
	base = 0x40
	tiles_data = []

	base_a = 0
	base_b = 0
	
	if layer_b:
		for i, image in enumerate(layer_b.tileset):
			tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
			tile_data = []
			for row in tiled.map:
				tile_data += row
				# if i in high_priority_tiles:		
					# prioritized_patterns.update([x.id_ for x in row])
			tiles_data += [tile_data]

		base_a = len(layer_b.tileset)
		
	
	for i, image in enumerate(layer_a.tileset):
		tiled = PTiledMap.from_surface(image, (8, 8), check_flips, tileset = patterns)
		tile_data = []
		for row in tiled.map:
			tile_data += row
			if i in high_priority_tiles:
				print (i, row)
				# prioritized_patterns.update([x.id_ for x in row])
		tiles_data += [tile_data]

	print ('base_a = %X\nbase_b = %X' % (base_a, base_b))
	print ('%s patterns generated' % len(patterns))
	# if 0 in prioritized_patterns:
		# prioritized_patterns.remove(0)
	# print (prioritized_patterns)

	printed_tiles = []
	for tile in tiles_data:
		printed_tiles += ['\t' + (', '.join([fmt(x) for x in tile]))]
	res = 'tileset = [\n%s\n]\n\n' % ',\n'.join(printed_tiles)
	
	# res += 'tileset_attributes = [\n%s\n]\n\n' % fmt_attrs(get_attributes(layer_a, collision_layer, len(tiles_data)))

	# print (get_floors_map(collision_layer))

	res += 'tilemap_A = [\n%s\n]\n\n' % print_tilemap(layer_a, base_a, high_priority_tiles)
	if layer_b:
		res += 'tilemap_B = [\n%s\n]\n\n' % print_tilemap(layer_b, base_b)
	
	res += 'collision_map = [\n%s\n]\n\n' % print_map(collisions, 4)
	
	res += 'nb_ptrns = 0x%X\n\n' % len(patterns)
	
	res += 'twidth = %d\ntheight = %d\n\n' % (len(layer_a.map[0]), len(layer_a.map))
	
	res += 'drawing_method = %d\n\n' % drawing_method
	
	res += 'priority = %s\n\n' % ['0', '0x8000'][priority]
	
	# res += 'special_effect = %s\n\n' % special_effect
	
	res += "patterns = load_data_from_png('res/levels/level_%d_%d.png')\n\n" % (mission, stage)
	
	res += '# ========================================================\n\n'


	print ('generating objects ressources')

	objects_path = '%s/%s/objects.txt' % (source_dir, map_id)
	
	h, r = generate_objects_ressources(tmx, objects_path, collisions)
	header += '\n' + h + '\n\n\n'
	res += r
	
	with open('%s/%s/level_%d_%d.py' % (source_dir, map_id, mission, stage), 'w') as f:
		f.write(header)
		f.write(res)

	export_tileset(patterns, '%s/%s/level_%d_%d.png' % (source_dir, map_id, mission, stage))

	if True:
		def to_color(x):
			return pygame.Color(x * 0x100)

		w, h = tmx.get_size()
		collision_surf = pygame.Surface((w * 16, h * 16))
		for y in range(h):
			for x in range(w):
				pygame.draw.rect(collision_surf, to_color(collisions[y][x]), (x * 16, y * 16, 16, 16)) 
		pygame.image.save(collision_surf, '%s/%s/collision_map.png' % (source_dir, map_id))
	

import sys

if '0-1' in sys.argv:
	generate(0, 1, drawing_method = 0, priority = False)

if '0-2' in sys.argv:
	generate(0, 2, drawing_method = 0, priority = False)

if '1-1' in sys.argv:
	generate(1, 1, drawing_method = 2, high_priority_tiles = [28, 29, 30, 33], priority = True)
if '1-2' in sys.argv:
	generate(1, 2, drawing_method = 2, priority = True)
if '1-3' in sys.argv:
	generate(1, 3, drawing_method = 1, priority = True)

if '2-1' in sys.argv:
	generate(2, 1, drawing_method = 2, high_priority_tiles = [83, 84, 85, 86, 104, 105, 122, 123, 124, 131, 132, 133, 134, 141, 142, 143, 144, 154, 160, 162, 167, 168, 169, 170, 171, 178], priority = True)
if '2-2' in sys.argv:
	generate(2, 2, drawing_method = 0, priority = True)
if '2-3' in sys.argv:
	generate(2, 3, drawing_method = 2, high_priority_tiles = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57], priority = False, special_effect = 'splash')
if '2-4' in sys.argv:
	generate(2, 4, drawing_method = 2, priority = True)
	
if '3-1' in sys.argv:
	generate(3, 1, drawing_method = 2, high_priority_tiles = [19, 20, 25, 31, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47], priority = False)
if '3-2' in sys.argv:
	generate(3, 2, drawing_method = 1, priority = True)
if '3-3' in sys.argv:
	generate(3, 3, drawing_method = 1, high_priority_tiles = range(0, 0 + 57), priority = True)
if '3-4' in sys.argv:
	generate(3, 4, drawing_method = 1, priority = True)

if '4-1' in sys.argv:
	generate(4, 1, drawing_method = 2, priority = True)
if '4-2' in sys.argv:
	generate(4, 2, drawing_method = 1, priority = True)
if '4-3' in sys.argv:
	generate(4, 3, drawing_method = 1, priority = True)
if '4-4' in sys.argv:
	generate(4, 4, drawing_method = 0, priority = True)

if '5-1' in sys.argv:
	generate(5, 1, drawing_method = 2, high_priority_tiles = [19], priority = False)
if '5-2' in sys.argv:
	generate(5, 2, drawing_method = 2, high_priority_tiles = [1, 2, 6, 7, 18, 28, 35, 36, 37, 38, 39, 40, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 6, 61, 62, 63, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 800, 81, 82, 83, 84, 85, 86, 87, 88, 89] + list(range(92, 156)), priority = True)
if '5-3' in sys.argv:
	generate(5, 3, drawing_method = 1, priority = True)
if '5-4' in sys.argv:
	generate(5, 4, drawing_method = 1, priority = True)
	
