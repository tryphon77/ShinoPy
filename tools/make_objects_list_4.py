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
	# print ('[make_list]')
	res = []
	w, h = layer.get_size()
	for (x, y) in order(w, h):
		cell = layer[y][x]
		# if (90 <= x < 100) and (20 <= y < 30):
			# print ((x, y, cell))
		if cell is not None:
			t = cell.id_
			obj = obj_name[t]
			print ('\t%s: %d, %d' % (obj, x, y))
			if cell.hflip:
				dir = 'right'
			else:
				dir = 'left'
			res += [(obj_name[t], dir, x, y)]
	# print ('[/make_list]')
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

def musashi_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def punk_fun(self, params):
	self.update({
		'is_monodir': True,
		'print': lambda self_: 'None'
	})
	
def shooter_fun(self, params):
	self.update({
		'is_monodir': True,
		'option': params.get('option', 'standing'),
		'print': lambda self_: '(%s)' % (['standing', 'sitting', 'lying'].index(self_['option']))
	})

def pink_guardian_fun(self, params):
	self.update({
		'hostage': params['hostage'],
		'print': lambda self_: '(%s)' % self_['hostage']
	})

def hostage_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def knife_fun(self, params):
	self.update({
		'is_monodir': True,
		'print': lambda self_: 'None'
	})

def spider_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def kenoh_fun(self, params):
	return "None"

def green_bazooka_fun(self, params):
	self.update({
		'is_monodir': True,
		'mobile': params.get('mobile', 'True'),
		'print': lambda self_: '(%s)' % self_['mobile']
	})

def blue_bazooka_fun(self, params):
	self.update({
		'is_monodir': True,
		'range': params.get('range', 0),
		'print': lambda self_: '(%s)' % self_['range']
	})

def green_guardian_fun(self, params):
	self.update({
		'range': params.get('range', '0'),
		'nervosity': params.get('nervosity', '5'),
		'hostage': params.get('hostage', '0'),
		'option': params.get('option', 'high'),
		'print': lambda self_: '(%s, %s, %s, %s)' % (self_['range'], self_['nervosity'], self_['hostage'], ['high', 'low'].index(self_['option']))
	})

def green_ninja_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def blue_ninja_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def red_ninja_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def toad_a_fun(self, params):
	self.update({
		'is_monodir': True,
		'friend': params.get('friend', None),
		'print': lambda self_: '(%s)' % self_['friend']
	})
	
def toad_b_fun(self, params):
	self.update({
		'is_monodir': True,
		'friend': params.get('friend', None),
		'print': lambda self_: '(%s)' % self_['friend']
	})
	
def bird_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})
	
def skeleton_fun(self, params):
	self.update({
		'is_monodir': True, # was False ?
		'range': params.get('range', 128),
		'shoots': params.get('shoots', 4),
		'print': lambda self_: '(%s, %s)' % (self_['range'], self_['shoots'])
	})
	
def frogman_fun(self, params):
	self.update({
		'spawn': params.get('spawn', 0),
		'print': lambda self_: '(%s)' % self_['spawn']
	})
	
def monk_fun(self, params):
	self.update({
		'print': lambda self_: 'None'
	})

def rolling_fun(self, params):
	orientation = params.get('orientation', '.')
	vector = {\
		'.': "0, 0",
		'W': "-6, 0",
		'SW': "-4.25, 4.25",
		'SSW': "-3, 5",
		'S': "0, 6",
		'SE': "4.25, 4.25",
		'SSE': '3, 5',
		'E': "6, 0"
	}[orientation]
	
	if 'W' in orientation:
		dir = 'left'
	else:
		dir = 'right'
		
	self.update({
		'is_monodir': True,
		'dir': dir,
		'vector': vector,
		'delay': params.get('delay', '0'),
		'print': lambda self_: '(%s, %s)' % (self_['vector'], self_['delay'])
	})

param_fun = {
	'musashi': musashi_fun, 
	'punk': punk_fun, 
	'shooter': shooter_fun, 
	'pink_guardian': pink_guardian_fun, 
	'hostage': hostage_fun, 
	'knife': knife_fun, 
	'spider': spider_fun, 
	'blue_bazooka': blue_bazooka_fun, 
	'green_bazooka': green_bazooka_fun,
	'green_guardian': green_guardian_fun, 
	'green_ninja': green_ninja_fun, 
	'blue_ninja': blue_ninja_fun, 
	'red_ninja': red_ninja_fun, 
	'frogman': frogman_fun,
	'toad_a': toad_a_fun, 
	'toad_b': toad_b_fun, 
	'bird': bird_fun, 
	'skeleton': skeleton_fun, 
	'monk': monk_fun, 
	'rolling': rolling_fun
}

