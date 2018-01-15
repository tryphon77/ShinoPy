from genepy import *
from tsprite import TSpriteData

frames_table = [
        [               # frame 0
                [-6, -10, -3, 0x0004, 0x00]
        ],
        [               # frame 1
                [-6, -10, -4, 0x0004, 0x02]
        ],
        [               # frame 2
                [-6, -10, -3, 0x0004, 0x04]
        ],
        [               # frame 3
                [-9, -7, -1, 0x0004, 0x06],
                [-6, -2, -9, 0x0000, 0x08]
        ],
        [               # frame 4
                [-6, -10, -6, 0x0005, 0x09]
        ],
        [               # frame 5
                [-7, -9, -7, 0x0005, 0x0D]
        ],
        [               # frame 6
                [-6, -10, -1, 0x0004, 0x11]
        ],
        [               # frame 7
                [-4, -12, -1, 0x0004, 0x13]
        ],
        [               # frame 8
                [-8, -8, -2, 0x0004, 0x15]
        ],
        [               # frame 9
                [-6, -10, -6, 0x0005, 0x17]
        ],
        [               # frame 10
                [-8, -8, -8, 0x0005, 0x1B]
        ],
        [               # frame 11
                [-14, -10, -6, 0x0009, 0x1F],
                [-9, -7, -14, 0x0004, 0x25]
        ],
        [               # frame 12
                [-12, -12, -12, 0x000A, 0x27]
        ],
        [               # frame 13
                [-12, -12, 6, 0x0008, 0x30],
                [-18, -14, -10, 0x000D, 0x33],
                [-15, -9, -18, 0x0008, 0x3B]
        ],
        [               # frame 14
                [-16, -16, -16, 0x000F, 0x3E]
        ],
        [               # frame 15
                [-17, -15, 10, 0x000C, 0x4E],
                [-22, -10, -14, 0x000E, 0x52],
                [10, -18, -14, 0x0002, 0x5E],
                [-13, -11, -22, 0x0008, 0x61]
        ],
        [               # frame 16
                [-16, -16, 12, 0x000C, 0x64],
                [-20, -12, -12, 0x000E, 0x68],
                [12, -20, -12, 0x0002, 0x74],
                [-16, -16, -20, 0x000C, 0x77]
        ],
        [               # frame 17
                [-5, -11, -2, 0x0004, 0x7B]
        ],
        [               # frame 18
                [-5, -11, 0, 0x0004, 0x7D]
        ],
        [               # frame 19
                [4, -20, -8, 0x0005, 0x7F],
                [-12, -4, 1, 0x0004, 0x83]
        ],
        [               # frame 20
                [-19, -13, 0, 0x000C, 0x85],
                [13, -21, 0, 0x0000, 0x89],
                [-20, 12, -8, 0x0000, 0x8A]
        ],
        [               # frame 21
                [-20, 4, -6, 0x0005, 0x8B],
                [-4, -20, -6, 0x0008, 0x8F]
        ]
]

patterns_blocks = [
        [0x0000, 0x0002],
        [0x0002, 0x0002],
        [0x0004, 0x0002],
        [0x0006, 0x0003],
        [0x0009, 0x0004],
        [0x000D, 0x0004],
        [0x0011, 0x0002],
        [0x0013, 0x0002],
        [0x0015, 0x0002],
        [0x0017, 0x0004],
        [0x001B, 0x0004],
        [0x001F, 0x0008],
        [0x0027, 0x0009],
        [0x0030, 0x000E],
        [0x003E, 0x0010],
        [0x004E, 0x0016],
        [0x0064, 0x0017],
        [0x007B, 0x0002],
        [0x007D, 0x0002],
        [0x007F, 0x0006],
        [0x0085, 0x0006],
        [0x008B, 0x0007]
]

shuriken = [(0, 2), (1, 2), (2, 2)]
shuriken_vanish = [(3, 2), (4, 2), (5, 2)]
bullet = [(17, 6), (18, 6)]
bullet_vanish = [(3, 2), (4, 2), (5, 2)]
blade = [(19, 2), (20, 2), (21, 2)]

animations_table = [
        shuriken,
        shuriken_vanish,
        bullet,
        bullet_vanish,
        blade
]

SHURIKEN = 0
SHURIKEN_VANISH = 1
BULLET = 2
BULLET_VANISH = 3
BLADE = 4

patterns = load_data_from_png('res/chars/projectile_patterns.png')
nb_ptrns = 147


box1 = (-6, -4, 12, 9)
box2 = (-16, -6, 32, 12)

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
	None,	# bounding box 10,
	None,	# bounding box 11,
	None,	# bounding box 12,
	None,	# bounding box 13,
	None,	# bounding box 14,
	None,	# bounding box 15,
	None,	# bounding box 16,
	None,	# bounding box 17,
	None,	# bounding box 18,
	None,	# bounding box 19,
	None,	# bounding box 20,
	None,	# bounding box 21,
]

hitboxes = [
	box1,	# hitbox 0,
	box1,	# hitbox 1,
	box1,	# hitbox 2,
	None,	# hitbox 3,
	None,	# hitbox 4,
	None,	# hitbox 5,
	box1,	# hitbox 6,
	box1,	# hitbox 7,
	box1,	# hitbox 8,
	None,	# hitbox 9,
	None,	# hitbox 10,
	None,	# hitbox 11,
	None,	# hitbox 12,
	None,	# hitbox 13,
	None,	# hitbox 14,
	None,	# hitbox 15,
	None,	# hitbox 16,
	box1,	# hitbox 17,
	box1,	# hitbox 18,
	box2,	# hitbox 19,
	box2,	# hitbox 20,
	box2,	# hitbox 21,
]

sprite_data = TSpriteData(patterns, frames_table, None, animations_table, bounding_boxes, hitboxes, box2, "shuriken")

PROJECTILE_VPOS = 0x480
MORE_VPOS = PROJECTILE_VPOS + 0x92
