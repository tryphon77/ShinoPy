from object import *
from tsprite import *
from genepy import *
from res.musashi_data import *
from res import projectiles


def init_object():
    print 'init_object'
    self = allocate_object()
    self.status = ACTIVE

    self.x = 160
    self.y = 127
    self.floor = 2

    self.back = -10
    self.front = 10

    self.sprite = sprite = allocate_sprite()
    sprite.vpos = 0x200
    sprite.status = 1
    sprite.is_dynamic = True
    sprite.x = self.x
    sprite.y = self.y
    sprite.patterns = load_data_from_png('res/musashi_patterns.png')
    sprite.frames_table = frames_table
    sprite.animations_table = animations_table
    sprite.frame = 76
    sprite.patterns_blocks = patterns_blocks
    sprite.bbox = (-6, 0, 16, 64)

    init_stand(self)


def init_stand(self):
    # print 'init_stand'
    set_animation(self.sprite, STAND)
    set_physics(self, 0, 0, 0, 0)
    self.update_function = update_stand


def update_stand(self):
    # print 'update_stand'
    if not (collides_background(self, self.front, 1) or
            collides_background(self, self.back, 1)):
        init_fall(self)
    elif (Globs.joy_pressed & BUTTON_B):
        init_fire(self)
    elif (Globs.joy_pressed & BUTTON_C):
        init_jump(self)
    elif (Globs.joy & Globs.forward)\
            and collides_background(self, self.front + 1, 0) == 0:
        init_walk(self)
    elif Globs.joy & Globs.backward:
        flip_controls()
        flip(self)
        init_walk(self)
    elif Globs.joy & BUTTON_UP:
        init_prepare_hijump_up(self)
    elif Globs.joy & BUTTON_DOWN:
        init_crouch(self)


def init_fire(self):
    set_physics(self, 0, 0, 0, 0)
    print 'fire %d' % self.sprite.frame
    set_animation(self.sprite, walk_fire_anims[self.sprite.frame])
    throw_shuriken(self, 32, -48)
    self.update_function = update_fire


def update_fire(self):
    if self.sprite.is_animation_over:
        init_stand(self)


def throw_shuriken(self, dx, dy):
    shuriken = projectiles.init_object()
    shuriken.x = self.x + signate(self, dx)
    shuriken.y = self.y + dy
    shuriken.floor = self.floor
    shuriken.speed_x = signate(self, 4)
    shuriken.is_flipped = self.is_flipped
    print 'throw .x = %d, .speed = %d, .front = %d' % (shuriken.x, shuriken.speed_x, shuriken.front)


def init_walk(self):
    # print 'init_walk'
    set_animation(self.sprite, WALK)
    set_physics(self, 2, 0, 0, 0)
    self.update_function = update_walk


def update_walk(self):
    # print 'update_walk'
    if not (Globs.joy & Globs.forward):
        init_stand(self)
    elif (Globs.joy_pressed & BUTTON_B):
        init_fire(self)
    elif (Globs.joy_pressed & BUTTON_C):
        init_jump(self)
    elif Globs.joy & BUTTON_DOWN:
        init_crawl(self)
    else:
        self.x += self.speed_x
        # print 'collision:', collides_background(self, self.front, 0)
        # print 'moving: x = %d' % self.x

        if not (collides_background(self, self.front, 1) or
                collides_background(self, self.back, 1)):
            init_fall(self)
        elif collides_background(self, self.front, 0):
            print 'collision'
            fix_hpos(self)
            init_stand(self)


def init_prepare_hijump_up(self):
    set_animation(self.sprite, HIJUMP_PREPARATION)
    self.speed_y = 0
    self.accel_y = 0
    self.update_function = update_prepare_hijump_up


def update_prepare_hijump_up(self):
    if not (Globs.joy & BUTTON_UP):
        init_stand(self)
    elif Globs.joy_pressed & BUTTON_C:
        if self.floor < 2:
            init_hijump_up(self)
        else:
            init_jump(self)


def init_hijump_up(self):
    self.floor += 1
    self.speed_y = self.accel_y = 0
    set_animation(self.sprite, HIJUMP0)
    self.update_function = update_hijump_up


def update_hijump_up(self):
    if self.sprite.is_animation_over:
        init_hijump1_up(self)


def init_hijump1_up(self):
    self.speed_y = get_hijump_impulsion(self)
    self.accel_y = 0.5
    set_animation(self.sprite, HIJUMP1)
    self.update_function = update_hijump1_up


def update_hijump1_up(self):
    self.speed_y += self.accel_y
    self.y += self.speed_y
    if self.speed_y >= 0:
        init_hifall(self)


def init_crouch(self):
    set_animation(self.sprite, CROUCH_NO_MOVE)
    self.speed_y = 0
    self.accel_y = 0
    self.update_function = update_crouch


def update_crouch(self):
    if not (Globs.joy & BUTTON_DOWN):
        init_stand(self)
    elif (Globs.joy & Globs.backward):
        flip_controls()
        flip(self)
        init_crawl(self)
    elif (Globs.joy_pressed & BUTTON_B):
        init_crouch_fire(self)
    elif Globs.joy_pressed & BUTTON_C:
        if self.floor > 1:
            init_hijump_down(self)
        else:
            init_jump(self)
    elif Globs.joy & Globs.forward\
            and collides_background(self, self.front + 1, 0) == 0:
        init_crawl(self)


