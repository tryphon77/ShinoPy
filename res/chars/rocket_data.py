from genepy import *
from tsprite import TSpriteData

frames_table = [
        [               # frame 0
                [-12, -12, -1, 0x0008, 0x00]
        ],
        [               # frame 1
                [-12, -12, -2, 0x0008, 0x03]
        ],
        [               # frame 2
                [-10, -6, -2, 0x0004, 0x06],
                [-4, -4, -10, 0x0000, 0x08]
        ],
        [               # frame 3
                [-4, -12, -4, 0x0005, 0x09]
        ],
        [               # frame 4
                [-7, -9, -6, 0x0005, 0x0D]
        ],
        [               # frame 5
                [-7, -9, -6, 0x0005, 0x11]
        ],
        [               # frame 6
                [-12, -12, -4, 0x0009, 0x15],
                [-4, -12, -12, 0x0004, 0x1B]
        ],
        [               # frame 7
                [-11, -21, -19, 0x000F, 0x1D],
                [-27, -5, 13, 0x000C, 0x2D],
                [-19, 11, -11, 0x0002, 0x31],
                [5, -21, 13, 0x0004, 0x34]
        ],
        [               # frame 8
                [-12, -12, -8, 0x000A, 0x36],
                [-12, -4, -16, 0x0004, 0x3F],
                [12, -28, -16, 0x0004, 0x41],
                [-28, 12, -8, 0x0004, 0x43],
                [-20, 12, 8, 0x0001, 0x45],
                [12, -20, 8, 0x0001, 0x47],
                [-12, 4, -24, 0x0000, 0x49],
                [12, -20, -8, 0x0000, 0x4A],
                [-4, -4, 16, 0x0000, 0x4B]
        ],
        [               # frame 9
                [15, -23, -6, 0x0000, 0x4C],
                [5, -13, -8, 0x0001, 0x4D],
                [-1, -7, -15, 0x0002, 0x4F],
                [-9, 1, -6, 0x0001, 0x52],
                [-18, 10, -8, 0x0001, 0x54],
                [-25, 17, -12, 0x0002, 0x56]
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

rocket = [(0, 6), (1, 6)]
ball = [(2, 4), (3, 4)]
explosion = [(4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 3)]

animations_table = [
        rocket,
        ball,
        explosion
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

sprite_data = TSpriteData(patterns, frames_table, None, animations_table, bounding_boxes, hitboxes, box1, "rocket")

