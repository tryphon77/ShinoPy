from genepy import load_data_from_png


patterns = load_data_from_png('res/hostage_patterns.png')


frames_table = [
    [       # frame 0
        [-7, -9, -26, 0x0007, 0x00],
        [-15, 7, -10, 0x0001, 0x08]
    ],
    [       # frame 1
        [-5, -11, -26, 0x0007, 0x0A],
        [-13, 5, -10, 0x0001, 0x12]
    ],
    [       # frame 2
        [-15, -9, -14, 0x0009, 0x14],
        [-9, -7, -30, 0x0005, 0x1A]
    ],
    [       # frame 3
        [-14, -10, -15, 0x0009, 0x1E],
        [-8, -8, -31, 0x0005, 0x24]
    ],
    [       # frame 4
        [-12, -12, -23, 0x000A, 0x28],
        [-8, -8, -31, 0x0004, 0x31]
    ],
    [       # frame 5
        [-7, -9, -11, 0x0004, 0x33],
        [-13, -11, -43, 0x000B, 0x35],
        [-16, -8, -51, 0x0008, 0x41]
    ],
    [       # frame 6
        [-9, -7, -34, 0x0006, 0x44],
        [-15, -9, -42, 0x0008, 0x4A],
        [-10, -6, -50, 0x0004, 0x4D]
    ],
    [       # frame 7
        [-8, -8, -41, 0x0006, 0x4F],
        [-8, 0, -57, 0x0001, 0x55],
        [0, -8, -17, 0x0001, 0x57]
    ],
    [       # frame 8
        [-18, -14, -8, 0x000D, 0x59],
        [14, -22, -8, 0x0001, 0x61]
    ],
    [       # frame 9
        [-18, -14, -8, 0x000D, 0x63],
        [14, -22, -8, 0x0001, 0x6B]
    ],
    [       # frame 10
        [-23, -9, -8, 0x000D, 0x6D],
        [9, -25, -8, 0x0005, 0x75]
    ],
    [       # frame 11
        [-24, -8, -9, 0x000E, 0x79],
        [8, -24, -9, 0x0006, 0x85]
    ]
]

patterns_blocks = [
    [0x0000, 0x000A],
    [0x000A, 0x000A],
    [0x0014, 0x000A],
    [0x001E, 0x000A],
    [0x0028, 0x000B],
    [0x0033, 0x0011],
    [0x0044, 0x000B],
    [0x004F, 0x000A],
    [0x0059, 0x000A],
    [0x0063, 0x000A],
    [0x006D, 0x000C],
    [0x0079, 0x0012]
]

wait = [(0, 8), (1, 8), (2, 8), (3, 8), (2, 8), (3, 8), (0, 8), (1, 8), (0, 8), (1, 8), (0, 8), (1, 8)]
free = [(4, 8)]
free_2 = [(5, 8), (6, 4), (7, 4)]
bonus200 = [(8, 1)]
bonus500 = [(9, 1)]
bonus1000 = [(10, 1)]
bonuspow = [(11, 1)]

animations_table = [
    wait,
    free,
	free_2,
    bonus200,
    bonus500,
    bonus1000,
    bonuspow
]

WAIT = 0
FREE = 1
FREE_2 = 2
BONUS200 = 3
BONUS500 = 4
BONUS1000 = 5
BONUSPOW = 6


rect1 = (-12, -28, 24, 29)

bounding_boxes = [
    rect1,        # bounding box 0,
    rect1,        # bounding box 1,
    rect1,        # bounding box 2,
    None,        # bounding box 3,
    None,        # bounding box 4,
    None,        # bounding box 5,
    None,        # bounding box 6,
    None,        # bounding box 8,
    None,        # bounding box 7,
    None,        # bounding box 9,
    None,        # bounding box 10,
    None,        # bounding box 11
]

hitboxes = [None] * 12
