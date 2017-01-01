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

#    print 'draw_tile', (plane, tile, x_, y_)
    GP.set_tilemap(plane, Globs.tileset[tile], x_, y_);
    GP.set_tilemap(plane, Globs.tileset[tile + 1], x_ + 1, y_);
    GP.set_tilemap(plane, Globs.tileset[tile + 2], x_, y_ + 1);
    GP.set_tilemap(plane, Globs.tileset[tile + 3], x_ + 1, y_ + 1);
    

def draw_rect(layer, x, y, w, h):
    for j in range(y, y + h):
        if j >= 0 and j < layer.theight:
            for i in range(x, x + w):
                if i >= 0 and i < layer.twidth:
                    draw_tile(layer.plane, layer.data[j * layer.twidth + i], i, j)
                    


def init_stage(stage):
    # load background
    GP.load_tile_data(stage.patterns, 0) 
    
    # load tileset
    Globs.tileset = stage.tileset
    
    # load tilemap
    layer_A.plane = GP.plane_A
    layer_A.data = stage.tilemap_A
    layer_A.twidth = stage.twidth
    layer_A.theight = stage.theight

#    Globs.layer_a_twidth = stage.twidth;
#    Globs.layer_a_theight = stage.theight;
    Globs.layer_a_pwidth = stage.twidth * 16;
    Globs.layer_a_pheight = stage.theight * 16;

    layer_B.plane = GP.plane_B
    layer_B.data = stage.tilemap_B    
    layer_B.twidth = stage.twidth/2 + 10;
    layer_B.theight = stage.theight/2 + 7;
    
    Globs.layer_b_pwidth = stage.twidth * 16;
    Globs.layer_b_pheight = stage.theight * 16;

    Globs.camera_x = 0
    Globs.camera_y = 0
    
    draw_rect(layer_A, 0, 0, 32, 15)
    draw_rect(layer_B, 0, 0, 21, 15)
    
    Globs.vscroll_mode = 0

def set_camera(camera_new_x, camera_new_y):
    dx = camera_new_x/16 - Globs.camera_x/16;
    dy = camera_new_y/16 - Globs.camera_y/16;

    if dx > 0:
        draw_rect(layer_A, Globs.camera_x/16 + 21, Globs.camera_y/16 - 1, dx, 16)
    elif dx < 0:
        draw_rect(layer_A, camera_new_x/16 - 1, Globs.camera_y/16 - 1, -dx, 16)

    if dy > 0:
        draw_rect(layer_A, Globs.camera_x/16 - 1, Globs.camera_y/16 + 15, 22, dy)
    elif dy < 0:
        draw_rect(layer_A, camera_new_x/16 - 1, Globs.camera_y/16 - 1, 22, -dy)


    dx = camera_new_x/32 - Globs.camera_x/32;
    dy = camera_new_y/32 - Globs.camera_y/32;

    if dx > 0:
        draw_rect(layer_B, Globs.camera_x/32 + 21, Globs.camera_y/32 - 1, dx, 16)
    elif dx < 0:
        draw_rect(layer_B, camera_new_x/32 - 1, Globs.camera_y/32 - 1, -dx, 16)

    if dy > 0:
        draw_rect(layer_B, Globs.camera_x/32 - 1, Globs.camera_y/32 + 15, 22, dy)
    elif dy < 0:
        draw_rect(layer_B, camera_new_x/32 - 1, Globs.camera_y/32 - 1, 22, -dy)
    
    Globs.old_camera_x = Globs.camera_x;
    Globs.old_camera_y = Globs.camera_y;
    Globs.camera_x = camera_new_x;
    Globs.camera_y = camera_new_y;    
