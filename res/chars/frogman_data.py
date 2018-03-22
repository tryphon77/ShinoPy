from genepy import load_data_from_png
from tsprite import TSpriteData


patterns = load_data_from_png('res/chars/frogman_patterns.png')

frames_table = [
        [               # frame 0
                [-15, -17, -62, 0x000C, 0x00]
        ],
        [               # frame 1
                [-11, -5, -15, 0x0005, 0x04],
                [-11, -13, -23, 0x0008, 0x08],
                [-18, -14, -39, 0x000D, 0x0B],
                [-20, -4, -47, 0x0008, 0x13],
                [-24, -8, -63, 0x000D, 0x16],
                [-12, 4, -71, 0x0000, 0x1E]
        ],
        [               # frame 2
                [-14, -10, -63, 0x000B, 0x1F],
                [-6, -10, -31, 0x0007, 0x2B],
                [10, -34, -47, 0x0008, 0x33],
                [-6, -10, -71, 0x0004, 0x36],
                [26, -42, -55, 0x0004, 0x38],
                [-14, 6, -31, 0x0000, 0x3A],
                [18, -26, -15, 0x0000, 0x3B],
                [-14, 6, -7, 0x0000, 0x3C]
        ],
        [               # frame 3
                [-13, 5, -7, 0x0000, 0x3D],
                [-15, -9, -15, 0x0008, 0x3E],
                [-7, -9, -23, 0x0004, 0x41],
                [-9, -15, -31, 0x0008, 0x43],
                [-11, -21, -39, 0x000C, 0x46],
                [-10, -14, -47, 0x0008, 0x4A],
                [-17, -15, -63, 0x000D, 0x4D],
                [-2, -14, -71, 0x0004, 0x55]
        ],
        [               # frame 4
                [-17, -15, -39, 0x000F, 0x57],
                [-17, -15, -7, 0x000C, 0x67],
                [-9, -15, -47, 0x0008, 0x6B]
        ],
        [               # frame 5
                [-15, -9, -63, 0x000B, 0x6E],
                [-15, -9, -31, 0x000B, 0x7A],
                [9, -17, -39, 0x0001, 0x86]
        ],
        [               # frame 6
                [-24, -8, -24, 0x000E, 0x88],
                [8, -32, -24, 0x0009, 0x94],
                [-8, -24, -32, 0x000C, 0x9A],
                [0, -8, -40, 0x0000, 0x9E],
                [-24, 16, -32, 0x0000, 0x9F],
                [-32, 24, -24, 0x0000, 0xA0]
        ]
]

patterns_blocks = [
        [0x0000, 0x0004],
        [0x0004, 0x001B],
        [0x001F, 0x001E],
        [0x003D, 0x001A],
        [0x0057, 0x0017],
        [0x006E, 0x001A],
        [0x0088, 0x0019]
]

hidden = [(0, 1)]
jump = [(1, 1)]
attack = [(2, 15), (3, 15)]
crouch = [(4, 60)]
leap = [(5, 1)]
hit = [(6, 1)]
death = [(6, 14)]

animations_table = [
        hidden,
        jump,
        attack,
        crouch,
        leap,
        hit,
        death
]

HIDDEN = 0
JUMP = 1
ATTACK = 2
CROUCH = 3
LEAP = 4
HIT = 5
DEATH = 6

rect0 = (-16, -63, 32, 64)
rect1 = (-10, -63, 20, 64)
rect2 = (-10, -47, 20, 48)
rect3 = (-10, -61, 20, 62)

bounding_boxes = [
    None,        # bounding box 0,
    rect1,        # bounding box 1,
    rect1,        # bounding box 2,
    rect1,        # bounding box 3,
    rect2,        # bounding box 4,
    rect3,        # bounding box 5,
    None        # bounding box 6,
]

hitboxes = [None] * 7


sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "frogman")
