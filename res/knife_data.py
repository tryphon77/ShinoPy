from genepy import load_data_from_png


patterns = load_data_from_png('res/knife_patterns.png')

frames_table = [
    [       # frame 0
        [-13, -3, -7, 0x0004, 0x00],
        [-12, -12, -15, 0x0008, 0x02],
        [-4, -12, -23, 0x0004, 0x05],
        [-8, -8, -31, 0x0004, 0x07],
        [-9, -15, -55, 0x000A, 0x09],
        [-1, -15, -63, 0x0004, 0x12]
    ],
    [       # frame 1
        [-5, -19, -58, 0x000B, 0x14],
        [-5, -19, -26, 0x0009, 0x20],
        [-21, -11, -10, 0x000C, 0x26],
        [-13, 5, -50, 0x0001, 0x2A],
        [19, -27, -42, 0x0000, 0x2C],
        [-13, 5, -18, 0x0000, 0x2D],
        [-21, 13, -2, 0x0000, 0x2E],
        [3, -11, -2, 0x0000, 0x2F]
    ],
    [       # frame 2
        [-20, -12, -7, 0x000C, 0x30],
        [-24, -8, -15, 0x000C, 0x34],
        [8, -16, -15, 0x0000, 0x38],
        [-7, -17, -31, 0x0009, 0x39],
        [-11, -21, -47, 0x000D, 0x3F],
        [-9, -15, -55, 0x0008, 0x47],
        [-1, -15, -63, 0x0004, 0x4A]
    ],
    [       # frame 3
        [-17, -15, -23, 0x000E, 0x4C],
        [-9, -15, -31, 0x0008, 0x58],
        [15, -23, -23, 0x0001, 0x5B],
        [7, -15, -39, 0x0000, 0x5D]
    ],
    [       # frame 4
        [-19, -13, -7, 0x000C, 0x5E],
        [-22, -10, -15, 0x000C, 0x62],
        [10, -18, -15, 0x0000, 0x66],
        [-14, -18, -23, 0x000C, 0x67],
        [-10, -14, -31, 0x0008, 0x6B],
        [4, -12, -39, 0x0000, 0x6E]
    ],
    [       # frame 5
        [-14, -10, -31, 0x000B, 0x6F],
        [10, -18, -23, 0x0001, 0x7B],
        [-6, -2, -39, 0x0000, 0x7D]
    ],
    [       # frame 6
        [-13, -11, -7, 0x0008, 0x7E],
        [-12, -12, -15, 0x0008, 0x81],
        [-17, -15, -39, 0x000E, 0x84],
        [-3, -13, -47, 0x0004, 0x90]
    ],
    [       # frame 7
        [-9, -7, -15, 0x0005, 0x92],
        [-11, -13, -31, 0x0009, 0x96],
        [-18, -14, -47, 0x000D, 0x9C],
        [-16, -8, -55, 0x0008, 0xA4],
        [-1, -7, -63, 0x0000, 0xA7]
    ],
    [       # frame 8
        [-17, -15, -47, 0x000F, 0xA8],
        [-17, -7, -55, 0x0008, 0xB8],
        [-9, -15, -15, 0x0008, 0xBB],
        [15, -31, -31, 0x0004, 0xBE],
        [-1, -7, -63, 0x0000, 0xC0],
        [15, -23, -23, 0x0000, 0xC1],
        [-9, 1, -7, 0x0000, 0xC2],
        [7, -15, -7, 0x0000, 0xC3]
    ],
    [       # frame 9
        [-16, -8, -49, 0x000B, 0xC4],
        [8, -40, -49, 0x000C, 0xD0],
        [8, -16, -33, 0x0003, 0xD4],
        [-16, -8, -57, 0x0008, 0xD8],
        [-8, 0, -17, 0x0002, 0xDB],
        [16, -24, -25, 0x0000, 0xDE],
        [0, -8, -17, 0x0000, 0xDF]
    ],
    [       # frame 10
        [-10, -14, -31, 0x000B, 0xE0],
        [-14, -18, -39, 0x000C, 0xEC],
        [1, -17, -47, 0x0004, 0xF0]
    ],
    [       # frame 11
        [-10, -22, -7, 0x000C, 0xF2],
        [-7, -25, -23, 0x000D, 0xF6],
        [6, -14, -31, 0x0000, 0xFE]
    ]
]

patterns_blocks = [
    [0x0000, 0x0014],
    [0x0014, 0x001C],
    [0x0030, 0x001C],
    [0x004C, 0x0012],
    [0x005E, 0x0011],
    [0x006F, 0x000F],
    [0x007E, 0x0014],
    [0x0092, 0x0016],
    [0x00A8, 0x001C],
    [0x00C4, 0x001C],
    [0x00E0, 0x0012],
    [0x00F2, 0x000D]
]

walk = [(0, 7), (1, 7), (2, 7)]
stab_stand = [(7, 4), (8, 10), (7, 5), (1, 7)]
hit = [(6, 1)]
turn = [(5, 7), (3, 7)]
ready_to_jump = [(6, 6)]
jump = [(7, 1)]
end_of_jump = [(6, 6), (3, 8)]
stab_jump = [(9, 10)]
waiting = [(3, 16), (4, 16)]
death = [(6, 7), (10, 8), (11, 16)]

animations_table = [
    walk,
    stab_stand,
    hit,
    turn,
    ready_to_jump,
    jump,
    end_of_jump,
    stab_jump,
    waiting,
    death
]

WALK = 0
STAB_STAND = 1
HIT = 2
TURN = 3
READY_TO_JUMP = 4
JUMP = 5
END_OF_JUMP = 6
STAB_JUMP = 7
WAITING = 8
DEATH = 9
