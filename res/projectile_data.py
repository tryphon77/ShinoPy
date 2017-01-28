from genepy import *


frames_table = [
    [       # frame 0
        [-8, -8, -4, 0x0004, 0x00]
    ],
    [       # frame 1
        [-8, -8, -8, 0x0005, 0x02]
    ],
    [       # frame 2
        [-8, -8, -4, 0x0004, 0x06]
    ],
    [       # frame 3
        [-8, -8, -7, 0x0005, 0x08]
    ],
    [       # frame 4
        [-8, -8, -6, 0x0005, 0x0C]
    ],
    [       # frame 5
        [-8, -8, -7, 0x0005, 0x10]
    ],
    [       # frame 6
        [-8, -8, -1, 0x0004, 0x14]
    ],
    [       # frame 7
        [-8, -8, -1, 0x0004, 0x16]
    ],
    [       # frame 8
        [-8, -8, -2, 0x0004, 0x18]
    ],
    [       # frame 9
        [-8, -8, -6, 0x0005, 0x1A]
    ],
    [       # frame 10
        [-8, -8, -8, 0x0005, 0x1E]
    ],
    [       # frame 11
        [-12, -12, -10, 0x000A, 0x22]
    ],
    [       # frame 12
        [-12, -12, -12, 0x000A, 0x2B]
    ],
    [       # frame 13
        [-16, -16, -14, 0x000F, 0x34]
    ],
    [       # frame 14
        [-16, -16, -16, 0x000F, 0x44]
    ],
    [       # frame 15
        [-18, -14, -18, 0x000F, 0x54],
        [14, -22, -18, 0x0003, 0x64],
        [-18, -14, 14, 0x000C, 0x68],
        [14, -22, 14, 0x0000, 0x6C]
    ],
    [       # frame 16
        [-20, -12, -20, 0x000F, 0x6D],
        [12, -20, -20, 0x0003, 0x7D],
        [-20, -12, 12, 0x000C, 0x81],
        [12, -20, 12, 0x0000, 0x85]
    ],
    [       # frame 17
        [-5, -11, -2, 0x0004, 0x86]
    ],
    [       # frame 18
        [-5, -11, 0, 0x0004, 0x88]
    ]
]

shuriken = [(0, 2), (1, 2), (2, 2)]
shuriken_vanish = [(3, 2), (4, 2), (5, 2)]
bullet = [(17, 6), (18, 6)]
bullet_vanish = [(3, 2), (4, 2), (5, 2)]

animations_table = [
    shuriken,
    shuriken_vanish,
    bullet,
    bullet_vanish
]

SHURIKEN = 0
SHURIKEN_VANISH = 1
BULLET = 2
BULLET_VANISH = 3

patterns = load_data_from_png('res/projectile_patterns.png')
nb_ptrns = 0x13E