bounding_boxes = {
	'musashi': (-16, -64, 32, 63),
	'punk': (-16, -64, 32, 63),
	'shooter': (-16, -64, 32, 63), 
	'pink_guardian': (-16, -64, 32, 63), 
	'hostage': (-16, -64, 32, 63), 
	'knife': (-16, -64, 32, 63), 
	'spider': (-16, -64, 32, 63), 
	'blue_bazooka': (-16, -64, 32, 63), 
	'green_bazooka': (-16, -64, 32, 63), 
	'green_guardian': (-16, -64, 32, 63), 
	'green_ninja': (-16, -64, 32, 63), 
	'blue_ninja': (-16, -64, 32, 63), 
	'red_ninja': (-16, -64, 32, 63), 
	'frogman': (-16, -64, 32, 63),
	'toad_a': (-16, -64, 32, 63), 
	'toad_b': (-16, -64, 32, 63), 
	'bird': (-16, -64, 32, 63), 
	'skeleton': (-16, -64, 32, 63), 
	'monk': (-16, -64, 32, 63), 
	'rolling': (-16, -64, 32, 63),
	'kenoh' : (-16, -64, 32, 63)
}

def get_bounding_box(obj, dir, px, py):
	x, y, w, h = bounding_boxes[obj]
	if dir == 'left':
		return (px + x, px + x + w, py + y, py + y + h)
	else:
		return (px - x - w, px - x, py + y, py + y + h)
		
