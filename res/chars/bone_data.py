from genepy import load_data_from_png
from tsprite import TSpriteData

patterns = load_data_from_png('res/chars/bone_patterns.png')

frames_table = [
        [               # frame 0
                [-7, -9, -3, 0x0004, 0x00]
        ],
        [               # frame 1
                [-7, -9, -3, 0x0004, 0x02]
        ],
        [               # frame 2
                [-2, -6, -3, 0x0000, 0x04]
        ],
        [               # frame 3
                [-2, -6, -3, 0x0000, 0x05]
        ]
]

patterns_blocks = [
        [0x0000, 0x0002],
        [0x0002, 0x0002],
        [0x0004, 0x0001],
        [0x0005, 0x0001]
]

bone = [(0, 3), (1, 3), (2, 3), (3, 3)]

animations_table = [
        bone
]

BONE = 0


rect0 = (-8, -4, 16, 8)
rect1 = (-4, -2, 8, 4)

bounding_boxes = [
    rect1,    # bounding box 0,
    rect1,    # bounding box 1,
    rect1,    # bounding box 2,
    rect1,    # bounding box 3,
]

hitboxes = [None]*4

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, rect0, "bone")
