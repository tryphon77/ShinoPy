from genepy import load_data_from_png
from tsprite import TSpriteData

patterns = load_data_from_png('res/chars/toad_a_patterns.png')


frames_table = [
        [               # frame 0
                [-17, -15, -39, 0x000E, 0x00],
                [-9, -7, -15, 0x0005, 0x0C],
                [-17, 9, -15, 0x0000, 0x10]
        ],
        [               # frame 1
                [-2, -6, -8, 0x0000, 0x11],
                [-18, -6, -16, 0x0008, 0x12],
                [-17, -15, -40, 0x000E, 0x15],
                [3, -11, -48, 0x0000, 0x21]
        ],
        [               # frame 2
                [8, -16, -35, 0x0001, 0x22],
                [-8, -8, -31, 0x0007, 0x24],
                [-16, 8, -30, 0x0002, 0x2C],
                [-24, 16, -24, 0x0001, 0x2F]
        ],
        [               # frame 3
                [-13, -3, -7, 0x0004, 0x31],
                [-21, -3, -15, 0x0008, 0x33],
                [-16, -16, -31, 0x000D, 0x36],
                [-12, -20, -39, 0x000C, 0x3E]
        ],
        [               # frame 4
                [-11, -5, -7, 0x0004, 0x42],
                [-13, -3, -15, 0x0004, 0x44],
                [-17, -15, -31, 0x000D, 0x46],
                [-9, -23, -47, 0x000D, 0x4E],
                [23, -31, -47, 0x0001, 0x56],
                [11, -19, -55, 0x0000, 0x58]
        ],
        [               # frame 5
                [-17, -15, -35, 0x000D, 0x59],
                [-17, 1, -19, 0x0006, 0x61],
                [-25, 17, -19, 0x0000, 0x67]
        ],
        [               # frame 6
                [-20, -4, -27, 0x000A, 0x68],
                [-12, -4, -3, 0x0004, 0x71],
                [4, -12, -27, 0x0001, 0x73],
                [-28, 20, -19, 0x0000, 0x75]
        ],
        [               # frame 7
                [-21, -11, -18, 0x000D, 0x76],
                [-13, -3, -2, 0x0004, 0x7E],
                [11, -19, -18, 0x0000, 0x80]
        ]
]

patterns_blocks = [
        [0x0000, 0x0011],
        [0x0011, 0x0011],
        [0x0022, 0x000F],
        [0x0031, 0x0011],
        [0x0042, 0x0017],
        [0x0059, 0x000F],
        [0x0068, 0x000E],
        [0x0076, 0x000B]
]

wait = [(0, 20), (1, 20)]
jump_start = [(3, 4)]
jump_mid = [(4, 1)]
jump_end = [(3, 3), (2, 20)]
hit = [(5, 1)]
death = [(5, 8), (6, 8), (7, 30)]

animations_table = [
        wait,
        jump_start,
        jump_mid,
        jump_end,
        hit,
        death
]

WAIT = 0
JUMP_START = 1
JUMP_MID = 2
JUMP_END = 3
HIT = 4
DEATH = 5


rect0 = (-32, -47, 64, 48)
rect1 = (-8, -39, 16, 40)

bounding_boxes = [
    rect1,    # bounding box 0,
    rect1,    # bounding box 1,
    rect1,    # bounding box 2,
    rect1,    # bounding box 3,
    rect1,    # bounding box 4,
    None,    # bounding box 5,
    None,    # bounding box 6,
    None,    # bounding box 7,
]

hitboxes = [None]*8

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "toad_a")

