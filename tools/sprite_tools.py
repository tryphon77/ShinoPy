import sys
sys.path.append('..')
sys.path.append('C:/Users/fterr/Documents/workspace/MDTools')

import pygame
import numpy
import random
import itertools

from tools.psdreader import *
from tools.animsreader import load_animdefs
from map_tools import make_sheet

from tools.surface import *
from tools.colors import *
import tools.plugins.basic_splitter
import tools.plugins.group_splitter
import tools.plugins.row_splitter
import tools.plugins.best_splitter


def read_sheet(path):
	# psd = load_psd('%s/sheet.psd' % base_dir)
	psd = load_psd(path)

	res = []
	for i, layer in enumerate(psd.get_layers()):
		nm = layer.get_name()
		if nm.startswith('frame'):
			print (nm)
			nm, j_ = nm.split(' ')[:2]
			j = int(j_)
			res += [{
				'id': j,
				'surface': layer.get_surface()
			}]
	
	return res

def read_split_file(path):
	def read_rect(srect):
		return tuple([int(x) for x in srect.strip('()').split(',')])

	def read_rects(srects):
		srects = srects.strip(' []\r\n')
		if srects:
			return [read_rect(srect.strip()) for srect in srects.split(';')]
		else:
			return []
	
	splits = {}
	with open(path) as f:
		lines = f.readlines()

	for line in lines:
		if line.startswith('frame:'):
			f_id = int(line[6:])
		elif line.startswith('split:'):
			# print('split: %s' % read_rects(line[6:]))
			splits[f_id] = read_rects(line[6:])
	
	return splits

def get_patterns(surf):
	res = []
	w, h = surf.get_size()
	for x in range(0, w, 8):
		for y in range(0, h, 8):
			res += [surf.subsurface((x, y, 8, 8))]
	# print("%d patterns" % len(res))
	return res

def get_subsurface(surf, rect):
	x, y, w, h = rect
	sw, sh = surf.get_size()
	
	res = pygame.Surface((w, h), pygame.SRCALPHA)
	
	rx = ry = 0
	
	if x < 0:
		rx = -x
		w += x
		x = 0
	if x + w > sw:
		w = sw

	if y < 0:
		ry = -y
		h += y
		y = 0
	if y + h > sh:
		h = sh
	
	res.blit(surf, (rx, ry), (x, y, w, h))
	return res


def generate_splits(data):
	path = '%s/split.txt' % data['path']

	if os.path.exists(path):
		data['splits'] = read_split_file(path)
		return

	# generate splits if not presents

	splitters = [(tools.plugins.basic_splitter.splitter, []),
				 (tools.plugins.group_splitter.splitter, []),
				 (tools.plugins.row_splitter.splitter, [])]

	ennemy_palette = data['palette']

	splits = {}
	res = ''
	for i, frame in enumerate(data['frames']):
		print ('splitting frame #%d' % i)
		j = frame['id']

		res += 'frame: %d\n' % j
		surf = frame['surface']
		frame = Surface4bpp.from_pygame_surface(surf, palette = ennemy_palette)
		
		frame.save('%s/debug/%02d.png' % (data['path'], i), palette = ennemy_palette)

		rects = tools.plugins.best_splitter.splitter(frame, splitters)
		res += 'split: [%s]\n\n' % (' ; '.join([str(x) for x in rects]))
		
		splits[j] = rects
		

	with open(path, 'w') as f:
		f.write(res)
	data['splits'] = splits

def print_frames_table(data):
	# generating frames_table and patterns_blocks
	if 'splits' not in data:
		generate_splits(data)
		
	splits = data['splits']
	
	hotspot_x, hotspot_y = data['hotspot']
	
	res = 'frames_table = '
	dp = 0
	res_ = []
	ptrn_blocks = []
	for i in splits.keys():
		# print 'frame:', i
		split = splits[i]
		# print split
		res__ = []
		dp0 = dp
		for j, (x, y, w, h) in enumerate(split):
			x_ = x - hotspot_x
			y_ = y - hotspot_y
			bx_ = -x_ - w
			sw, sh = w // 8, h // 8
			flags = ((sw - 1) << 2) + sh - 1
			res__ += ['\t\t[%d, %d, %d, 0x%04X, 0x%02X]' % (x_, bx_, y_, flags, dp)]
			dp += sw * sh
		res_ += ['\t[\t\t# frame %d\n%s\n\t]' % (i, ',\n'.join(res__))]
		
		ptrn_blocks += [(dp0, dp - dp0)]

	res += '[\n%s\n]\n' % ',\n'.join(res_)

	print(res)

	print('patterns_blocks = [\n%s\n]\n' % ',\n'.join(['\t[0x%04X, 0x%04X]' % (p, l)\
													   for (p, l) in ptrn_blocks]))

	
