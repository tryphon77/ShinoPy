frames_table = [
        [               # frame 0
                [-5, -19, -1, 0x0008, 0x00]
        ],
        [               # frame 1
                [-5, -19, -2, 0x0008, 0x03]
        ],
        [               # frame 2
                [-10, -6, -2, 0x0004, 0x06],
                [-4, -4, -10, 0x0000, 0x08]
        ],
        [               # frame 3
                [-4, -12, -4, 0x0005, 0x09]
        ],
        [               # frame 4
                [-6, -10, -6, 0x0005, 0x0D]
        ],
        [               # frame 5
                [-6, -10, -6, 0x0005, 0x11]
        ],
        [               # frame 6
                [-11, -13, -4, 0x0009, 0x15],
                [-11, -5, -12, 0x0004, 0x1B]
        ],
        [               # frame 7
                [-20, -12, -19, 0x000F, 0x1D],
                [-20, -12, 13, 0x000C, 0x2D],
                [12, -20, -11, 0x0003, 0x31],
                [20, -28, 13, 0x0000, 0x35]
        ],
        [               # frame 8
                [-11, -13, -8, 0x000A, 0x36],
                [-27, 11, -16, 0x0004, 0x3F],
                [-3, -13, -16, 0x0004, 0x41],
                [13, -29, -8, 0x0004, 0x43],
                [-19, 11, 8, 0x0001, 0x45],
                [13, -21, 8, 0x0001, 0x47],
                [5, -13, -24, 0x0000, 0x49],
                [-19, 11, -8, 0x0000, 0x4A],
                [-3, -5, 16, 0x0000, 0x4B]
        ],
        [               # frame 9
                [15, -23, -12, 0x0002, 0x4C],
                [7, -15, -10, 0x0001, 0x4F],
                [-1, -7, -14, 0x0002, 0x51],
                [-17, 1, -7, 0x0005, 0x54],
                [-25, 17, -6, 0x0000, 0x58]
        ]
]

patterns_blocks = [
        [0x0000, 0x0003],
        [0x0003, 0x0003],
        [0x0006, 0x0003],
        [0x0009, 0x0004],
        [0x000D, 0x0004],
        [0x0011, 0x0004],
        [0x0015, 0x0008],
        [0x001D, 0x0019],
        [0x0036, 0x0016],
        [0x004C, 0x000D]
]

ROCKET = [(0, 6), (1, 6)]
BALL = [(2, 4), (3, 4)]
EXPLOSION = [(4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 3)]

animations_table = [
        ROCKET,
        BALL,
        EXPLOSION
]

ROCKET = 0
BALL = 1
EXPLOSION = 2

patterns = load_data_from_png('res/chars/rocket_patterns.png')
nb_ptrns = 89


box1 = (-5, -1, 10, 3)
box2 = (-4, -4, 9, 0)

bounding_boxes = [
	None,	# bounding box 0,
	None,	# bounding box 1,
	None,	# bounding box 2,
	None,	# bounding box 3,
	None,	# bounding box 4,
	None,	# bounding box 5,
	None,	# bounding box 6,
	None,	# bounding box 7,
	None,	# bounding box 8,
	None,	# bounding box 9,
]

hitboxes = [
	box1,	# hitbox 0,
	box1,	# hitbox 1,
	box2,	# hitbox 2,
	box2,	# hitbox 3,
	None,	# hitbox 4,
	None,	# hitbox 5,
	box1,	# hitbox 6,
	box1,	# hitbox 7,
	box1,	# hitbox 8,
	None,	# hitbox 9,
	None,	# hitbox 10,
]

sprite_data = TSpriteData(patterns, frames_table, None, animations_table, bounding_boxes, hitboxes, "rocket")

