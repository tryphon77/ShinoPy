from genepy import *
from globals import Globs
import res.level_1_1, res.musashi_data
from tilemap import init_stage, draw_tile, layer_A, layer_B, set_camera
import numpy

class TSprite():
    def __init__(self):
        self.patterns = None
        self.frames_table = None
        self.patterns_blocks = None
        self.x = 0
        self.y = 0
        self.frame = 0

sizes = [1, 2, 3, 4, 2, 4, 6, 8, 3, 6, 9, 12, 4, 8, 12, 16]

def update_patterns(sprite):
    start, ln = sprite.patterns_blocks[sprite.frame]
    GP.load_tile_data(sprite.patterns[start : start + ln], 0x200)
    print sprite.frame, ':', sprite.frames_table[sprite.frame]

def update_sprite(sprite):    
    x = sprite.x
    y = sprite.y
    t_id = 0x200
#    print sprite.frames_table[sprite.frame]
    for (dx, dy, sz, dp) in sprite.frames_table[sprite.frame]:
        GP.set_sprite(Globs.link, 
                      x + dx, 
                      y + dy, 
                      sz,
                      Globs.base_id + t_id, 
                      Globs.link + 1)
        t_id += sizes[sz]
        Globs.link += 1
    

def main():
    init_stage(res.level_1_1)

    musashi_patterns = load_data_from_png('res/musashi_patterns.png')
    
    musashi_sprite = TSprite()
    musashi_sprite.x = 160
    musashi_sprite.y = 144
    musashi_sprite.frames_table = res.musashi_data.frames_table
    musashi_sprite.patterns = musashi_patterns
    musashi_sprite.frame = 76
    musashi_sprite.patterns_blocks = res.musashi_data.patterns_blocks
    Globs.base_id = 0
    
    update_patterns(musashi_sprite)   

    camera_x = camera_y = 0
    old_joy = joy_pressed = 0
    
    while True:
        joy = GP.read_joypad(0)
        joy_pressed = (~old_joy) & joy
        old_joy = joy
        
        if joy & BUTTON_LEFT:
            camera_x -= 1
        if joy & BUTTON_RIGHT:
            camera_x += 1
        if joy & BUTTON_UP:
            camera_y -= 1
        if joy & BUTTON_DOWN:
            camera_y += 1
        
        if joy_pressed & BUTTON_A:
            musashi_sprite.frame += 1
            update_patterns(musashi_sprite)
        elif joy_pressed & BUTTON_B:
            musashi_sprite.frame -= 1
            update_patterns(musashi_sprite)
        elif joy_pressed & BUTTON_C:
            Globs.base_id ^= 0x8000
            
        
        camera_x = max(0, camera_x)
        camera_x = min(Globs.layer_a_pwidth - 320, camera_x)
        camera_y = max(0, camera_y)
        camera_y = min(Globs.layer_a_pheight - 224, camera_y)

        set_camera(camera_x, camera_y)
        GP.plane_A_offset = -camera_x, camera_y
        GP.plane_B_offset = -camera_x/2, camera_y/2
        
        Globs.link = 0
        update_sprite(musashi_sprite)
        GP.sprite_cache[Globs.link - 1].link = 0
        
        GP.wait_vblank()

if __name__ == '__main__':
#     test = numpy.array([1, 2, 3, 4], dtype = '>i2')
#     test.shape = (2, 2)
#     print test
#     test.tofile('test.bin')
#     
#     test2 = numpy.fromfile('test.bin', dtype = '>i2')
#     test2.shape = (2, 2)
#     print test2
    
    GP.init()
    main()
        