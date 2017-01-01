from genepy import GP
from globals import Globs


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
    GP.load_tile_data(sprite.patterns[start:start + ln], 0x200)
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