def init_crawl(self):
    set_physics(self, 1, 0, 0, 0)
    set_animation(self.sprite, CROUCH)
    self.update_function = update_crawl


def update_crawl(self):
    if not (Globs.joy & BUTTON_DOWN):
        init_stand(self)
    elif not (Globs.joy & Globs.forward):
        init_crouch(self)
    elif Globs.joy_pressed & BUTTON_B:
        init_crouch_fire(self)
    elif Globs.joy_pressed & BUTTON_C:
        if self.floor > 1:
            init_hijump_down(self)
        else:
            init_jump(self)
    else:
        self.x += self.speed_x
        # print 'collision:', collides_background(self, self.front, 0)
        # print 'moving: x = %d' % self.x

        if not (collides_background(self, self.front, 1) or
                collides_background(self, self.back, 1)):
            init_fall(self)
        elif collides_background(self, self.front, 0):
            print 'collision'
            fix_hpos(self)
            init_crouch(self)


def init_crouch_fire(self):
    set_physics(self, 0, 0, 0, 0)
    print 'fire %d' % self.sprite.frame
    set_animation(self.sprite, crouch_fire_anims[self.sprite.frame - 17])
    throw_shuriken(self, 32, -24)
    self.update_function = update_crouch_fire


def update_crouch_fire(self):
    if self.sprite.is_animation_over:
        init_crouch(self)


def init_hijump_down(self):
    set_animation(self.sprite, HIFALL0)
    self.update_function = update_hijump_down


def update_hijump_down(self):
    if self.sprite.is_animation_over:
        init_hijump1_down(self)


def init_hijump1_down(self):
    self.speed_y = -6
    self.accel_y = 0.5
    self.floor -= 1
    set_animation(self.sprite, HIFALL1)
    self.update_function = update_hijump1_down


def update_hijump1_down(self):
    self.speed_y += self.accel_y
    self.y += self.speed_y
    if self.speed_y >= 0:
        init_hifall(self)


def init_hifall(self):
    self.sprite.vpos ^= 0x8000
    self.update_function = update_hifall


def update_hifall(self):
    self.speed_y += self.accel_y
    self.y += self.speed_y
    if collides_background(self, self.front, 1) or\
            collides_background(self, self.back, 1):
        fix_vpos(self)
        init_stand(self)


def init_jump(self):
    set_animation(self.sprite, JUMP)
    self.speed_y = -8.5
    self.accel_y = 0.5
    self.update_function = update_jump


def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val


def update_jump_action(self):
    self.accel_x = 0
    if Globs.joy & Globs.forward:
        self.accel_x = signate(self, 0.125)
    elif Globs.joy & Globs.backward:
        self.accel_x = signate(self, -0.125)

    self.speed_x += self.accel_x
    self.speed_x = clamp(self.speed_x, -2, 2)
    self.x += self.speed_x

    if self.is_flipped:
        if self.speed_x > 0:
            flip_controls()
            flip(self)
    elif self.speed_x < 0:
            flip_controls()
            flip(self)


def update_jump_position(self):
    update_jump_action(self)
    self.speed_y += self.accel_y
    self.y += self.speed_y

    if collides_background(self, self.front, 0):
        fix_hpos(self)
        self.speed_x = 0


def update_fall_position(self):
    update_jump_action(self)

    if collides_background(self, self.front, 0):
        fix_hpos(self)
        self.speed_x = 0

    self.speed_y += self.accel_y
    self.y += self.speed_y

    if collides_background(self, self.front, 0) or\
            collides_background(self, self.back, 0):
        fix_vpos(self)
        init_stand(self)


def update_jump(self):
    if self.speed_y >= 0:
        init_fall(self)
    elif Globs.joy_pressed & BUTTON_B:
        init_jump_fire(self)
    update_jump_position(self)


def init_jump_fire(self):
    set_animation(self.sprite, JUMP_FIRE)
    throw_shuriken(self, 32, -48)
    self.update_function = update_jump_fire


def update_jump_fire(self):
    if self.sprite.is_animation_over:
        set_animation(self.sprite, JUMP)
        self.update_function = update_jump
    elif self.speed_y >= 0:
        change_animation(self.sprite, FALL_FIRE)
        self.update_function = update_fall_fire
    update_jump_position(self)


def init_fall(self):
    set_animation(self.sprite, FALL)
    self.accel_y = 0.5
    self.update_function = update_fall


def update_fall(self):
    if Globs.joy_pressed & BUTTON_B:
        init_fall_fire(self)
    else:
        update_fall_position(self)


def init_fall_fire(self):
    set_animation(self.sprite, FALL_FIRE)
    throw_shuriken(self, 32, -48)
    self.update_function = update_fall_fire


def update_fall_fire(self):
    if self.sprite.is_animation_over:
        set_animation(self.sprite, FALL)
        self.update_function = update_jump
    update_fall_position(self)

