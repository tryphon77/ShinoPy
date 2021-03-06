from genepy import load_data_from_png
from tsprite import TSpriteData


patterns = load_data_from_png('res/chars/spider_patterns.png')


frames_table = [
        [               # frame 0
                [-11, -5, 4, 0x0004, 0x00],
                [-19, -13, -12, 0x000D, 0x02],
                [-20, -4, -20, 0x0008, 0x0A],
                [-24, -8, -28, 0x000C, 0x0D],
                [-18, -14, -36, 0x000C, 0x11],
                [-9, -15, -44, 0x0008, 0x15]
        ],
        [               # frame 1
                [-18, -14, -27, 0x000F, 0x18],
                [-25, -7, -35, 0x000C, 0x28],
                [7, -15, -35, 0x0000, 0x2C],
                [-22, -2, -43, 0x0008, 0x2D]
        ],
        [               # frame 2
                [-15, -1, 4, 0x0004, 0x30],
                [-22, -10, -4, 0x000C, 0x32],
                [-18, -14, -12, 0x000C, 0x36],
                [-10, -14, -20, 0x0008, 0x3A],
                [-16, -16, -28, 0x000C, 0x3D],
                [-19, -13, -36, 0x000C, 0x41],
                [-22, -2, -44, 0x0008, 0x45]
        ],
        [               # frame 3
                [-11, -21, -33, 0x000E, 0x48],
                [-3, -13, -41, 0x0004, 0x54],
                [-19, 3, -9, 0x0004, 0x56],
                [5, -21, -9, 0x0004, 0x58],
                [5, -13, -49, 0x0000, 0x5A],
                [21, -29, -33, 0x0000, 0x5B],
                [-19, 11, -17, 0x0000, 0x5C],
                [5, -13, -1, 0x0000, 0x5D]
        ],
        [               # frame 4
                [-5, -11, -11, 0x0005, 0x5E],
                [-12, -12, -19, 0x0008, 0x62],
                [-8, -16, -35, 0x0009, 0x65],
                [-3, -13, -43, 0x0004, 0x6B]
        ],
        [               # frame 5
                [-6, -18, -8, 0x0008, 0x6D],
                [-14, -18, -32, 0x000E, 0x70],
                [-11, -13, -40, 0x0008, 0x7C],
                [4, -12, -48, 0x0000, 0x7F]
        ],
        [               # frame 6
                [-8, -16, -38, 0x000B, 0x80],
                [8, -24, -6, 0x0004, 0x8C],
                [-16, 8, -22, 0x0001, 0x8E],
                [16, -24, -22, 0x0000, 0x90],
                [-8, 0, -6, 0x0000, 0x91]
        ],
        [               # frame 7
                [-13, -19, -23, 0x000E, 0x92],
                [19, -35, -7, 0x0004, 0x9E],
                [11, -19, -31, 0x0000, 0xA0]
        ],
        [               # frame 8
                [-12, -20, -23, 0x000E, 0xA1],
                [4, -20, -31, 0x0004, 0xAD],
                [20, -36, -7, 0x0004, 0xAF],
                [20, -28, -15, 0x0000, 0xB1]
        ],
        [               # frame 9
                [-8, -16, -31, 0x000B, 0xB2],
                [-16, 8, -23, 0x0001, 0xBE]
        ],
        [               # frame 10
                [-7, -17, -23, 0x000A, 0xC0],
                [-3, -13, -31, 0x0004, 0xC9]
        ],
        [               # frame 11
                [-6, -18, -20, 0x000A, 0xCB]
        ],
        [               # frame 12
                [-11, -5, -19, 0x0005, 0xD4]
        ],
        [               # frame 13
                [-14, -10, -20, 0x0009, 0xD8],
                [-14, -2, -28, 0x0004, 0xDE]
        ],
        [               # frame 14
                [-23, -9, -44, 0x000F, 0xE0],
                [-23, -9, -12, 0x000C, 0xF0],
                [9, -17, -36, 0x0003, 0xF4],
                [17, -25, -12, 0x0000, 0xF8]
        ],
        [               # frame 15
                [-14, -10, -33, 0x000A, 0xF9],
                [-30, 14, -41, 0x0004, 0x102],
                [-6, -10, -41, 0x0004, 0x104],
                [10, -26, -33, 0x0004, 0x106],
                [-22, 14, -17, 0x0001, 0x108],
                [10, -18, -17, 0x0001, 0x10A],
                [2, -10, -49, 0x0000, 0x10C],
                [-22, 14, -33, 0x0000, 0x10D],
                [-6, -2, -9, 0x0000, 0x10E]
        ],
        [               # frame 16
                [11, -19, -31, 0x0002, 0x10F],
                [3, -11, -29, 0x0001, 0x112],
                [-5, -3, -33, 0x0002, 0x114],
                [-21, 5, -26, 0x0005, 0x117],
                [-29, 21, -25, 0x0000, 0x11B]
        ]
]

patterns_blocks = [
        [0x0000, 0x0018],
        [0x0018, 0x0018],
        [0x0030, 0x0018],
        [0x0048, 0x0016],
        [0x005E, 0x000F],
        [0x006D, 0x0013],
        [0x0080, 0x0012],
        [0x0092, 0x000F],
        [0x00A1, 0x0011],
        [0x00B2, 0x000E],
        [0x00C0, 0x000B],
        [0x00CB, 0x0009],
        [0x00D4, 0x0004],
        [0x00D8, 0x0008],
        [0x00E0, 0x0019],
        [0x00F9, 0x0016],
        [0x010F, 0x000D]
]

wait = [(0, 1)]
climb = [(1, 10), (2, 10), (1, 10), (0, 10)]
flop = [(3, 10), (4, 10), (5, 10)]
fall = [(6, 1)]
reception = [(7, 6)]
crouch = [(8, 20)]
jump = [(5, 12), (6, 16)]
death1 = [(12, 8), (13, 8), (14, 8), (15, 8), (16, 16)]
death2 = [(9, 7), (10, 2), (11, 15)]

animations_table = [
        wait,
        climb,
        flop,
        fall,
        reception,
        crouch,
        jump,
        death1,
        death2
]

WAIT = 0
CLIMB = 1
FLOP = 2
FALL = 3
RECEPTION = 4
CROUCH = 5
JUMP = 6
DEATH1 = 7
DEATH2 = 8


rect0 = (-20, -40, 36, 64)
rect1 = (-16, -40, 32, 48)
rect2 = (-12, -40, 24, 40)
rect3 = (-12, -32, 24, 32)

bounding_boxes = [
	rect1,
	rect1,
	rect1,
	rect1,
	rect2,
	rect2,
	rect2,
	rect3,
	rect3,
	rect3,
	None,
	None,
	None,
	None,
	None,
	None,
	None,
	None,
	None
]

hitboxes = [None] * 18

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "spider")
