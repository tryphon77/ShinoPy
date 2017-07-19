import sys
sys.path.append('../../pygato')

import pygame

from map import *
from psd import *


def fmt(c):
	return '%08X' % c

def fmtl(l):
	return '(' + ', '.join([fmt(c) for c in l]) + ')'

def recolor(surf, source, dest):
	res = surf.copy()
	a = pygame.surfarray.pixels2d(res)
	for s, d in zip(source, dest):
		a[a == s] = d
	return res

if True:
	source_dir = 'C:/Users/fterr/Documents/hack/Shinobi/sheets/ninja'
	psd = load_psd('%s/palettes.psd' % source_dir)
	
	arrays = [pygame.surfarray.pixels2d(layer.get_surface()) for layer in psd.get_layers()]
	print (arrays)
	n = len(arrays)
	
	base_colors = []
	colors = []
	
	(w, h) = arrays[0].shape
	print (w, h)
	
	for y in range(h):
		for x in range(w):
			cs = [arrays[i][x, y] for i in range(n)] 
			# print ('x: %d | y: %d | colors: %s | %d | %d' % (x, y, fmtl(cs), len(base_colors), len(colors)))
			
			c = cs[0]
			if c in base_colors:
				k = base_colors.index(c)
				cols = colors[k]
				if cols != cs:
					print('unmatching colors : %s != %s' % (cs, cols))
					exit()
			else:
				base_colors += [c]
				colors += [cs]

	for i in range(n):
		print (', '.join([fmt(c[i]) for c in colors]))
		print ('=======================')

	pal_vert = [
		0x00000000, 0x00FFFFFF, 0xFFF7F7F7, 0xFFB5B5B5, 
		0xFF00CE00, 0xFF00FF00, 0xFF00E600, 0xFF00B500, 
		0xFF009C00, 0xFFFFC594, 0xFFB59463, 0xFF008400, 
		0xFF000000, 0xFFFF0000, 0xFFAD0000, 0xFFD60000
	]
	
	pal_bleu = [
		0x00000000, 0x00FFFFFF, 0xFFF7F7F7, 0xFFB5B5B5, 
		0xFF0000CE, 0xFF0000FF, 0xFF0000E6, 0xFF0000B5, 
		0xFF00009C, 0xFFFFC594, 0xFFB59463, 0xFF000084, 
		0xFF000000, 0xFFB594A4, 0xFF735263, 0xFF947384
	]

	pal_rouge = [
		0x00000000, 0x00FFFFFF, 0xFFF7F7F7, 0xFFB5B5B5, 
		0xFFCE0000, 0xFFFF0000, 0xFFE60000, 0xFFB50000, 
		0xFF9C0000, 0xFFFFC594, 0xFFB59463, 0xFF840000, 
		0xFF000000, 0xFF00A4B5, 0xFF006373, 0xFF008494
	]

	pal_jaune = [
		0x00000000, 0x00FFFFFF, 0xFFF7F7F7, 0xFFB5B5B5, 
		0xFFCECE00, 0xFFF7F700, 0xFFE6E600, 0xFFB5B500, 
		0xFF9C9C00, 0xFFFFC594, 0xFFB59463, 0xFF848400, 
		0xFF000000, 0xFF0000FF, 0xFF0000AD, 0xFF0000D6
	]
	
	pal_magenta = [
		0x00000000, 0x00FFFFFF, 0xFFF7F7F7, 0xFFB5B5B5, 
		0xFFCE00CE, 0xFFFF00FF, 0xFFE600E6, 0xFFB500B5, 
		0xFF9C009C, 0xFFFFC594, 0xFFB59463, 0xFF840084, 
		0xFF000000, 0xFF00FF00, 0xFF00AD00, 0xFF00D600
	]
	
	
	sheet = load_psd('%s/sheet.psd' % source_dir)
	for i in [1, 2, 3, 22]:
		base = sheet.get_layers()[i]
		surf = recolor(base.get_surface(), pal_rouge, pal_vert)
		pygame.image.save(surf, '%s/temp/recolored%02d.png' % (source_dir, i))
	
	for i in [19, 20]:
		base = sheet.get_layers()[i]
		surf = recolor(base.get_surface(), pal_bleu, pal_vert)
		pygame.image.save(surf, '%s/temp/recolored%02d.png' % (source_dir, i))