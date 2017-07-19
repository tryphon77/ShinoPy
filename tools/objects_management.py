import sys
sys.path.append('../../pygato')

import pygame

from map import *
from tmx import *

RESPAWNABLE = 2

def rainbow(steps):
	steps = [255*k // steps for k in range(1, steps)]
	
	print (steps)
	red_yellow = [pygame.Color(255, k, 0, 255) for k in steps]
	yellow_green = [pygame.Color(255 - k, 255, 0, 255) for k in steps]
	green_cyan = [pygame.Color(0, 255, k, 255) for k in steps]
	cyan_blue = [pygame.Color(0, 255 - k, 255, 255) for k in steps]
	blue_magenta = [pygame.Color(k, 0, 255, 255) for k in steps]
	magenta_red = [pygame.Color(255, 0, 255 - k, 255) for k in steps]

	return [pygame.Color('red')] + red_yellow + [pygame.Color('yellow')] + yellow_green+ [pygame.Color('green')] + green_cyan+ [pygame.Color('cyan')] + cyan_blue + [pygame.Color('blue')] + blue_magenta + [pygame.Color('magenta')] + magenta_red
	
hostages = [
    [RESPAWNABLE, 400, 128, 'hostage_states.init_object', 1, 400, 239, None],
    [RESPAWNABLE, 1680, 128, 'hostage_states.init_object', 2, 1680, 127, None]	
]

objects = [
    [RESPAWNABLE, 400, 128, 'knife_states.init_object', 1, 64, 239, None],
    [RESPAWNABLE, 400, 128, 'punk_states.init_object', 1, 400, 239, hostages[0]],
	hostages[0],
    [RESPAWNABLE, 496, 128, 'shooter_states.init_object', 1, 496, 239, None],
    [RESPAWNABLE, 592, 128, 'sword_states.init_object', 2, 592, 127, None],
    [RESPAWNABLE, 656, 128, 'punk_states.init_object', 1, 656, 239, None],
    [RESPAWNABLE, 720, 128, 'punk_states.init_object', 2, 720, 127, None],
    [RESPAWNABLE, 752, 128, 'shooter_states.init_object', 1, 752, 239, None],
    [RESPAWNABLE, 784, 128, 'punk_states.init_object', 1, 784, 239, None],
    [RESPAWNABLE, 912, 128, 'shooter_states.init_object', 1, 912, 239, None],
    [RESPAWNABLE, 944, 128, 'punk_states.init_object', 2, 944, 127, None],
    [RESPAWNABLE, 1056, 128, 'punk_states.init_object', 2, 1056, 127, None],
    [RESPAWNABLE, 1216, 128, 'shooter_states.init_object', 1, 1216, 239, None],
    [RESPAWNABLE, 1296, 128, 'knife_states.init_object', 1, 1296, 239, None],
    [RESPAWNABLE, 1312, 128, 'knife_states.init_object', 1, 1312, 239, None],
    [RESPAWNABLE, 1328, 128, 'knife_states.init_object', 1, 1328, 239, None],
    [RESPAWNABLE, 1456, 128, 'shooter_states.init_object', 1, 1456, 207, None],
    [RESPAWNABLE, 1504, 128, 'shooter_states.init_object', 2, 1504, 127, None],
    [RESPAWNABLE, 1520, 128, 'shooter_states.init_object', 1, 1520, 239, None],
    [RESPAWNABLE, 1680, 128, 'sword_states.init_object', 2, 1680, 127, None],
    hostages[1], 
	[RESPAWNABLE, 1744, 128, 'punk_states.init_object', 1, 1744, 239, None],
    [RESPAWNABLE, 1872, 128, 'knife_states.init_object', 2, 1872, 127, None],
    [RESPAWNABLE, 1888, 128, 'knife_states.init_object', 1, 1888, 239, None],
    [RESPAWNABLE, 1920, 128, 'knife_states.init_object', 1, 1920, 239, None],
    [RESPAWNABLE, 1952, 128, 'shooter_states.init_object', 1, 1952, 239, None],
    [RESPAWNABLE, 1984, 128, 'knife_states.init_object', 1, 1984, 239, None]
]

width = 2048
height = 256

tw, th = width >> 4, height >> 4


blank = [-1]
res = [[set() for _ in range(tw)] for _ in range(th)]

print (len(res))
print (len(res[0]))
# res = pygame.Surface((width, height))
# res.fill(pygame.Color('white'))

for obj_id, obj in enumerate(objects):
	_, _, _, _, _, x, y, _ = obj
	
	x = x >> 4
	y = y >> 4
	
	delta = 16
	x0 = max(x - delta, 0)
	y0 = max(y - delta, 0)
	x1 = min(x + delta, tw - 1)
	y1 = min(y + delta, th - 1)

	print (obj_id, x0, y0, x1, y1) 
	for j in range(y0, y1 + 1):
		for i in range(x0, x1 + 1):
			# print(i, j, res[0][0])
			res[j][i].add(obj_id)
	# exit()

areas = [[-1 for _ in range(tw)] for _ in range(th)]

res_set = []
for j in range(0, th):
	for i in range(0, tw):
		if res[j][i] in res_set:
			areas[j][i] = res_set.index(res[j][i])
		else:
			areas[j][i] = len(res_set)
			res_set += [res[j][i]]

print(len(res_set))
print ('\n'.join([str(l) for l in res]))
print (areas)
# print (res[0][0])

colors = rainbow(10)

surf = pygame.Surface((tw, th))
surf.fill(pygame.Color('white'))

for i in range(0, tw):
	for j in range(0, th):
		c = areas[j][i] + 1
		if c > 0:
			surf.set_at((i, j), colors[c])
		
pygame.image.save(surf, 'map_objects.png')

