from genepy import *


frames_table = [
	[		# frame 0
		[-40, 24, -36, 0x0004, 0x02]
	],
	[		# frame 1
		[-40, 24, -40, 0x0005, 0x06]
	],
	[		# frame 2
		[-40, 24, -36, 0x0004, 0x08]
	],
	[		# frame 3
		[-40, 24, -39, 0x0005, 0x0C]
	],
	[		# frame 4
		[-40, 24, -38, 0x0005, 0x10]
	],
	[		# frame 5
		[-40, 24, -39, 0x0005, 0x14]
	],
	[		# frame 6
		[-40, 24, -33, 0x0004, 0x16]
	],
	[		# frame 7
		[-40, 24, -33, 0x0004, 0x18]
	],
	[		# frame 8
		[-40, 24, -34, 0x0004, 0x1A]
	],
	[		# frame 9
		[-40, 24, -38, 0x0005, 0x1E]
	],
	[		# frame 10
		[-40, 24, -40, 0x0005, 0x22]
	],
	[		# frame 11
		[-44, 20, -42, 0x000A, 0x2B]
	],
	[		# frame 12
		[-44, 20, -44, 0x000A, 0x34]
	],
	[		# frame 13
		[-48, 16, -46, 0x000F, 0x44]
	],
	[		# frame 14
		[-48, 16, -48, 0x000F, 0x54]
	],
	[		# frame 15
		[-50, 18, -50, 0x000F, 0x64],
		[-18, 10, -50, 0x0003, 0x68],
		[-50, 18, -18, 0x000C, 0x6C],
		[-18, 10, -18, 0x0000, 0x6D]
	],
	[		# frame 16
		[-52, 20, -52, 0x000F, 0x7D],
		[-20, 12, -52, 0x0003, 0x81],
		[-52, 20, -20, 0x000C, 0x85],
		[-20, 12, -20, 0x0000, 0x86]
	],
	[		# frame 17
		[-37, 21, -34, 0x0004, 0x88]
	],
	[		# frame 18
		[-37, 21, -32, 0x0004, 0x8A]
	]
]

shuriken = [(0, 2), (1, 2), (2, 2), (-1, 0)]
shuriken_vanish = [(3, 2), (4, 2), (5, 2), (-1, 0)]
bullet = [(17, 6), (18, 6), (-1, 0)]
bullet_vanish = [(3, 2), (4, 2), (5, 2), (-1, 0)]

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
