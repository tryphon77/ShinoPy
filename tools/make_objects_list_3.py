import sys
sys.path.append('../../pygato')

import pygame

from map import *
from tmx import *

d_left = -13
d_right = 9
d_top = -7
d_bottom = 7

# ======================================================
# parse maps 

def left_to_right(w, h):
	for x in range(w):
		for y in range(h):
			yield (x, y)

def make_list(layer, names, order):
	res = []
	w, h = layer.get_size()
	for (x, y) in order(w, h):
		cell = layer[y][x]
		if cell is not None:
			t = cell.id_
			obj = obj_name[t]
			print ('\t%s: %d, %d' % (obj, x, y))
			if cell.hflip:
				dir = 'right'
			else:
				dir = 'left'
			res += [(obj_name[t], dir, x, y)]
	return res


obj_name = ['musashi', 'punk', 'shooter', 'pink_guardian', 'hostage', 'knife', 'spider', 'cross', 
'kenoh', 'blue_bazooka', 'green_bazooka', 'green_guardian', 'green_ninja', 'blue_ninja', 'red_ninja', 'frogman',
'toad_a', 'toad_b', 'bird', 'skeleton', 'monk', 'rolling', '', '',
'', '', '', '', '', '', '', '',
'', '', '', '', '', '', '', '',
'up', 'down', '', '', '', '', 'tl_bracket', 'rb_bracket',
'cross 9', 'cross A', 'cross B', 'cross C', 'cross D', 'cross E', 'cross F', 'cross 10',
'cross 1', 'cross 2', 'cross 3', 'cross 4', 'cross 5', 'cross 6', 'cross 7', 'cross 8'
]

monodirectional_objects = ['punk', 'shooter', 'knife', 'toad_a', 'toad_b', 'bird', 'blue_bazooka', 'green_bazooka']

# =======================================================

def read_param_file(path):
	def _read_object(ls, current_name):
		res = {'name': current_name}
		while True:
			line = next(ls)
			l = line.strip()
			if l:
				g, d = l.split('=')
				res[g.strip()] = d.strip()
			else:
				return res

	with open(path) as f:
		lines = iter(f.readlines())
	
	res = []
	current_name = ''
	try:
		while True:
			line = next(lines)
			if line.startswith('$'):
				current_name = line.strip()
			if line.startswith('object'):
				res += [_read_object(lines, current_name)]
	except StopIteration:
		return res

# =======================================================

def dir_to_bool(dir):
	return ['True', 'False'][dir == 'right']

def musashi_fun(params, dir):
	return "None"

def punk_fun(params, dir):
	return dir_to_bool(dir)
	
def shooter_fun(params, dir):
	return '(%s, %s)' % (dir == 'left', ['standing', 'sitting', 'lying'].index(params['option']))

def pink_guardian_fun(params, dir):
	return '(%s, %s)' % (dir_to_bool(dir), params['hostage'])

def hostage_fun(params, dir):
	return "None"

def knife_fun(params, dir):
	return dir_to_bool(dir)

def spider_fun(params, dir):
	return "None"

def kenoh_fun(params, dir):
	return "None"

def green_bazooka_fun(params, dir):
	return '(%s, %s)' % (dir_to_bool(dir), params.get('mobile', 'True'))

def blue_bazooka_fun(params, dir):
	return '(%s, %s)' % (dir_to_bool(dir), params.get('range', '0'))

def green_guardian_fun(params, dir):
	return ('(%s, %s, %s, %s, %s)' % (\
		dir_to_bool(dir),
		params.get('range', '0'),
		params.get('nervosity', '5'),
		params.get('hostage', '0'),
		['high', 'low'].index(params['option'])
		)
	)

def green_ninja_fun(params, dir):
	return "None"

def blue_ninja_fun(params, dir):
	return "None"

def red_ninja_fun(params, dir):
	return "None"

def toad_a_fun(params, dir):
	return None
	
def toad_b_fun(params, dir):
	return None
	
def bird_fun(params, dir):
	return None
	
def skeleton_fun(params, dir):
	return 0
	
def frogman_fun(params, dir):
	return params['spawn']
	
def monk_fun(params, dir):
	return 0

def rolling_fun(params, dir):
	return 0

