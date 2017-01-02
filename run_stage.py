from genepy import *
from tsprite import *
from globals import Globs
import res.level_1_1, res.musashi_data
from tilemap import init_stage, set_camera


def main():
    init_stage(res.level_1_1)

    musashi_patterns = load_data_from_png('res/musashi_patterns.png')

    musashi_sprite = TSprite()
    musashi_sprite.status = 1
    musashi_sprite.x = 160
    musashi_sprite.y = 144
    musashi_sprite.patterns = musashi_patterns
    musashi_sprite.frames_table = res.musashi_data.frames_table
    musashi_sprite.animations_table = res.musashi_data.animations_table
    musashi_sprite.frame = 76
    musashi_sprite.patterns_blocks = res.musashi_data.patterns_blocks
    Globs.base_id = 0

    update_patterns(musashi_sprite)
    allocate_sprite(musashi_sprite)

    camera_x = camera_y = 0
    old_joy = joy_pressed = 0

    animation = 0

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
            animation += 1
            set_animation(musashi_sprite, animation)
        elif joy_pressed & BUTTON_B:
            animation -= 1
            set_animation(musashi_sprite, animation)
        elif joy_pressed & BUTTON_C:
            Globs.base_id ^= 0x8000

        camera_x = max(0, camera_x)
        camera_x = min(Globs.layer_a_pwidth - 320, camera_x)
        camera_y = max(0, camera_y)
        camera_y = min(Globs.layer_a_pheight - 224, camera_y)

        set_camera(camera_x, camera_y)
        GP.plane_A_offset = -camera_x, camera_y
        GP.plane_B_offset = -camera_x / 2, camera_y / 2

        update_all_sprites()

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
