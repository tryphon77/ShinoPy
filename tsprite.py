from genepy import GP
from globals import Globs


NONE = 0
ACTIVE = 1


class TSprite():
    def __init__(self):
        self.status = NONE
        self.is_dynamic = False
        self.is_flipped = False
        self.vpos = 0
        self.needs_refresh_patterns = False

        self.x = 0
        self.y = 0

        self.patterns = None
        self.frames_table = None
        self.patterns_blocks = None
        self.frame = 0

        self.animations_table = None
        self.animation = None
        self.animation_id = -1
        self.tick = 0
        self.total_ticks_in_animation = 0
        self.is_animation_over = False

        self.bboxes_table = None
        self.hitboxes_table = None
        self.bbox = None
        self.hitbox = None


sprites_size = 16
sprites = [TSprite()] * sprites_size


def allocate_sprite(sprite):
    for i, s in enumerate(sprites):
        if s.status == 0:
            print 'allocating sprite %s in slot %d' % (sprite, i)
            sprites[i] = sprite
            return 1
    GP.exit_with_error('Overflow in TSprite.allocate_sprite')


sizes = [1, 2, 3, 4, 2, 4, 6, 8, 3, 6, 9, 12, 4, 8, 12, 16]


def update_patterns(sprite):
    start, ln = sprite.patterns_blocks[sprite.frame]
    GP.load_tile_data(sprite.patterns[start:start + ln], 0x200)


def update_frame(sprite):
    x = sprite.x
    y = sprite.y
    t_id = 0x200
#    print sprite.frames_table[sprite.frame]

    if sprite.is_flipped:
        for (_, dx, dy, sz, dp) in sprite.frames_table[sprite.frame]:
            t_id |= 0x800
            GP.set_sprite(Globs.link,
                          x + dx,
                          y + dy,
                          sz,
                          Globs.base_id + t_id,
                          Globs.link + 1)
            t_id += sizes[sz]
            Globs.link += 1
    else:
        for (dx, _, dy, sz, dp) in sprite.frames_table[sprite.frame]:
            GP.set_sprite(Globs.link,
                          x + dx,
                          y + dy,
                          sz,
                          Globs.base_id + t_id,
                          Globs.link + 1)
            t_id += sizes[sz]
            Globs.link += 1


def set_animation(self, anim):
    self.total_ticks_in_animation = 0
    if self.animation_id != anim:
        self.animation_id = anim
        self.animation = self.animations_table[anim]
        self.animation_index = 0
        load_next_frame(self)


def load_next_frame(self):
    # animation format :
    # frame_id, ticks, x, y, clsn1_rect_id, clsn2_rect_id for all frames except last
    # -1, frame_id, X, X, X, X for last frame

    frame_id, ticks = self.animation[self.animation_index]

    self.is_animation_over = False
    if frame_id < 0:
        self.is_animation_over = True
        self.animation_index = ticks
        frame_id, ticks = self.animation[self.animation_index]

    if self.frame != frame_id:
        self.frame = frame_id
        self.needs_refresh_patterns = True

    self.tick = ticks

    self.animation_index += 1


def update_animation(self):
    self.total_ticks_in_animation += 1
    self.tick -= 1
    if self.tick == 0:
        load_next_frame(self)


def sprite_update(spr):
    if spr.status:
        update_animation(spr)
    if spr.needs_refresh_patterns:
        update_patterns(spr)
    update_frame(spr)


def update_all_sprites():
    Globs.link = 0
    for sprite in sprites:
        if sprite.status == 0:
            break
        sprite_update(sprite)
    GP.sprite_cache[Globs.link - 1].link = 0
