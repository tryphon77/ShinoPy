from genepy import load_data_from_png
from tsprite import TSpriteData


pink_patterns = load_data_from_png('res/chars/pink_guardian_patterns.png')
green_patterns = load_data_from_png('res/chars/green_guardian_patterns.png')

frames_table = [
        [               # frame 0
                [-9, -15, -31, 0x000B, 0x00],
                [-16, -16, -55, 0x000E, 0x0C],
                [-8, -16, -63, 0x0008, 0x18]
        ],
        [               # frame 1
                [-9, -15, -31, 0x000B, 0x1B],
                [-15, -17, -55, 0x000E, 0x27],
                [-8, -16, -63, 0x0008, 0x33]
        ],
        [               # frame 2
                [13, -21, -60, 0x0002, 0x36],
                [5, -13, -55, 0x0003, 0x39],
                [5, -13, -23, 0x0002, 0x3D],
                [-11, -5, -63, 0x0007, 0x40],
                [-11, -5, -31, 0x0007, 0x48],
                [-19, 11, -47, 0x0000, 0x50]
        ],
        [               # frame 3
                [-6, -10, -7, 0x0004, 0x51],
                [-9, -7, -15, 0x0004, 0x53],
                [-14, -10, -31, 0x0009, 0x55],
                [-12, -20, -63, 0x000F, 0x5B]
        ],
        [               # frame 4
                [-20, -12, -23, 0x000E, 0x6B],
                [12, -20, -23, 0x0002, 0x77],
                [-19, -13, -39, 0x000D, 0x7A],
                [13, -21, -39, 0x0001, 0x82],
                [-5, -19, -47, 0x0008, 0x84]
        ],
        [               # frame 5
                [-20, -12, -31, 0x000F, 0x87],
                [-4, -20, -47, 0x0009, 0x97],
                [12, -20, -31, 0x0003, 0x9D],
                [-20, 4, -39, 0x0004, 0xA1]
        ],
        [               # frame 6
                [-10, -22, -47, 0x000F, 0xA3],
                [-18, -14, -15, 0x000D, 0xB3],
                [-18, 10, -39, 0x0002, 0xBB],
                [14, -22, -15, 0x0001, 0xBE]
        ],
        [               # frame 7
                [13, -21, -51, 0x0003, 0xC0],
                [13, -21, -19, 0x0001, 0xC4],
                [5, -13, -50, 0x0003, 0xC6],
                [5, -13, -18, 0x0000, 0xCA],
                [-11, -5, -47, 0x0007, 0xCB],
                [-11, -5, -15, 0x0005, 0xD3],
                [-19, 11, -40, 0x0003, 0xD7],
                [-19, 11, -8, 0x0000, 0xDB]
        ],
        [               # frame 8
                [-20, -12, -55, 0x000F, 0xDC],
                [4, -20, -23, 0x0006, 0xEC],
                [-20, 4, -23, 0x0005, 0xF2],
                [12, -20, -55, 0x0003, 0xF6],
                [-12, -12, -63, 0x0008, 0xFA],
                [-28, 20, -63, 0x0002, 0xFD],
                [-4, -4, -23, 0x0000, 0x100],
                [-20, 12, -7, 0x0000, 0x101]
        ],
        [               # frame 9
                [-23, -9, -7, 0x000C, 0x102],
                [9, -17, -7, 0x0000, 0x106],
                [-13, -11, -15, 0x0008, 0x107],
                [-9, -15, -39, 0x000A, 0x10A],
                [-16, -16, -55, 0x000D, 0x113],
                [-21, -11, -63, 0x000C, 0x11B],
                [-18, 2, -71, 0x0004, 0x11F]
        ],
        [               # frame 10
                [-5, -27, -63, 0x000E, 0x121],
                [-13, -11, -39, 0x000B, 0x12D],
                [11, -27, -71, 0x0004, 0x139],
                [-21, 5, -7, 0x0004, 0x13B],
                [3, -19, -7, 0x0004, 0x13D],
                [-13, 5, -55, 0x0001, 0x13F],
                [11, -19, -39, 0x0000, 0x141]
        ],
        [               # frame 11
                [-15, -17, -54, 0x000E, 0x142],
                [-15, -9, -30, 0x000A, 0x14E],
                [33, -57, -54, 0x0009, 0x157],
                [17, -49, -38, 0x000C, 0x15D],
                [-7, -17, -62, 0x0008, 0x161],
                [-23, 7, -6, 0x0004, 0x164],
                [1, -17, -6, 0x0004, 0x166],
                [41, -49, -62, 0x0000, 0x168]
        ],
        [               # frame 12
                [-13, -19, -55, 0x000F, 0x169],
                [-13, -11, -23, 0x000A, 0x179],
                [3, -19, -63, 0x0004, 0x182],
                [11, -19, -7, 0x0000, 0x184]
        ],
        [               # frame 13
                [-10, -22, -55, 0x000E, 0x185],
                [-10, -14, -31, 0x000B, 0x191],
                [6, -22, -63, 0x0004, 0x19D],
                [14, -22, -7, 0x0000, 0x19F]
        ],
        [               # frame 14
                [-10, -22, -55, 0x000E, 0x1A0],
                [-10, -14, -31, 0x000B, 0x1AC],
                [6, -22, -63, 0x0004, 0x1B8],
                [14, -30, -23, 0x0004, 0x1BA],
                [14, -22, -7, 0x0000, 0x1BC]
        ],
        [               # frame 15
                [-13, -19, -55, 0x000F, 0x1BD],
                [-13, -11, -23, 0x000A, 0x1CD],
                [19, -43, -31, 0x0008, 0x1D6],
                [3, -19, -63, 0x0004, 0x1D9],
                [11, -19, -7, 0x0000, 0x1DB]
        ],
        [               # frame 16
                [-19, -13, -7, 0x000C, 0x1DC],
                [-21, -11, -15, 0x000C, 0x1E0],
                [-20, -12, -31, 0x000D, 0x1E4],
                [-25, -7, -47, 0x000D, 0x1EC],
                [7, -15, -47, 0x0001, 0x1F4],
                [-21, -3, -63, 0x0009, 0x1F6]
        ],
        [               # frame 17
                [-20, -12, -23, 0x000E, 0x1FC],
                [-20, -4, -39, 0x0009, 0x208],
                [12, -20, -31, 0x0002, 0x20E],
                [-20, 12, -47, 0x0000, 0x211],
                [-4, -4, -47, 0x0000, 0x212],
                [-28, 20, -7, 0x0000, 0x213]
        ],
        [               # frame 18
                [-16, -16, -15, 0x000D, 0x214],
                [-16, 0, -23, 0x0004, 0x21C],
                [8, -16, -23, 0x0000, 0x21E],
                [-24, 16, -7, 0x0000, 0x21F]
        ]
]

