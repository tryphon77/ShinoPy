import pygame

# objects = [(1, 1), (62, 1), (1, 62), (62, 62)]
# width = height = 64
# objects = [(1, 1), (22, 1), (1, 22), (22, 22)]
# width = height = 24

def read_object_file(path):
	with open(path) as f:
		lines = f.readlines()
	
	res = []
	for line in lines:
		line = line.strip()
		if line:
			_, _, x, y = line.strip('[]').split(',')
			res += [(int(x) // 16, int(y) // 16)]
	return res
			

base_dir = 'C:/Users/fterr/Documents/hack/Shinobi/maps'


punk = shooter = guardian = knife = green_ninja = blue_ninja = red_ninja = None

# objects = [(x // 16, y // 16) for (_, _, x, y, _) in [
    # [punk, 1, 320, 239, None],
    # [punk, 1, 368, 239, None],
    # [shooter, 1, 592, 239, None],
    # [punk, 1, 608, 239, None],
    # [shooter, 2, 672, 127, None],
    # [punk, 1, 752, 239, None],
    # [punk, 2, 896, 127, None],
    # [punk, 1, 960, 239, None],
    # [shooter, 1, 1008, 239, None],
    # [punk, 1, 1024, 239, None],
    # [shooter, 1, 1168, 239, None],
    # [punk, 1, 1264, 239, None],
    # [punk, 1, 1280, 239, None],
    # [punk, 1, 1312, 239, None],
    # [punk, 2, 1440, 127, None],
	# [shooter, 1, 1456, 207, None],
    # [punk, 1, 1520, 239, None],
	# [shooter, 1, 1712, 239, None],
    # [shooter, 2, 1728, 127, None],
# ]]

# width = 128
# height = 16

objects = read_object_file('%s/2-2/objects.txt' % base_dir)
width = 64
height = 64
print (objects)

def pow_print(c):
	res = 0
	for x in c:
		res += (2**x)
	return '%02X' % res

def print_array(a, print_fun = lambda x: '%02X' % x):
	print('\n'.join([' '.join([print_fun(x) for x in row]) for row in a]))


def colorize(a, rect, col):
	x0, y0, x1, y1 = rect
	
	for x_ in range(x0, x1 + 1):
		for y_ in range(y0, y1 + 1):
			if col not in a[y_][x_]:
				a[y_][x_] += col


def get_opposite_vertex(a, x0, y0):
	x, y = x0, y0
	ref = a[y0][x0]
	
	while x < 64:
		if a[y][x] != ref:
			break
		x += 1
	x1 = x - 1
	
	while y < 64:
		if x0 > 0 and a[y][x0 - 1] == ref:
			break
		
		res = False
		for x in range(x0, x1 + 1):
			if a[y][x] != ref:
				res = True
				break
		
		if res:
			break
		
		y += 1
	
	y1 = y - 1
	return x1, y1

def find_diffs(l1, l2):
	res = []
	for x in l2:
		if x not in l1:
			res += [x]
	return res
	
def check_transitions(a, list_of_pos):
	l1 = a[s1[1]][s1[0]]
	l2 = a[s2[1]][s2[0]]
	
	res = []
	for x in l2:
		if x not in l1:
			res += [x]
	return res


visibility = [[[] for _ in range(width)] for _ in range(height)]


for i, pos in enumerate(objects):
	x, y = pos
	
	# if x <= 20:
		# x0 = 0
		# x1 = 20
	# elif x >= width - 21:
		# x0 = width - 21
		# x1 = width - 1
	# else:
	x0 = max(0, x - 10)
	x1 = min(x + 11, width - 1)
	
	# if y <= 14:
		# y0 = 0
		# y1 = 14
	# elif y >= height - 15:
		# y0 = height - 15
		# y1 = height - 1
	# else:
	y0 = max(0, y - 10) #y - 7) # ??????????
	y1 = min(y + 11, height - 1)
	
	colorize(visibility, (x0, y0, x1, y1), [i])

	
# print_array(visibility, pow_print)
# exit()

def get_regular_rects(visibility, w = 8, h = 8):
	blocks = []
	i = 0
	state_map = [[-1] * width for _ in range(height)]
	for y in range(0, height, h):
		for x in range(0, width, w):
			objs = set()
			for y_ in range(y, y + h):
				for x_ in range(x, x + w):
					state_map[y_][x_] = i
					objs.update(visibility[y_][x_])
			blocks += [{'id': i, 
						'rect': (x, y, 8, 8),
						'objects': sorted(list(objs))}]
			i += 1

	def get_objects(x, y):
		return blocks[state_map[y][x]]['objects']

	for state in blocks:
		id_ = state['id']
		objs = state['objects']
		x, y, w, h = state['rect']
		transitions = []
		if x > 0:
			dest_id = state_map[y][x - 1]
			dest_objs = blocks[dest_id]['objects']
			transitions += [(dest_id, find_diffs(objs, dest_objs))]
		else:
			transitions += [(-1, [])]
		
		if x + w < width:
			dest_id = state_map[y][x + w + 1]
			dest_objs = blocks[dest_id]['objects']
			transitions += [(dest_id, find_diffs(objs, dest_objs))]
		else:
			transitions += [(-1, [])]


		if y > 0:
			dest_id = state_map[y - 1][x]
			dest_objs = blocks[dest_id]['objects']
			transitions += [(dest_id, find_diffs(objs, dest_objs))]
		else:
			transitions += [(-1, [])]



		if y + h < height:
			dest_id = state_map[y + h + 1][x]
			dest_objs = blocks[dest_id]['objects']
			transitions += [(dest_id, find_diffs(objs, dest_objs))]
		else:
			transitions += [(-1, [])]

		state['transitions'] = transitions
	return blocks


states = get_regular_rects(visibility)

for state in states:
	res = ''
	trans = state['transitions']
	if trans[0][1]:
		res += 'left : %s\n' % str(trans[0])
	if trans[1][1]:
		res += 'right : %s\n' % str(trans[1])
	if trans[2][1]:
		res += 'up : %s\n' % str(trans[2])
	if trans[3][1]:
		res += 'down : %s\n' % str(trans[3])
	
	if res:
		print ('state %d : %s' % (state['id'], state['rect']))
		print ('objects: %s' % (state['objects']))
		print (res)
		print ('=====================================')
	
	
list_of_transitions = []

for state in states:
	list_of_transitions += [tuple(t[1]) for t in state['transitions']]

set_of_transitions = set()
set_of_transitions.update(list_of_transitions)

for t in set_of_transitions:
	print ('%s : %d' % (t, list_of_transitions.count(t)))

	
def get_objects_map():
	objects_refs = [[]]
	objects_map = []
	rows = []
	for y in range(height):
		row = []
		for x in range(width):
			objs = visibility[y][x]
			if objs not in objects_refs:
				objects_refs += [objs]
			row += [objects_refs.index(objs)]
		
		objects_map += [row]
		rows += ['\t' + (', '.join(['0x%02X' % k for k in row]))]
	
	map_surf = pygame.Surface((width, height))
	
	nb_colors = len(objects_refs)
	map_colors = [pygame.Color(0, 0, 0, 255) for _ in range(nb_colors)]
	for i in range(nb_colors):
		map_colors[i].hsva = ((360 * i) // nb_colors, 100, (100 * i) // nb_colors, 100)
	for y in range(height):
		for x in range(width):
			map_surf.set_at((x, y), map_colors[objects_map[y][x]])
	pygame.image.save(map_surf, 'object_map.png')
	
	print ('objects_map = [')
	print (',\n'.join(rows))
	print (']\n')
	
	obj_rows = []
	for objs in objects_refs:
		obj_rows += ['\t[' + (', '.join('%d' % (1 + k) for k in objs)) + ']']
	print ('objects_chunks = [')
	print (',\n'.join(obj_rows))
	print (']\n')
	
	def get_new_objects_ref(strip, dx, dy):
		x0, y0, x1, y1 = strip
		
		new_objects_refs = []
		for state_id in range(nb_colors):
			new_objs = objects_refs[state_id]
			# print ('state: %d, objects: %s' % (state_id, new_objs))
			new_objs_for_state = set()
			for y in range(height):
				for x in range(width):
					obj = objects_map[y][x]
					if x0 <= x <= x1 and y0 <= y <= y1 and obj == state_id:
						old_objs = objects_refs[objects_map[y + dy][x + dx]]
						for new_obj in new_objs:
							if new_obj not in old_objs:
								# print ('from %02X: %d' % (obj, new_obj))
								new_objs_for_state.add(new_obj)
			new_objects_refs += [sorted(list(new_objs_for_state))]
		
		return new_objects_refs

	def print_llist(name, l):
		obj_rows = []
		for objs in l:
			obj_rows += ['\t[' + (', '.join('%d' % (1 + k) for k in objs)) + ']']
		print ('%s = [' % name)
		print (',\n'.join(obj_rows))
		print (']\n')
	
	# look for new object from the left
	objects_from_left = get_new_objects_ref((1, 0, width - 1, height - 1), -1, 0)
	print_llist('objects_from_left', objects_from_left)
	
	# look for new object from the right
	objects_from_right = get_new_objects_ref((0, 0, width - 2, height - 1), 1, 0)
	print_llist('objects_from_right', objects_from_right)
	
	# look for new object from the top
	objects_from_top = get_new_objects_ref((0, 1, width - 1, height - 1), 0, -1)
	print_llist('objects_from_top', objects_from_top)

	# look for new object from the bottom
	objects_from_bottom = get_new_objects_ref((0, 0, width - 1, height - 2), 0, 1)
	print_llist('objects_from_bottom', objects_from_bottom)
	
	return
	
	neighbours = [set() for _ in range(len(objects_refs))]
	for y in range(height):
		for x in range(width):
			objs = visibility[y][x]
			k = objects_map[y][x]
			n = neighbours[k]
			
			if x > 0:
				n.add(objects_map[y][x - 1])
			if x < width - 1:
				n.add(objects_map[y][x + 1])
			if y > 0:
				n.add(objects_map[y - 1][x])
			if y < height - 1:
				n.add(objects_map[y + 1][x])

				
	objs_delta = []
	print ('new_objects_table = [')
	new_objects_table = []
	for src in neighbours:
		row = []
		for dst in neighbours:
			diff = sorted(dst.difference(src))
			if diff not in objs_delta:
				objs_delta += [diff]
			row += [objs_delta.index(diff)]
		new_objects_table += [row]
	
	print (',\n'.join(['\t' + str(x) for x in new_objects_table]))
	print (']\n')
	
	print ('new_objects_refs = [')
	print (',\n'.join(['\t' + str(x) for x in objs_delta]))
	print (']')
	
get_objects_map()
		
exit()

def get_optimal_rects():
	mask = [[0]* 64 for _ in range(64)]
	states = []
	states_array = [[0] * 64 for _ in range(64)]

	i = 0
	for y in range(64):
		for x in range(64):
			if not mask[y][x]:
				x1, y1 = get_opposite_vertex(visibility, x, y)
				states += [(x, y, x1, y1)]
				print ('rect: (%d, %d, %d, %d)' % (x, y, x1, y1))
				colorize(mask, (x, y, x1, y1), 1)
				colorize(states_array, (x, y, x1, y1), i)
				i += 1
				
				# print ('****')
				# print_array(mask)


	print ('=======')
	print (states)

	for i, state in enumerate(states):
		x0, y0, x1, y1 = state
		
		transitions = []
		
		if x0 > 0:
			transitions += check_transitions(visibility, zip([x0 - 1], range(y0, y1 + 1)))

			
			for y in range(y0, y1 + 1):
				dest = states_array[y0][x0 - 1]
				transitions += [(dest, find_diffs(visibility, state, states[dest]))]
		else:
			transitions += [(-1, [])]

		if x1 < 63:
			# transitions += check_transitions(visibility, state, zip([x0 + 1], range(y0, y1 + 1)))

			dest = states_array[y0][x1 + 1]
			transitions += [(dest, find_diffs(visibility, state, states[dest]))]
		else:
			transitions += [(-1, [])]
			
		if y0 > 0:
			# transitions += check_transitions(visibility, state, zip(range(x0, x1 + 1), [y0 - 1]))

			dest = states_array[y0 - 1][x0]
			transitions += [(dest, find_diffs(visibility, state, states[dest]))]
		else:
			transitions += [(-1, [])]

		if y1 < 63:
			# transitions += check_transitions(visibility, state, zip(range(x0, x1 + 1), [y0 = 1]))

			dest = states_array[y1 + 1][x0]
			transitions += [(dest, find_diffs(visibility, state, states[dest]))]
		else:
			transitions += [(-1, [])]
			
		for k, trans in transitions:
			print('%d->%d : %s' % (i, k, trans))
		print ('------------------')
	
