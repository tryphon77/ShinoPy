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

def get_attributes(layer, coll_layer, n_tiles):
	res = [0] * n_tiles
	for y, row in enumerate(coll_layer.map):
		for x, cell in enumerate(row):
			if cell:
				tile = layer.map[y][x]
				if 1 <= cell.id_ < 8:
					res[tile.id_] = 1
				elif 16 <= cell.id_ < 48:
					print (cell.id_, x, y, tile)
					res[tile.id_] = 2
	
	return res


def get_floors_map(map_):
	def cvt(t):
		print (t)
		if t is None:
			return 0
		elif 1 < t.id_ < 8:
			return t.id_
		elif 16 <= t.id_ < 24:
			return t.id_ & 7
		else:
			return 0

	w, h = map_.get_size()

	for x in range(10):
		floors = []
		f = 1
		y = h - 1
		while y > 0:
			tile = cvt(map_[y][x])
			tile_top = cvt(map_[y - 1][x])

			if 0 < tile < 8 and tile_top != tile and  tile == f:
				floors += [y]
				f += 1
			else:
				y -= 1
			
		print ('column: %d' % x)
		print (floors)
	
	exit()
	
def get_collmap(map_):
	def cvt(x):
		if x:
			if x.id_ < 8:
				return x.id_
			elif 16 < x.id_ < 24:
				return 8 + (x.id_ & 7)
		return 0

	impulsion = [1, 1, 2, 3, 4, 5, 5, 5, 6, 6, 7, 7, 7]
	res = [[cvt(x) for x in row] for row in map_]
	w, h = map_.get_size()
	ascending_map = [[0] * w for _ in range(h)]

	def get_floors(x):
		w, h = map_.get_size()
		floors = []
		f = 1
		y = h - 1
		while y > 0:
			tile = res[y][x] & 7
			tile_top = res[y - 1][x] & 7
			if 0 < tile < 8 and tile_top != tile and  tile == f:
				floors += [y]
				f += 1
			else:
				y -= 1
		return floors

	def process_ascending(x, y0, floor):
		found = False
		for y in range(y0 - 1, -1, -1):
			tile = map_[y][x]
			if tile and 8 < tile.id_ < 16:
				f = tile.id_ - 8
				if f == floor:
					found = True
					break
		
		if found:
			print ('(ascending) floor %d: from %d to %d' % (floor, y0, y))
			# for j in range(y0 - y):
			j = y0 - y - 1
			y_ = y + j + 1

			if (res[y_][x] & 7 == floor) \
			or ((x > 0) and (res[y_][x - 1] & 7 == floor)) \
			or ((x < w) and (res[y_][x + 1] & 7 == floor)):
				if x > 0:
					res[y + j + 1][x - 1] |= (j << 4)
					ascending_map[y + j + 1][x - 1] = j
					res[y + j][x - 1] |= (j - 1) << 4
					ascending_map[y + j][x - 1] = j - 1

				res[y + j + 1][x] |= (j << 4)
				ascending_map[y + j + 1][x] = j
				res[y + j][x] |= (j - 1) << 4
				ascending_map[y + j][x] = j - 1

				if x < w:
					res[y + j + 1][x + 1] |= (j << 4)
					ascending_map[y + j + 1][x + 1] = j
					res[y + j][x + 1] |= (j - 1) << 4
					ascending_map[y + j][x + 1] = j - 1
		
		return y
			
	def process_descending(x, y0, floor):
		found = False
		for y in range(y0 - 1, -1, -1):
			tile = map_[y][x]
			if tile and 8 < tile.id_ < 16:
				f = tile.id_ - 8
				if f == floor - 1:
					found = True
					break
		
		if found:
			print ('(descending) floor %d: from %d to %d' % (floor, y0, y))
			for j in range(-1, y0 - y):
				res[y + j + 1][x] |= (max(j, 1) << 8)
		
		return y
				
	for x in range(w):
		print ('column: %d' % x)
		floors_y = get_floors(x)
		print ('%d : %s' % (x, floors_y))
		
		floor = 1
		for floor_y in floors_y:
			print ('floor: %d (at %d)' % (floor, floor_y))
			process_ascending(x, floor_y, floor)
			process_descending(x, floor_y, floor)
			floor += 1

		if x == 28:
			print ('\n'.join(['%04X' % res[y][x] for y in range(h)]))
			exit()
	
	return res

	
	# =====================================================


if __name__ == '__main__':
	pass