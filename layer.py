from genepy import GP
from globals import Globs


class Layer():
	def __init__(self):
		self.plane = None
		self.data = None
		self.twidth = 0
		self.theight = 0
		
layer_A = Layer()
layer_B = Layer()

def draw_tile(plane, tile, x, y):
	x_ = (2*x) & 0x3E
	y_ = (2*y) & 0x3E
	tile *= 4

	# print ('[draw_tile] plane: %s, tile: %X/%X, x: %d, y:%d' % (plane, tile, len(Globs.tileset), x_, y_))
	GP.set_tilemap(plane, Globs.tileset[tile], x_, y_)
	GP.set_tilemap(plane, Globs.tileset[tile + 1], x_ + 1, y_)
	GP.set_tilemap(plane, Globs.tileset[tile + 2], x_, y_ + 1)
	GP.set_tilemap(plane, Globs.tileset[tile + 3], x_ + 1, y_ + 1)
	

def draw_rect(layer, x, y, w, h):
	for j in range(y, y + h):
		if j >= 0 and j < layer.theight:
			for i in range(x, x + w):
				if i >= 0 and i < layer.twidth:
					draw_tile(layer.plane, layer.data[j * layer.twidth + i], i, j)
					