param_fun = [
	musashi_fun, punk_fun, shooter_fun, pink_guardian_fun, hostage_fun, knife_fun, spider_fun, None, 
	kenoh_fun, blue_bazooka_fun, green_bazooka_fun, green_guardian_fun, green_ninja_fun, blue_ninja_fun, red_ninja_fun, frogman_fun,
	toad_a_fun, toad_b_fun, bird_fun, skeleton_fun, monk_fun, rolling_fun
]


def get_objects_and_chunks(tmx, param_fun, params):
	triggered_list = ['green_ninja', 'blue_ninja', 'red_ninja', 'spider']

	w, h = tmx.get_size()

	i = 0
	triggers = []
	objects = []
	chunks = []
	
	i_chunk = 0
	i_object = 0

	for layer in tmx:
		if layer.name.startswith('chunk')\
		or layer.name.startswith('$'):
			print (layer.name)
			i0 = i_object
			
			l = make_list(layer, obj_name, left_to_right)
			
			objs = []
			trigger = []
			for obj, dir, x, y in l:
				if obj == 'cross':
					trigger = [(obj, dir, x, y)]
				else:
					print (params[i_object])
					floor = int(params[i_object].get('floor', '1'))
					objs += [(obj, floor, x, y, param_fun[obj_name.index(obj)](params[i_object], dir))]
					i_object += 1
			
			if trigger:
				triggers += trigger
			else:
				triggers += l
				
			objects += objs
			chunks += [list(range(i0, i_object))]
			i_chunk += 1
				
	return triggers, objects, chunks

# ===================================================


def zip_maps(l):
	temp = l[0]
	h = len(temp)
	w = len(temp[0])
	res = [[[] for _ in range(w)] for _ in range(h)]
	for y in range(h):
		for x in range(w):
			res[y][x] = [l_[y][x] for l_ in l]
	return res

def encode_map(m, w, h):
	smap1 = [[tuple([tuple(z) for z in m[y][x]]) for x in range(w)] for y in range(h)]
	
	states = sorted(list(set([z for line in smap1 for z in line])))
	
	code_to_raw = states
	raw_to_code = {k: states.index(k) for k in states}
	res = [[raw_to_code[smap1[y][x]] for x in range(w)] for y in range(h)]
	
	return raw_to_code, code_to_raw, res

def new_map(w, h):
	return [[[] for _ in range(w)] for _ in range(h)]
	
def clamp(x, a, b):
	return max(min(x, b), a)

# =======================================================
	
def objects_ressources(objects, w, h, debug_surf = None):
	# left, right, top, bottom = edge_offsets
	
	left_map = new_map(w, h)
	right_map = new_map(w, h)
	top_map = new_map(w, h)
	bottom_map = new_map(w, h)
	
	# computing init chunk
	init_ = []
	print (objects)
	_, _, musashi_x, musashi_y = objects[0]
	x0 = musashi_x + d_left
	if x0 < 0:
		x0, x1 = 0, 21
	else:
		x1 = musashi_x + d_right
		if x1 >= w:
			x0, x1 = w - 21, w - 1
	
	y0 = musashi_y + d_top
	if y0 < 0:
		y0, y1 = 0, 16
	else:
		y1 = musashi_y + d_bottom
		if y1 >= h:
			y0, y1 = h - 16, h - 1
	
	i = 0
	for (_, _, x, y) in objects:
		if x0 <= x <= x1 and y0 <= y <= y1:
			init_ += [i]
		i += 1

	# regular chunks
	i = 1
	for (t, dir, x, y) in objects[1:]:
		process_left, process_right = True, True
		if t.startswith('cross'):
			x1 = x2 = x
		elif t in monodirectional_objects and dir == 'left':
			# print (t, dir, x, y)
			x1 = x2 = clamp(x + d_left, 0, w - 1)
			# process_right = False
		elif t in monodirectional_objects and dir == 'right':
			# print (t, dir, x, y)
			x1 = x2 = clamp(x + d_right, 0, w - 1)
			# process_left = False
		else:
			x1, x2 = clamp(x + d_left, 0, w - 1), clamp(x + d_right, 0, w - 1)
		y1 = clamp(y + d_top, 0, h - 1)
		y2 = clamp(y + d_bottom, 0, h - 1)

		# print ('update_map: %d, %d, %d, %d, %d, %d, %d, %d' % (x_, y_, dx, dy, tx, ty, w, h))
		for y_ in range(y1, y2 + 1):
			if process_left:
				left_map[y_][x1] += [i]
			if process_right:
				right_map[y_][x2] += [i]
		
		for x_ in range(x1, x2 + 1):
			top_map[y1][x_] += [i]
			bottom_map[y2][x_] += [i]
		i += 1
	
	raw_map = zip_maps([left_map, right_map, top_map, bottom_map])
		
	raw_to_code, code_to_raw, code_map = encode_map(raw_map, w, h)
	
	if debug_surf:
		pygame.image.save(map_to_surf(debug_surf, code_map), 'object_map.png')
	
	left_, right_, top_, bottom_ = zip(*code_to_raw)
		
	return code_map, left_, right_, top_, bottom_, init_

