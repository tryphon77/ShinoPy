from genepy import load_data_from_png
from tsprite import TSpriteData

patterns = load_data_from_png('res/chars/bird_patterns.png')


frames_table = [
        [               # frame 0
                [-8, -8, -31, 0x0007, 0x00],
                [-16, 8, -15, 0x0001, 0x08],
                [8, -16, -23, 0x0000, 0x0A]
        ],
        [               # frame 1
                [-8, -8, -31, 0x0007, 0x0B],
                [-16, 8, -31, 0x0001, 0x13],
                [8, -16, -23, 0x0000, 0x15],
                [-16, 8, -7, 0x0000, 0x16]
        ],
        [               # frame 2
                [-23, -1, -7, 0x0008, 0x17],
                [-10, -6, -15, 0x0004, 0x1A],
                [-20, -12, -23, 0x000C, 0x1C],
                [-16, -8, -31, 0x0008, 0x20]
        ],
        [               # frame 3
                [-16, -8, -28, 0x000A, 0x23],
                [-16, 0, -4, 0x0004, 0x2C],
                [8, -16, -28, 0x0000, 0x2E]
        ],
        [               # frame 4
                [4, -12, -27, 0x0001, 0x2F],
                [-12, -4, -31, 0x0007, 0x31],
                [-20, 12, -19, 0x0000, 0x39]
        ],
        [               # frame 5
                [4, -12, -28, 0x0001, 0x3A],
                [-12, -4, -31, 0x0007, 0x3C],
                [-20, 12, -28, 0x0001, 0x44]
        ],
        [               # frame 6
                [2, -10, -36, 0x0003, 0x46],
                [-14, -2, -31, 0x0007, 0x4A],
                [-22, 14, -37, 0x0000, 0x52]
        ],
        [               # frame 7
                [-11, -5, -15, 0x0005, 0x53],
                [-17, -7, -23, 0x0008, 0x57],
                [-21, -11, -31, 0x000C, 0x5A]
        ],
        [               # frame 8
                [-16, -8, -31, 0x000A, 0x5E],
                [-8, -8, -7, 0x0004, 0x67],
                [-24, 16, -31, 0x0000, 0x69]
        ],
        [               # frame 9
                [-12, -4, -7, 0x0004, 0x6A],
                [-8, -8, -15, 0x0004, 0x6C],
                [-14, -10, -23, 0x0008, 0x6E],
                [-16, -8, -31, 0x0008, 0x71]
        ],
        [               # frame 10
                [-18, -14, -30, 0x000F, 0x74]
        ],
        [               # frame 11
                [-18, -14, -23, 0x000E, 0x84],
                [-2, -14, -31, 0x0004, 0x90],
                [-18, 10, -31, 0x0000, 0x92]
        ],
        [               # frame 12
                [-17, -7, -20, 0x0009, 0x93],
                [-17, 1, -4, 0x0004, 0x99],
                [7, -15, -28, 0x0000, 0x9B],
                [7, -15, -12, 0x0000, 0x9C]
        ],
        [               # frame 13
                [-6, -2, -7, 0x0000, 0x9D]
        ]
]

patterns_blocks = [
        [0x0000, 0x000B],
        [0x000B, 0x000C],
        [0x0017, 0x000C],
        [0x0023, 0x000C],
        [0x002F, 0x000B],
        [0x003A, 0x000C],
        [0x0046, 0x000D],
        [0x0053, 0x000B],
        [0x005E, 0x000C],
        [0x006A, 0x000A],
        [0x0074, 0x0010],
        [0x0084, 0x000F],
        [0x0093, 0x000A],
        [0x009D, 0x0001]
]

fly = [(0, 8), (1, 8), (2, 8), (3, 8)]
fall = [(4, 8), (5, 8), (6, 8), (7, 8)]
turn_down = [(8, 8), (9, 8)]
turn_up = [(9, 8), (8, 8)]
hit = [(10, 1)]
death = [(10, 8), (11, 10), (12, 10), (13, 10)]

animations_table = [
        fly,
        fall,
        turn_down,
        turn_up,
        hit,
        death
]

FLY = 0
FALL = 1
TURN_DOWN = 2
TURN_UP = 3
HIT = 4
DEATH = 5


rect0 = (-16, -31, 32, 32)
rect1 = (-12, -29, 24, 30)

bounding_boxes = [
    rect1,    # bounding box 0,
    rect1,    # bounding box 1,
    rect1,    # bounding box 2,
    rect1,    # bounding box 3,
    rect1,    # bounding box 4,
    rect1,    # bounding box 5,
    rect1,    # bounding box 6,
    rect1,    # bounding box 7,
    rect1,    # bounding box 8,
    rect1,    # bounding box 9,
    None,    # bounding box 10,
    None,    # bounding box 11,
    None,    # bounding box 12,
    None,    # bounding box 13,
]

hitboxes = [None]*14

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "bird")
