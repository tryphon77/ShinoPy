from genepy import *
from globals import *
from layer import layer_A, layer_B, draw_rect

class Camera():
    def __init__(self):
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        self.virtual_left = 0
        self.virtual_right = 0
        self.virtual_top = 0
        self.virtual_bottom = 0
        
        self.moves_left = False
        self.moves_right = False
        self.moves_top = False
        self.moves_down = False
        

camera = Camera()

def set_camera(camera_new_x, camera_new_y):
    dx = camera_new_x - Globs.camera_x
    dy = camera_new_y - Globs.camera_y

    camera.moves_left = (dx < 0)
    camera.moves_right = (dx > 0)
    camera.moves_up = (dy < 0)
    camera.moves_down = (dy > 0)

    dx = camera_new_x//16 - Globs.camera_x//16
    dy = camera_new_y//16 - Globs.camera_y//16

    if dx > 0:
        draw_rect(layer_A, Globs.camera_x//16 + 21, Globs.camera_y//16 - 1, dx, 16)
    elif dx < 0:
        draw_rect(layer_A, camera_new_x//16 - 1, Globs.camera_y//16 - 1, -dx, 16)

    if dy > 0:
        draw_rect(layer_A, Globs.camera_x//16 - 1, Globs.camera_y//16 + 15, 22, dy)
    elif dy < 0:
        draw_rect(layer_A, camera_new_x//16 - 1, Globs.camera_y//16 - 1, 22, -dy)


    dx = camera_new_x//32 - Globs.camera_x//32
    dy = camera_new_y//32 - Globs.camera_y//32

    if dx > 0:
        draw_rect(layer_B, Globs.camera_x//32 + 21, Globs.camera_y//32 - 1, dx, 16)
    elif dx < 0:
        draw_rect(layer_B, camera_new_x//32 - 1, Globs.camera_y//32 - 1, -dx, 16)

    if dy > 0:
        draw_rect(layer_B, Globs.camera_x//32 - 1, Globs.camera_y//32 + 15, 22, dy)
    elif dy < 0:
        draw_rect(layer_B, camera_new_x//32 - 1, Globs.camera_y//32 - 1, 22, -dy)

    Globs.old_camera_x = Globs.camera_x
    Globs.old_camera_y = Globs.camera_y
    Globs.camera_x = camera_new_x
    Globs.camera_y = camera_new_y

    camera.left = camera_new_x
    camera.virtual_left = camera_new_x - 32
    camera.right = camera_new_x + 319
    camera.virtual_right = camera_new_x + 351
    camera.top = camera_new_y
    camera.virtual_top = camera_new_y - 32
    camera.bottom = camera_new_y + 223
    camera.virtual_bottom = camera_new_y + 271


def set_camera_focus_to(obj):
    camera_x = int(obj.x) - 160

    camera_x = max(0, camera_x)
    camera_x = min(Globs.layer_a_pwidth - 320, camera_x)

    # adjust camera_y
    camera_y = Globs.camera_y
    y = int(obj.y)
    sy = y - camera_y

    if Globs.vscroll_mode:
        sy = y - camera_y
        if sy < 64:
            sy = 64
            camera_y = y - 64
            if camera_y < 0:
                camera_y = 0
                sy = y

        elif sy > 208:
            sy = 208
            camera_y = y - 208
            if camera_y >= Globs.layer_a_pheight - 224:
                camera_y = Globs.layer_a_pheight - 224
                sy = y - camera_y

    else:
        if sy < 120 and camera_y > 0:
            camera_y -= 1
        elif sy > 120 and camera_y < Globs.layer_a_pheight - 224:
            camera_y += 1


    camera_y = max(0, camera_y)
    camera_y = min(Globs.layer_a_pheight - 224, camera_y)

    set_camera(camera_x, camera_y)
    # print 'camera = %d // musashi = %d' % (Globs.camera_x, objects[0].x)
    GP.plane_A_offset = -camera_x, camera_y
    GP.plane_B_offset = -camera_x // 2, camera_y // 2
