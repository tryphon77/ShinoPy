from genepy import *
from tsprite import *
from globals import Globs
from tilemap import init_stage, set_camera_focus_to
from object import *

# Organization needed
from res import level_1_1
from res import musashi_data
from res.states import musashi_states
from res.states import punk_states
from res.states import shooter_states
from res.states import knife_states
from res.states import sword_states
from res.states import spidey_states
from res.states import hostage_states
from res import projectile_data 


def main():
    init_stage(level_1_1)

    Globs.base_id = 0
    musashi_states.init_object()
    punk_states.init_object()
    shooter_states.init_object()
    knife_states.init_object()
    sword_states.init_object()
    spidey_states.init_object()
    hostage_states.init_object()

    GP.load_tile_data(projectile_data.patterns, 0x300)
    GP.load_tile_data(hostage_states.patterns, 0x400)

    old_joy = 0
    Globs.forward = BUTTON_RIGHT
    Globs.backward = BUTTON_LEFT

    while True:
        joy = GP.read_joypad(0)
        Globs.joy_pressed = (~old_joy) & joy
        old_joy = joy
        Globs.joy = joy

        update_all_objects()

        set_camera_focus_to(objects[0])

        update_all_sprites()

        GP.wait_vblank()


if __name__ == '__main__':
    GP.init()
    main()