def print_animations_table(data):
	# generate anims

	anims = data['animdefs']
	
	# print anims

	res = ''
	res2 = 'animations_table = [\n'
	res2_ = []
	name_id = 0
	name_ids = ''

	for name in anims.keys():
		anim = anims[name]
		if not 'hflip' in anim:
			name = name.replace('_right', '')
			res += ('%s = %s\n' % (name, anim['steps']))
			res2_ += ['\t' + name]

			name_ids += '%s = %s\n' % (name.upper(), name_id)
			name_id += 1

	print(res)
	res2 += ',\n'.join(res2_) + '\n]\n'
	print(res2)

	print(name_ids)

def generate_patterns(data):
	base_dir = data['path']
	if 'splits' not in data:
		generate_splits(data)
		
	splits = data['splits']

	patterns = []
	for i, frame in enumerate(data['frames']):
		j = frame['id']
		surf = frame['surface'].copy()

		# print '%d: frame %d (%s) -> %x' % (i, j, surf.get_size(), len(patterns))
		
		for k, rect in enumerate(splits[j]):
			sub = get_subsurface(surf, rect)
			patterns += get_patterns(sub)
			pygame.image.save(sub, '%s/debug/%02d-%02d.png' % (base_dir, i, k))
			pygame.draw.rect(surf, pygame.Color('red'), rect, 1)
		
		pygame.image.save(surf, '%s/debug/%02d.png' % (base_dir, i))
	
	print('%d patterns generated' % len(patterns))
	make_sheet(patterns, '%s/patterns.png' % base_dir)

	if data['recolor']:
		patterns_surf = pygame.image.load('%s/patterns.png' % base_dir)
		source_path, dest_pathes = data['recolor']
		source_sample = pygame.image.load('%s/%s' % (base_dir, source_path))
		
		for i, dest_path in enumerate(dest_pathes):
			dest_sample = pygame.image.load(	'%s/%s' % (base_dir, dest_path))
			recolored = recolor_surface(patterns_surf, source_sample, dest_sample)
	
			pygame.image.save(recolored, '%s/patterns-%d.png' % (base_dir, i))
			
			if save_recolored_frames:
				for j, frame in enumerate(data['frames']):
					surf = frame['surface']
					recolored = recolor_surface(surf, source_sample, dest_sample)
			
					pygame.image.save(recolored, '%s/recolored%02d-frame%02d.png' % (base_dir, i, j))


def load_gimp_palette(path, id_ = 1):
	with open(path) as f:
		lines = f.readlines()
	
	res = []
	for l in lines:
		if l.startswith('#'):
			col = int(l.strip()[1:], 16)
			res += [col]
	
	if len(res) < 16:
		res += [0] * (16 - len(res))
	
	return Palette.from_rgb_values(res, id_ = id_)

def recolor_surface(target, source, dest):
	def swap_rb(col):
		a, r, g, b = (col >> 24) & 255, (col >> 16) & 255, (col >> 8) & 255, col & 255
		return (a << 24) + (b << 16) + (g << 8) + r
	res = target.copy()
	
	target_ = pygame.surfarray.pixels2d(target)
	source_ = pygame.surfarray.pixels2d(source)
	dest_ = pygame.surfarray.pixels2d(dest)
	res_ = pygame.surfarray.pixels2d(res)

	print ('********')	
	matches = {}
	for col in numpy.unique(source_):
		print(col)
		# dst = swap_rb(numpy.unique(dest_[source_ == col])[0])
		dst = numpy.unique(dest_[source_ == col])[0]
		
		print ('%X -> %X' % (col, dst))
		
		res_[target_ == col] = dst
	
	del res_
	del dest_
	del source_
	del target_
	
	return res
	
	

def generate_sprite(name, hotspot, source_sample = None, alt_samples = []):
	base_dir = 'C:/Users/fterr/Documents/hack/Shinobi/sheets/%s' % name

	frames = read_sheet('%s/sheet.psd' % base_dir)
	anims = load_animdefs('%s/animdefs.txt' % base_dir)
	
	if source_sample:
		recolor = (source_sample, alt_samples)
	else:
		recolor = None
	
	char_data = {
		'path': base_dir,
		'frames': frames,
		'hotspot': hotspot,
		'animdefs': anims,
		'palette': load_gimp_palette('%s/palette.txt' % base_dir),
		'recolor': recolor
	}

	print_frames_table(char_data)
	print_animations_table(char_data)
	generate_patterns(char_data)
	
	exit()

	
# =================================================

import sys
print (sys.argv)

save_recolored_frames = 'save_recolored' in sys.argv

if 'spider' in sys.argv:
	print ('generating spider')
	generate_sprite('spider', (64, 84), 'blue_sample.png', ['black_sample.png'])

if 'guardian' in sys.argv:
	generate_sprite('sword', (64, 95), 'green_sample.png', ['pink_sample.png', 'blue_sample.png'])

if 'frogman' in sys.argv:
	generate_sprite('frogman', (48, 95))

if 'splash' in sys.argv:
	generate_sprite('splash', (16, 31))

if 'bazooka' in sys.argv:
	generate_sprite('bazooka', (64, 127), 'blue.png', ['green.png'])

if 'rocket' in sys.argv:
	generate_sprite('rocket', (22, 18))

if 'shooter' in sys.argv:
	generate_sprite('shooter', (64, 95))