def get_view(rect, focus, map_width, map_height):
	l, r, t, b = rect
		
	if focus:
		xf, yf = focus
		x0 = max(0, l - xf)
		x1 = min(r - xf, map_width * 16 - 320)
	else:
		# x0 = max(0, l - 320)
		# x1 = min(r, map_width * 16 - 320)
		x0 = l - 320
		x1 = r
	
	# if x0 < 0:
		# x0 = 0
	# if x1 >= map_width * 16:
		# x1 = map_width * 16 - 1

	if focus:
		y0 = max(t - yf, 0)
		y1 = min(y0 + 224, map_height * 16 - 224)
	else:
		# y0 = 0 
		# y1 = map_height*16 - 1 
		y0 = max(0, t - 224)
		y1 = min(b, map_height * 16 - 1)
	# if y0 < 0:
		# y0 = 0
	# if y1 >= map_height * 16:
		# y1 = map_height * 16- 1
	
	tx0 = max(x0 // 16, 0)
	tx1 = min(x1 // 16 + 1, map_width - 20)
	ty0 = max(y0 // 16, 0)
	ty1 = min(y1 // 16, map_height - 1)
	
	return (tx0, tx1, ty0, ty1)
		
def get_objects_in_layer(layer, params, i_object, collmap):
	print (layer.name)
	
	l = make_list(layer, obj_name, left_to_right)
	
	objs = []

	trigger = None
	for obj, dir, x, y in l:
		print ('obj: %s, %s, %d, %d i_object = %d' % (obj, dir, x, y, i_object)) 
		if obj == 'cross':
			trigger = (x, y)
			print ('trigger: %s' % str(trigger))

	for obj, dir, x, y in l:
		print ('obj: %s, %s, %d, %d i_object = %d trigger = %s' % (obj, dir, x, y, i_object, trigger)) 
		if obj != 'cross':
			# print (params[i_object])
			
			floor = int(params[i_object].get('floor', '1'))
			obj_type = obj_name.index(obj)

			if obj == 'frogman':
				hx, hy = x*16 + 8, y*16 + 41
			else:
				hx, hy = x*16 + 8, y*16 + 15

			off_x, off_y = eval(params[i_object].get('offset', '(0, 0)'))
			hx += off_x
			hy += off_y

			obj_bounding_box = get_bounding_box(obj, dir, hx, hy)

			if collmap[y][x] & 8:
				hy -= 8
			current_object = {
				'name': obj,
				'id_': i_object,
				'type': obj_type,
				'floor': floor, 
				'pos': (x, y),
				'hotspot': (hx, hy),
				'dir': dir,
				'is_monodir': False,
				'bounding_box': obj_bounding_box
			}
			
			param_fun[obj](current_object, params[i_object])
			i_object += 1
		
			if trigger:
				print ('triggered')
				x_, y_ = trigger
				trig_x, trig_y = x_ * 16, y_ * 16
				x0_, x1_, y0_, y1_ = get_view((trig_x, trig_x + 16, trig_y - 128, trig_y + 16), (128, 120), layer.width, layer.height)
				current_object['view'] = (x0_, x0_, y0_, y1_)
				current_object['is_triggered'] = True
			else:
				current_object['view'] = get_view(current_object['bounding_box'], None, layer.width, layer.height)
				current_object['is_triggered'] = False

			objs += [current_object]
			
		
			print ('current_object: %s' % current_object)
	
	return objs

def get_objects(tmx, params, collmap):
	print ('get_objects')
	triggered_list = ['green_ninja', 'blue_ninja', 'red_ninja', 'spider']

	w, h = tmx.get_size()

	triggers = []
	objects = []
	chunks = []
	
	i_object = 0

	for layer in tmx:
		if layer.name.startswith('chunk')\
		or layer.name.startswith('$'):
			print ('==============')
			new_objects = get_objects_in_layer(layer, params, i_object, collmap)
			objects += new_objects
			i_object += len(new_objects)
			# chunks += [list(range(i0, i_object))]
			# i_chunk += 1

	# exit()
	for obj in objects:
		print(obj)
		print ('---------------------------------------')
	# exit()
	return objects

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

def get_chunks(l):
	# c = list(set([tuple(x) for x in l if x]))
	c = [()]
	for t in l:
		x = tuple(t)
		if x not in c:
			c += [x]
	
	return {i: c.index(i) for i in c}

def get_ressources(objects, w, h, debug_surf = None):
	# left, right, top, bottom = edge_offsets
	
	left_map = new_map(w, h)
	right_map = new_map(w, h)
	top_map = new_map(w, h)
	bottom_map = new_map(w, h)
	
	# /!\ DEBUG !!!!!!!!!!!!!!!!!!!!!!!!
	# print (objects)
	# objects = [o for o in objects if o['name'] in ['musashi', 'hostage']]
	# print ('***********************')
	# print (objects)
	# print ('***********************')
	
	# computing init chunk
	init_ = []
	
	hx, hy = objects[0]['hotspot']
	x0, y0 = max(0, (hx - 128) // 16 - 1), max(0, (hy - 120) // 16 - 1)
	x1, y1 = min(w, x0 + 21), min(h, y0 + 15)
	
	i = 0
	for obj in objects:
		x, y = obj['pos']
		if (not obj['is_monodir']\
		or obj['dir'] == 'left')\
		and (x0 <= x <= x1 and y0 <= y <= y1):
			init_ += [i]
		i += 1

	# regular chunks
	i = 1
	for obj in objects[1:]:
		l, r, t, b = obj['view']
		is_monodir = obj['is_monodir']
		if is_monodir:
			if obj['dir'] == 'left':
				left = right = l
			else:
				left = right = r
		else:
			left = l
			right = r

		top = t
		bottom = b
	
		print ('(%02d) %s: %d, %d' % (obj['id_'], obj['name'], left, right))
		# print ('update_map: %d, %d, %d, %d, %d, %d, %d, %d' % (x_, y_, dx, dy, tx, ty, w, h))
		for y_ in range(top, bottom + 1):
			left_map[y_][left] += [i]
			right_map[y_][right] += [i]
		
		for x_ in range(left, right + 1):
			top_map[top][x_] += [i]
			bottom_map[bottom][x_] += [i]
		i += 1
	
	raw_map = zip_maps([left_map, right_map, top_map, bottom_map])
		
	raw_to_code, code_to_raw, code_map = encode_map(raw_map, w, h)
	
	if debug_surf:
		pygame.image.save(map_to_surf(debug_surf, code_map), 'object_map.png')
	
	left_, right_, top_, bottom_ = zip(*code_to_raw)
		
	print (tuple([tuple(init_)]))
	print (left_)
	chunks = get_chunks(tuple([tuple(init_)]) + left_ + right_ + top_ + bottom_)
	
	return {
		'map': code_map, 
		'left': left_, 
		'right': right_, 
		'top': top_, 
		'bottom': bottom_, 
		'chunks': chunks
	}

# =======================================================

def get_ressources_full_rects(objects, w, h, debug_surf = None):
	
	# /!\ DEBUG !!!!!!!!!!!!!!!!!!!!!!!!
	# print (objects)
	# objects = [o for o in objects if o['name'] in ['musashi', 'hostage']]
	# print ('***********************')
	# print (objects)
	# print ('***********************')
	
	# computing init chunk
	init_ = []
	
	hx, hy = objects[0]['hotspot']
	x0, y0 = max(0, (hx - 128) // 16 - 1), max(0, (hy - 120) // 16 - 1)
	x1, y1 = min(w, x0 + 21), min(h, y0 + 15)
	
	i = 0
	print ('init_chunk:')
	for obj in objects:
		x, y = obj['pos']
		if not obj['is_triggered'] and\
		(not obj['is_monodir']\
		or obj['dir'] == 'left')\
		and (x0 <= x <= x1 and y0 <= y <= y1):
			print (obj)
			init_ += [i]
		i += 1
	
	# regular chunks

	# only one map	
	map_ = new_map(w, h)

	i = 1
	for obj in objects[1:]:
		l, r, t, b = obj['view']
		is_monodir = obj['is_monodir']
		if is_monodir:
			if obj['dir'] == 'left':
				left = right = l
			else:
				left = right = r
		else:
			left = l
			right = r

		top = t
		bottom = b
	
		print ('(%02d) %s: left = %d top = %d right = %d bottom = %d' % (obj['id_'], obj['name'], left, top, right, bottom))
		# print ('update_map: %d, %d, %d, %d, %d, %d, %d, %d' % (x_, y_, dx, dy, tx, ty, w, h))
		for y_ in range(top, bottom + 1):
			for x_ in range(left, right + 1):
				map_[y_][x_] += [i]
		i += 1
	# exit()
	
	# ===============================================
	code_to_raw = [(), tuple(init_)]
	code_map = []
	for j in range(h):
		code_line = []
		for i in range(w):
			cell = tuple(map_[j][i])
			if cell not in code_to_raw:
				code_to_raw += [cell]
			code_line += [code_to_raw.index(cell)]
		code_map += [code_line]
	raw_to_code = {x: i for i, x in enumerate(code_to_raw)}
	
	# raw_map = zip_maps([map_])
	# print (raw_map)
	
	# raw_to_code, code_to_raw, code_map = encode_map(raw_map, w, h)
	
	if debug_surf:
		pygame.image.save(map_to_surf(debug_surf, code_map), 'object_map.png')
			
	print ('init_:', init_)
	print ('code_to_raw:', code_to_raw)
		
	print ('code_map:')
	print (code_map)
	
	return {
		'map': code_map, 
		'chunks': raw_to_code
	}

# =====================================================

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

def fmt_object(obj):
	print (obj)
	x, y = obj['hotspot']
	return '[%s, %d, %d, %d, %s, %s]' % (
		obj['name'], 
		obj['floor'], 
		x, y,
		obj['dir'] == 'left',
		obj['print'](obj)
	)

def fmt_chunk(c):
	return str(list(c))

def fmt_map_row(r):
	return ', '.join(['0x%02X' % x for x in r])

def fmt_transition(t, chunks):
	return str(chunks[tuple(t_ for t_ in t)])

	
def generate_objects_ressources_edges(tmx, objects_path, collmap):
	# tmx = load_tmx(tmx_path)
	params = read_param_file(objects_path)
	width, height = tmx.get_size()

	bg = tmx.get_layer_by_name('layer a').to_surface()
	
	objects = get_objects(tmx, params, collmap)
	
	ressources = get_ressources(objects, width, height, debug_surf = bg)	
		
	res = ''
	
	res += 'objects = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_object(o) for o in objects]))
	
	object_names = list(set([obj['name'] for obj in objects]))
	
	res += 'objects_chunks = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_chunk(c) for c in ressources['chunks']]))
		
	res += 'objects_map = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_map_row(r) for r in ressources['map']]))
	
	# res += 'init_chunk = %s\n\n' % ressources['init_chunk']
		
	for d in ['left', 'right', 'top', 'bottom']:
		res += 'objects_from_%s = [\n%s\n]\n\n' % (d, ',\n'.join(['\t%s' % fmt_transition(t, ressources['chunks']) for t in ressources[d]]))
	
	header = '\n'.join(['from chars import %s' % o for o in object_names])
	
	print (header)
	print ('****************')
	print (res)
	return header, res

# ========================================================

def generate_objects_ressources_full_rects(tmx, objects_path, collmap):

	def fmt_chunk(chunk):
		return str(list(chunk))
		
	# tmx = load_tmx(tmx_path)
	params = read_param_file(objects_path)
	width, height = tmx.get_size()

	bg = tmx.get_layer_by_name('layer a').to_surface()
	
	objects = get_objects(tmx, params, collmap)
		
	ressources = get_ressources_full_rects(objects, width, height, debug_surf = bg)	
	
	res = ''
	
	res += 'objects = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_object(o) for o in objects]))
	
	object_names = list(set([obj['name'] for obj in objects]))
	
	res += 'objects_chunks = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_chunk(c) for c in ressources['chunks']]))
		
	res += 'objects_map = [\n%s\n]\n\n' % (',\n'.join(['\t%s' % fmt_map_row(r) for r in ressources['map']]))
	
	# res += 'init_chunk = %s\n\n' % ressources['init_chunk']
	
	header = '\n'.join(['from chars import %s' % o for o in object_names])
	
	print (header)
	print ('****************')
	print (res)
	return header, res

# ========================================================

generate_objects_ressources = generate_objects_ressources_full_rects

if __name__ == '__main__':
	base_dir = 'C:/Users/fterr/Documents/hack/shinobi/maps/3-2'

	objects_path = '%s/objects.txt' % base_dir
	tmx_path = '%s/3-2.tmx' % base_dir
	res = generate_objects_ressources(tmx_path, objects_path)

	with open('output.py', 'w') as f:
		f.write(res)
