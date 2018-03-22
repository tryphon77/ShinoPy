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
	
# ========================================================
# get_collmap

def get_jumps_table(map_):
	w, h = map_.get_size()
	jumps_table = []
	n_levels = 1
	for x in range(w):
		jumps = [None] * 8
		for y in range(h):
			t = map_[y][x]
			if t and 8 <= t.id_ < 16:
				j = t.id_ - 8
				jumps[j] = y
				n_levels = max(j + 1, n_levels)
	
		jumps_table += [jumps]
	return n_levels, jumps_table
	
	
	print ('nb of floors: %d' % n_levels)

	# debug
	# print ('jumps')
	# for x in range(w):
		# print ('%d : %s' % (x, jumps_table[x]))
	# exit()


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

	n_levels, jumps_table = get_jumps_table(map_)
		
	# floors = []
	# for x in range(w):
		# floors_x = [None]
		# for f in range(1, n_levels + 1):
			# for y in range(1, h):
				# if res[y][x] & 7 in [f, 7] and res[y - 1][x] & 7 not in [f, 7]:
					# floors_x += [y]
					# break
			# else:
				# floors_x += [None]
		
		# floors += [floors_x]

	# debug
	# print ('floors')
	# for x in range(w):
		# print ('%d : %s' % (x, floors[x]))

	
	# for x in range(w):
		# print ('x = %d' % x)
		# for f in range(1, n_levels):
			# print ('f = %d' % f)
			# jump_y = jumps_table[x][f]
			# if jump_y:
				# # hijump up
				# low_y = floors[x][f]
				# j = low_y - jump_y - 1
				# print ('jump = %d, low = %d, j = %d' % (jump_y, low_y, j))
				# res[low_y - 1][x] |= (j << 4)
				
				# for dx in [-2, -1, 1, 2]:
					# if 0 <= x + dx < w and jumps_table[x + dx][f]:
						# res[low_y - 1][x + dx] |= (j << 4)
				
				# # hijump down
				# print (f, floors[y])
				# high_y = floors[x][f + 1]
				# j = high_y - jump_y - 1
				# print ('jump = %d, high = %d, j = %d' % (jump_y, high_y, j))
				# res[high_y - 1][x] |= (j << 8)
				
				# for dx in [-2, -1, 1, 2]:
					# if 0 <= x + dx < w and jumps_table[x + dx][f]:
						# res[high_y - 1][x + dx] |= (j << 8)

		# if x == 29:
			# print ('\n'.join(['%04X' % res[y][x] for y in range(h)]))
			# exit()
		
	# for floor in range(1, 8):
		# for x in dead_cols[floor - 1]:
			# for y in range(h):
				# if (res[y][x] & 7 == floor)\
				# or (y < h - 1 and (res[y + 1][x] & 7 == floor)):
					# res[y][x] &= 0xFF0F
	
	# print (dead_cols)
	# print ('\n'.join(['%04X' % res[y][49] for y in range(h)]))
	# print ('==============')
	# print ('\n'.join(['%04X' % res[y][38] for y in range(h)]))
	# exit()
		
	return res
	
	# =====================================================


if __name__ == '__main__':
	pass