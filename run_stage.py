from genepy import *
from tsprite import *
from globals import Globs
import res.level_1_1, res.musashi_data
from tilemap import init_stage, set_camera
from res.states.musashi_states import *


def main():
    init_stage(res.level_1_1)

    Globs.base_id = 0
    init_object()

    camera_x = camera_y = 0
    old_joy = joy_pressed = 0
    Globs.forward = BUTTON_RIGHT
    Globs.back = BUTTON_LEFT

    animation = 0

    while True:
        joy = GP.read_joypad(0)
        Globs.joy_pressed = (~old_joy) & joy
        old_joy = joy
        Globs.joy = joy

        update_all_objects()

        camera_x = objects[0].x - 160

        camera_x = max(0, camera_x)
        camera_x = min(Globs.layer_a_pwidth - 320, camera_x)
        camera_y = max(0, camera_y)
        camera_y = min(Globs.layer_a_pheight - 224, camera_y)

        set_camera(camera_x, camera_y)
        print 'camera = %d / musashi = %d' % (Globs.camera_x, objects[0].x)
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