# =======================================================

def make_table(listoflists):
	header_sz = len(listoflists)
	header = []
	data = []
	matches = {}
	for t in listoflists:
		if t not in matches:
			matches[t] = header_sz + len(data)
			data += list(t) + [0xFF]
		header += [matches[t]]
	
	return header + data

# =======================================================

def map_to_surf(bg, m):
	pal = [pygame.Color(c) for c in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'gray', 'orange', 'pink', 'brown', 'turquoise']]
	
	h = len(m)
	w = len(m[0])
	
	for y in range(h):
		for x in range(w):
			t = m[y][x]
			if t:
				pygame.draw.rect(bg, pal[t % len(pal)], (x * 16, y * 16, 16, 16))
	return bg

# ========================================================

offsets = {\
	'musashi': (16, 15),
	'punk': (16, 15),
	'shooter': (16, 15), 
	'pink_guardian': (16, 15), 
	'hostage': (10, 15), 
	'knife': (16, 15), 
	'spider': (15, 15), 
	'blue_bazooka': (24, 15), 
	'green_bazooka': (24, 15), 
	'green_guardian': (16, 15), 
	'green_ninja': (16, 15), 
	'blue_ninja': (16, 15), 
	'red_ninja': (16, 15), 
	'frogman': (16, 41),
	'toad_a': (16, 15), 
	'toad_b': (16, 15), 
	'bird': (16, 15), 
	'skeleton': (16, 15), 
	'monk': (16, 15), 
	'rolling': (16, 15),
	'kenoh' : (32, 15)
}

def fmt_object(obj):
	n, f, x, y, param = obj
	dx, dy = offsets[n]
	return '[%s, %d, %d, %d, %s]' % (n, f, x * 16 + dx, y * 16 + dy, param)

def fmt_chunk(c):
	return str(c)

def fmt_map_row(r):
	return ', '.join(['0x%02X' % x for x in r])

def fmt_transition(t):
	return str(list(t))

	
def generate_objects_ressources(tmx, params):
	print (tmx.get_layer_by_name('layer a'))
	bg = tmx.get_layer_by_name('layer a').to_surface()
	
	triggers, objects_list, chunks = get_objects_and_chunks(tmx, param_fun, params)
	
	res = ''
	
	res += 'objects = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_object(o) for o in objects_list]))
	
	object_names = list(set([obj[0] for obj in objects_list]))
	
	res += 'objects_chunks = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_chunk(c) for c in chunks]))
	
	width, height = tmx.get_size()
	
	map_, left, right, top, bottom, init_ = objects_ressources(triggers, width, height, debug_surf = bg)	

	res += 'objects_map = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_map_row(r) for r in map_]))
	
	res += 'init_chunk = %s\n\n' % init_
	
	res += 'objects_from_left = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_transition(t) for t in left]))
	
	res += 'objects_from_right = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_transition(t) for t in right]))
	
	res += 'objects_from_top = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_transition(t) for t in top]))
	
	res += 'objects_from_bottom = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_transition(t) for t in bottom]))

	header = '\n'.join(['from chars import %s' % o for o in object_names])
	return header, res

# ========================================================

if __name__ == '__main__':
	base_dir = 'C:/Users/fterr/Documents/hack/shinobi/maps/3-2'
	params = read_param_file('%s/objects.txt' % base_dir)

	tmx = load_tmx('%s/3-2.tmx' % base_dir)

	res = generate_objects_ressources(tmx, params)

	with open('output.py', 'w') as f:
		f.write(res)