patterns_blocks = [
        [0x0000, 0x001B],
        [0x001B, 0x001B],
        [0x0036, 0x001B],
        [0x0051, 0x001A],
        [0x006B, 0x001C],
        [0x0087, 0x001C],
        [0x00A3, 0x001D],
        [0x00C0, 0x001C],
        [0x00DC, 0x0026],
        [0x0102, 0x001F],
        [0x0121, 0x0021],
        [0x0142, 0x0027],
        [0x0169, 0x001C],
        [0x0185, 0x001B],
        [0x01A0, 0x001D],
        [0x01BD, 0x001F],
        [0x01DC, 0x0020],
        [0x01FC, 0x0018],
        [0x0214, 0x000C]
]

stand1 = [(0, 6), (1, 6)]
stand2 = [(2, 6), (3, 6)]
walk = [(4, 6), (6, 6), (7, 6), (6, 6)]
block = [(5, 3), (4, 3)]
throw = [(2, 5), (8, 20), (9, 5), (10, 5), (11, 5)]
throw_wait = [(12, 5), (13, 255)]
throw_end = [(14, 5)]
slash = [(8, 20), (9, 3), (10, 3), (11, 3), (15, 3), (14, 30)]
hit = [(4, 1)]
death = [(16, 8), (17, 8), (18, 16)]

animations_table = [
        stand1,
        stand2,
        walk,
        block,
        throw,
        throw_wait,
        throw_end,
        slash,
        hit,
        death
]

STAND1 = 0
STAND2 = 1
WALK = 2
BLOCK = 3
THROW = 4
THROW_WAIT = 5
THROW_END = 6
SLASH = 7
HIT = 8
DEATH = 9

rect0 = (-20, -63, 40, 64)
rect1 = (-16, -47, 32, 48)
rect2 = (-16, -63, 32, 64)

bounding_boxes = [
    rect1,        # bounding box 0,
    rect1,        # bounding box 1,
    rect1,        # bounding box 2,
    rect1,        # bounding box 3,
    rect1,        # bounding box 4,
    rect1,        # bounding box 5,
    rect1,        # bounding box 6,
    rect1,        # bounding box 7,
    rect2,        # bounding box 8,
    rect2,        # bounding box 9,
    rect2,        # bounding box 10,
    rect2,        # bounding box 11,
    rect2,        # bounding box 12,
    rect2,        # bounding box 13,
    rect2,        # bounding box 14,
    rect2,        # bounding box 15,
    None,        # bounding box 16,
    None,        # bounding box 17,
    None,        # bounding box 18,
]

hitboxes = [None] * 19

walk_offsets = [3, 3, 3, 3]
back_walk_offsets = [-3, -3, -3, -3]

sword_box = (20, -48, 10, 48)

pink_sprite_data = TSpriteData(pink_patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "pink guardian")
green_sprite_data = TSpriteData(green_patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "green guardian")
