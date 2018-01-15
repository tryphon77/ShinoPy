from genepy import load_data_from_png
from tsprite import TSpriteData


patterns = load_data_from_png('res/chars/splash_patterns.png')


frames_table = [
        [               # frame 0
                [-20, -12, -7, 0x000C, 0x00],
                [-9, -7, -23, 0x0005, 0x04]
        ],
        [               # frame 1
                [-16, -16, -31, 0x000F, 0x08]
        ],
        [               # frame 2
                [7, -15, -16, 0x0001, 0x18],
                [-1, -7, -23, 0x0002, 0x1A],
                [-9, 1, -16, 0x0001, 0x1D],
                [-17, 9, -10, 0x0000, 0x1F]
        ]
]

patterns_blocks = [
        [0x0000, 0x0008],
        [0x0008, 0x0010],
        [0x0018, 0x0008]
]

splash = [(0, 7), (1, 8), (2, 8)]
short_splash = [(0, 4), (1, 8), (2, 8)]
long_splash = [(0, 4), (1, 8), (2, 8), (0, 4), (1, 8), (2, 4)]

animations_table = [
        splash,
        short_splash,
        long_splash
]

SPLASH = 0
SHORT_SPLASH = 1
LONG_SPLASH = 2

rect0 = (-16, -16, 32, 32)

bounding_boxes = [
	None,
	None,
	None
]

hitboxes = [
	None,
	None,
	None
]

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "splash")
