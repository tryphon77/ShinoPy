from genepy import load_data_from_png
from tsprite import TSpriteData

patterns = load_data_from_png('res/chars/toad_b_patterns.png')


frames_table = [
        [               # frame 0
                [-17, -7, -7, 0x0008, 0x00],
                [-19, -13, -31, 0x000E, 0x03],
                [-13, -11, -39, 0x0008, 0x0F]
        ],
        [               # frame 1
                [-17, -7, -7, 0x0008, 0x12],
                [-14, -10, -15, 0x0008, 0x15],
                [-18, -14, -39, 0x000E, 0x18],
                [0, -8, -47, 0x0000, 0x24]
        ],
        [               # frame 2
                [-16, -8, -15, 0x0009, 0x25],
                [-24, -8, -23, 0x000C, 0x2B],
                [-23, -1, -31, 0x0008, 0x2F],
                [-20, -12, -39, 0x000C, 0x32],
                [-11, -13, -47, 0x0008, 0x36],
                [-6, -10, -55, 0x0004, 0x39]
        ],
        [               # frame 3
                [-16, 8, -7, 0x0000, 0x3B],
                [-18, 2, -15, 0x0004, 0x3C],
                [-18, -6, -39, 0x000A, 0x3E],
                [-19, -13, -63, 0x000E, 0x47]
        ],
        [               # frame 4
                [-13, -3, -8, 0x0004, 0x53],
                [-19, -13, -32, 0x000E, 0x55],
                [-5, -11, -40, 0x0004, 0x61]
        ],
        [               # frame 5
                [-8, -16, -31, 0x000A, 0x63],
                [-16, -8, -7, 0x0008, 0x6C],
                [-16, 8, -23, 0x0001, 0x6F]
        ],
        [               # frame 6
                [-14, -18, -15, 0x000D, 0x71],
                [-9, -15, -23, 0x0008, 0x79]
        ]
]

patterns_blocks = [
        [0x0000, 0x0012],
        [0x0012, 0x0013],
        [0x0025, 0x0016],
        [0x003B, 0x0018],
        [0x0053, 0x0010],
        [0x0063, 0x000E],
        [0x0071, 0x000B]
]

wait = [(0, 20), (1, 20)]
jump_start = [(2, 4), (0, 20)]
jump_mid = [(3, 1)]
hit = [(4, 1)]
death = [(4, 8), (5, 8), (6, 30)]

animations_table = [
        wait,
        jump_start,
        jump_mid,
        hit,
        death
]

WAIT = 0
JUMP_START = 1
JUMP_MID = 2
HIT = 3
DEATH = 4


rect0 = (-32, -47, 64, 48)
rect1 = (-8, -39, 16, 40)

bounding_boxes = [
    rect1,    # bounding box 0,
    rect1,    # bounding box 1,
    rect1,    # bounding box 2,
    rect1,    # bounding box 3,
    None,    # bounding box 4,
    None,    # bounding box 5,
    None,    # bounding box 6,
]

hitboxes = [None]*7

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "toad_b")

