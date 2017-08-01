from genepy import load_data_from_png
from tsprite import TSpriteData


patterns = load_data_from_png('res/chars/musashi_patterns.png')

frames_table = [
    [       # frame 0
        [-5, -11, -56, 0x0007, 0x08],
        [-5, -11, -24, 0x0005, 0x0C],
        [-13, -3, -8, 0x0004, 0x0E],
        [-13, 5, -48, 0x0001, 0x10],
        [11, -19, -40, 0x0001, 0x12],
        [3, -11, -64, 0x0000, 0x13]
    ],
    [       # frame 1
        [-10, -6, -8, 0x0004, 0x15],
        [-12, -12, -24, 0x0009, 0x1B],
        [-7, -9, -32, 0x0004, 0x1D],
        [-11, -13, -40, 0x0008, 0x20],
        [-8, -8, -48, 0x0004, 0x22],
        [-5, -11, -56, 0x0004, 0x24],
        [2, -10, -64, 0x0000, 0x25]
    ],
    [       # frame 2
        [-17, -15, -16, 0x000D, 0x2D],
        [-12, -12, -24, 0x0008, 0x30],
        [-7, -17, -40, 0x0009, 0x36],
        [-8, -8, -48, 0x0004, 0x38],
        [-5, -11, -56, 0x0004, 0x3A],
        [2, -10, -64, 0x0000, 0x3B]
    ],
    [       # frame 3
        [-13, -3, -8, 0x0004, 0x3D],
        [-5, -11, -24, 0x0005, 0x41],
        [-7, -17, -40, 0x0009, 0x47],
        [-8, -8, -48, 0x0004, 0x49],
        [-5, -11, -64, 0x0005, 0x4D]
    ],
    [       # frame 4
        [-10, -6, -8, 0x0004, 0x4F],
        [-10, -14, -40, 0x000B, 0x5B],
        [-8, -8, -48, 0x0004, 0x5D],
        [-5, -11, -56, 0x0004, 0x5F],
        [2, -10, -64, 0x0000, 0x60]
    ],
    [       # frame 5
        [-12, -12, -43, 0x000B, 0x6C],
        [-4, -12, -59, 0x0005, 0x70],
        [-20, 4, -11, 0x0004, 0x72],
        [4, -20, -3, 0x0004, 0x74],
        [12, -20, -35, 0x0000, 0x75],
        [4, -12, -11, 0x0000, 0x76],
        [-12, 4, -3, 0x0000, 0x77]
    ],
    [       # frame 6
        [-7, -9, -16, 0x0005, 0x7B],
        [-6, -10, -32, 0x0005, 0x7F],
        [-4, -12, -40, 0x0004, 0x81],
        [-11, -13, -48, 0x0008, 0x84],
        [-7, -9, -56, 0x0004, 0x86],
        [-1, -7, -64, 0x0000, 0x87]
    ],
    [       # frame 7
        [-10, -6, -8, 0x0004, 0x89],
        [-12, -12, -24, 0x0009, 0x8F],
        [-7, -9, -32, 0x0004, 0x91],
        [-11, -13, -48, 0x0009, 0x97],
        [-7, -9, -56, 0x0004, 0x99],
        [-1, -7, -64, 0x0000, 0x9A]
    ],
    [       # frame 8
        [-9, -15, -56, 0x000B, 0xA6],
        [-9, -15, -24, 0x0009, 0xAC],
        [-1, -15, -8, 0x0004, 0xAE],
        [-17, 9, -16, 0x0001, 0xB0]
    ],
    [       # frame 9
        [-13, -3, -8, 0x0004, 0xB2],
        [-5, -11, -32, 0x0006, 0xB8],
        [-4, -12, -40, 0x0004, 0xBA],
        [-11, -13, -48, 0x0008, 0xBD],
        [-7, -9, -56, 0x0004, 0xBF],
        [-1, -7, -64, 0x0000, 0xC0]
    ],
    [       # frame 10
        [-10, -6, -8, 0x0004, 0xC2],
        [-10, -14, -40, 0x000B, 0xCE],
        [-11, -13, -48, 0x0008, 0xD1],
        [-7, -9, -56, 0x0004, 0xD3],
        [-1, -7, -64, 0x0000, 0xD4]
    ],
    [       # frame 11
        [-17, -15, -8, 0x000C, 0xD8],
        [-13, -11, -16, 0x0008, 0xDB],
        [-12, -12, -24, 0x0008, 0xDE],
        [-7, -9, -32, 0x0004, 0xE0],
        [-11, -13, -48, 0x0009, 0xE6],
        [-7, -9, -56, 0x0004, 0xE8]
    ],
    [       # frame 12
        [-13, -11, -24, 0x000A, 0xF1],
        [-7, -9, -32, 0x0004, 0xF3],
        [-27, -5, -40, 0x000C, 0xF7],
        [5, -21, -40, 0x0004, 0xF9],
        [-16, -16, -48, 0x000C, 0xFD],
        [-16, -8, -56, 0x0008, 0x100],
        [-3, -5, -64, 0x0000, 0x101]
    ],
    [       # frame 13
        [-9, -7, -24, 0x0006, 0x107],
        [-14, -10, -56, 0x000B, 0x113],
        [-3, -5, -64, 0x0000, 0x114]
    ],
    [       # frame 14
        [-7, -9, -24, 0x0006, 0x11A],
        [-12, -12, -56, 0x000B, 0x126],
        [-4, -4, -64, 0x0000, 0x127]
    ],
    [       # frame 15
        [-9, -7, -24, 0x0006, 0x12D],
        [-10, -14, -48, 0x000A, 0x136],
        [-15, -9, -56, 0x0008, 0x139],
        [-3, -5, -64, 0x0000, 0x13A]
    ],
    [       # frame 16
        [-9, -7, -24, 0x0006, 0x140],
        [-12, -12, -56, 0x000B, 0x14C],
        [-4, -4, -64, 0x0000, 0x14D]
    ],
    [       # frame 17
        [-21, -11, -8, 0x000C, 0x151],
        [11, -27, -8, 0x0004, 0x153],
        [-15, -17, -24, 0x000D, 0x15B],
        [-9, -15, -32, 0x0008, 0x15E]
    ],
    [       # frame 18
        [-12, -12, -16, 0x0009, 0x164],
        [-14, -18, -24, 0x000C, 0x168],
        [-3, -13, -32, 0x0004, 0x16A]
    ],
    [       # frame 19
        [-21, -11, -8, 0x000C, 0x16E],
        [-19, -13, -16, 0x000C, 0x172],
        [-10, -14, -32, 0x0009, 0x178],
        [5, -13, -40, 0x0000, 0x179]
    ],
    [       # frame 20
        [-21, -11, -8, 0x000C, 0x17D],
        [11, -27, -8, 0x0004, 0x17F],
        [-15, -17, -16, 0x000C, 0x183],
        [-12, -12, -32, 0x0009, 0x189],
        [2, -10, -40, 0x0000, 0x18A]
    ],
    [       # frame 21
        [-12, -12, -32, 0x000B, 0x196],
        [2, -10, -40, 0x0000, 0x197]
    ],
    [       # frame 22
        [-21, -11, -8, 0x000C, 0x19B],
        [-19, -13, -16, 0x000C, 0x19F],
        [-12, -12, -32, 0x0009, 0x1A5],
        [3, -11, -40, 0x0000, 0x1A6]
    ],
    [       # frame 23
        [-11, -21, -24, 0x000E, 0x1B2],
        [-11, -13, -32, 0x0008, 0x1B5],
        [5, -13, -40, 0x0000, 0x1B6],
        [21, -29, -24, 0x0000, 0x1B7],
        [-19, 11, -8, 0x0000, 0x1B8],
        [21, -29, -8, 0x0000, 0x1B9]
    ],
    [       # frame 24
        [12, -28, -27, 0x0004, 0x1BB],
        [4, -12, -40, 0x0003, 0x1BF],
        [4, -12, -8, 0x0000, 0x1C0],
        [-4, -4, -32, 0x0003, 0x1C4],
        [-12, 4, -24, 0x0002, 0x1C7]
    ],
    [       # frame 25
        [-21, -11, -8, 0x000C, 0x1CB],
        [-19, -13, -16, 0x000C, 0x1CF],
        [-12, -20, -24, 0x000C, 0x1D3],
        [20, -28, -24, 0x0000, 0x1D4],
        [-5, -19, -32, 0x0008, 0x1D7],
        [3, -11, -40, 0x0000, 0x1D8]
    ],
    [       # frame 26
        [-21, -11, -8, 0x000C, 0x1DC],
        [11, -27, -8, 0x0004, 0x1DE],
        [-15, -17, -24, 0x000D, 0x1E6],
        [-12, -12, -32, 0x0008, 0x1E9],
        [2, -10, -40, 0x0000, 0x1EA]
    ],
    [       # frame 27
        [-11, -13, -32, 0x000B, 0x1F6],
        [5, -13, -40, 0x0000, 0x1F7],
        [13, -21, -24, 0x0000, 0x1F8]
    ],
    [       # frame 28
        [-21, -11, -8, 0x000C, 0x1FC],
        [-15, -17, -24, 0x000D, 0x204],
        [-7, -17, -32, 0x0008, 0x207],
        [3, -11, -40, 0x0000, 0x208]
    ],
    [       # frame 29
        [-5, -11, -40, 0x0007, 0x210],
        [-5, -19, -56, 0x0009, 0x216],
        [19, -35, -48, 0x0004, 0x218],
        [-13, -3, -8, 0x0004, 0x21A],
        [3, -11, -64, 0x0000, 0x21B]
    ],
    [       # frame 30
        [-10, -6, -8, 0x0004, 0x21D],
        [-12, -12, -24, 0x0009, 0x223],
        [-7, -9, -40, 0x0005, 0x227],
        [-10, -22, -48, 0x000C, 0x22B],
        [22, -30, -48, 0x0000, 0x22C],
        [-5, -19, -56, 0x0008, 0x22F],
        [2, -10, -64, 0x0000, 0x230]
    ],
    [       # frame 31
        [-17, -15, -16, 0x000D, 0x238],
        [-12, -12, -24, 0x0008, 0x23B],
        [-6, -10, -40, 0x0005, 0x23F],
        [-10, -22, -48, 0x000C, 0x243],
        [22, -30, -48, 0x0000, 0x244],
        [-5, -11, -56, 0x0004, 0x246],
        [1, -9, -64, 0x0000, 0x247]
    ],
    [       # frame 32
        [-5, -11, -40, 0x0007, 0x24F],
        [-5, -19, -56, 0x0009, 0x255],
        [19, -35, -48, 0x0004, 0x257],
        [-13, -3, -8, 0x0004, 0x259],
        [3, -11, -64, 0x0000, 0x25A]
    ],
    [       # frame 33
        [-10, -6, -8, 0x0004, 0x25C],
        [-10, -14, -32, 0x000A, 0x265],
        [-7, -9, -40, 0x0004, 0x267],
        [-10, -22, -48, 0x000C, 0x26B],
        [22, -30, -48, 0x0000, 0x26C],
        [-5, -19, -56, 0x0008, 0x26F],
        [2, -10, -64, 0x0000, 0x270]
    ],
    [       # frame 34
        [-17, -15, -8, 0x000C, 0x274],
        [-13, -11, -16, 0x0008, 0x277],
        [-12, -12, -24, 0x0008, 0x27A],
        [-6, -10, -40, 0x0005, 0x27E],
        [-10, -22, -48, 0x000C, 0x282],
        [22, -30, -48, 0x0000, 0x283],
        [-5, -11, -56, 0x0004, 0x285],
        [1, -9, -64, 0x0000, 0x286]
    ],
    [       # frame 35
        [-7, -9, -16, 0x0005, 0x28A],
        [-6, -10, -32, 0x0005, 0x28E],
        [-4, -12, -40, 0x0004, 0x290],
        [-9, -15, -48, 0x0008, 0x293],
        [-7, -9, -56, 0x0004, 0x295],
        [-1, -7, -64, 0x0000, 0x296]
    ],
    [       # frame 36
        [-10, -6, -8, 0x0004, 0x298],
        [-12, -12, -24, 0x0009, 0x29E],
        [-7, -9, -32, 0x0004, 0x2A0],
        [-9, -15, -48, 0x0009, 0x2A6],
        [-7, -9, -56, 0x0004, 0x2A8],
        [-1, -7, -64, 0x0000, 0x2A9]
    ],
    [       # frame 37
        [-9, -15, -56, 0x000B, 0x2B5],
        [-9, -15, -24, 0x0009, 0x2BB],
        [-1, -15, -8, 0x0004, 0x2BD],
        [-17, 9, -16, 0x0001, 0x2BF]
    ],
    [       # frame 38
        [-13, -3, -8, 0x0004, 0x2C1],
        [-5, -11, -32, 0x0006, 0x2C7],
        [-4, -12, -40, 0x0004, 0x2C9],
        [-9, -15, -48, 0x0008, 0x2CC],
        [-7, -9, -56, 0x0004, 0x2CE],
        [-1, -7, -64, 0x0000, 0x2CF]
    ],
    [       # frame 39
        [-10, -6, -8, 0x0004, 0x2D1],
        [-10, -14, -40, 0x000B, 0x2DD],
        [-9, -15, -48, 0x0008, 0x2E0],
        [-7, -9, -56, 0x0004, 0x2E2],
        [-1, -7, -64, 0x0000, 0x2E3]
    ],
    [       # frame 40
        [-17, -15, -8, 0x000C, 0x2E7],
        [-13, -11, -16, 0x0008, 0x2EA],
        [-12, -12, -24, 0x0008, 0x2ED],
        [-7, -9, -32, 0x0004, 0x2EF],
        [-9, -15, -48, 0x0009, 0x2F5],
        [-7, -9, -56, 0x0004, 0x2F7]
    ],
    [       # frame 41
        [-14, -2, -9, 0x0004, 0x2F9],
        [-8, -8, -17, 0x0004, 0x2FB],
        [-15, -9, -25, 0x0008, 0x2FE],
        [-20, -12, -33, 0x000C, 0x302],
        [-11, -13, -41, 0x0008, 0x305],
        [-2, -14, -49, 0x0004, 0x307]
    ],
    [       # frame 42
        [-6, -10, -17, 0x0005, 0x30B],
        [-13, -11, -25, 0x0008, 0x30E],
        [-20, -12, -33, 0x000C, 0x312],
        [-11, -13, -41, 0x0008, 0x315],
        [-2, -14, -49, 0x0004, 0x317]
    ],
    [       # frame 43
        [-14, -2, -9, 0x0004, 0x319],
        [-8, -8, -17, 0x0004, 0x31B],
        [-15, -9, -33, 0x0009, 0x321],
        [-11, -21, -41, 0x000C, 0x325],
        [21, -29, -41, 0x0000, 0x326],
        [-5, -11, -49, 0x0004, 0x328],
        [1, -9, -57, 0x0000, 0x329]
    ],
    [       # frame 44
        [-6, -10, -17, 0x0005, 0x32D],
        [-13, -11, -33, 0x0009, 0x333],
        [-11, -21, -41, 0x000C, 0x337],
        [21, -29, -41, 0x0000, 0x338],
        [-5, -11, -49, 0x0004, 0x33A],
        [1, -9, -57, 0x0000, 0x33B]
    ],
    [       # frame 45
        [-14, -2, -9, 0x0004, 0x33D],
        [-8, -8, -17, 0x0004, 0x33F],
        [-14, -10, -33, 0x0009, 0x345],
        [-11, -13, -41, 0x0008, 0x348],
        [-4, -12, -57, 0x0005, 0x34C]
    ],
    [       # frame 46
        [-6, -10, -17, 0x0005, 0x350],
        [-13, -11, -33, 0x0009, 0x356],
        [-11, -13, -49, 0x0009, 0x35C],
        [-4, -12, -57, 0x0004, 0x35E]
    ],
    [       # frame 47
        [-14, -2, -9, 0x0004, 0x360],
        [-8, -8, -17, 0x0004, 0x362],
        [-15, -9, -25, 0x0008, 0x365],
        [-17, -15, -33, 0x000C, 0x369],
        [-12, -20, -41, 0x000C, 0x36D],
        [-3, -13, -49, 0x0004, 0x36F],
        [3, -11, -57, 0x0000, 0x370]
    ],
    [       # frame 48
        [-6, -10, -17, 0x0005, 0x374],
        [-13, -11, -25, 0x0008, 0x377],
        [-17, -15, -33, 0x000C, 0x37B],
        [-12, -20, -41, 0x000C, 0x37F],
        [-3, -13, -49, 0x0004, 0x381],
        [3, -11, -57, 0x0000, 0x382]
    ],
    [       # frame 49
        [41, -57, -16, 0x0004, 0x384],
        [25, -41, -23, 0x0005, 0x388],
        [9, -25, -32, 0x0006, 0x38E],
        [-7, -9, -36, 0x0006, 0x394],
        [-15, 7, -25, 0x0001, 0x396],
        [-23, 15, -16, 0x0000, 0x397]
    ],
    [       # frame 50
        [19, -27, -16, 0x0001, 0x399],
        [11, -19, -35, 0x0003, 0x39D],
        [3, -11, -43, 0x0003, 0x3A1],
        [3, -11, -11, 0x0000, 0x3A2],
        [-5, -3, -41, 0x0003, 0x3A6],
        [-13, 5, -19, 0x0001, 0x3A8],
        [-21, 13, -10, 0x0000, 0x3A9]
    ],
    [       # frame 51
        [-6, -10, -17, 0x0005, 0x3AD],
        [-13, -11, -33, 0x0009, 0x3B3],
        [-17, -15, -41, 0x000C, 0x3B7],
        [-9, -15, -49, 0x0008, 0x3BA],
        [4, -20, -57, 0x0004, 0x3BC]
    ],
    [       # frame 52
        [-6, -10, -17, 0x0005, 0x3C0],
        [-13, -11, -33, 0x0009, 0x3C6],
        [-12, -12, -41, 0x0008, 0x3C9],
        [-7, -25, -49, 0x000C, 0x3CD],
        [6, -22, -57, 0x0004, 0x3CF],
        [-11, -13, -65, 0x0008, 0x3D2]
    ],
    [       # frame 53
        [28, -36, -60, 0x0001, 0x3D4],
        [20, -28, -52, 0x0001, 0x3D6],
        [12, -20, -42, 0x0000, 0x3D7],
        [4, -12, -49, 0x0003, 0x3DB],
        [4, -12, -17, 0x0001, 0x3DD],
        [-4, -4, -43, 0x0003, 0x3E1],
        [-4, -4, -11, 0x0000, 0x3E2],
        [-12, 4, -43, 0x0002, 0x3E5],
        [-20, 12, -35, 0x0000, 0x3E6]
    ],
    [       # frame 54
        [-6, -10, -17, 0x0005, 0x3EA],
        [-13, -11, -25, 0x0008, 0x3ED],
        [-17, -15, -33, 0x000C, 0x3F1],
        [15, -47, -33, 0x000C, 0x3F5],
        [-13, -11, -41, 0x0008, 0x3F8],
        [-4, -12, -49, 0x0004, 0x3FA]
    ],
    [       # frame 55
        [-6, -10, -17, 0x0005, 0x3FE],
        [-14, -18, -25, 0x000C, 0x402],
        [-23, -9, -33, 0x000C, 0x406],
        [-12, -12, -41, 0x0008, 0x409],
        [-4, -12, -49, 0x0004, 0x40B]
    ],
    [       # frame 56
        [-6, -10, -17, 0x0005, 0x40F],
        [-13, -11, -33, 0x0009, 0x415],
        [-17, -15, -41, 0x000C, 0x419],
        [-4, -12, -49, 0x0004, 0x41B]
    ],
    [       # frame 57
        [-4, -4, -8, 0x0000, 0x41C],
        [-20, -12, -24, 0x000D, 0x424],
        [12, -20, -24, 0x0001, 0x426],
        [-23, -9, -32, 0x000C, 0x42A],
        [-8, 0, -40, 0x0000, 0x42B]
    ],
    [       # frame 58
        [-3, -13, -8, 0x0004, 0x42D],
        [-8, -8, -16, 0x0004, 0x42F],
        [-21, -11, -24, 0x000C, 0x433],
        [11, -19, -24, 0x0000, 0x434],
        [-21, -11, -32, 0x000C, 0x438],
        [-20, 4, -48, 0x0005, 0x43C]
    ],
    [       # frame 59
        [6, -30, -22, 0x0009, 0x442],
        [-2, -6, -27, 0x0002, 0x445],
        [-26, 2, -16, 0x0009, 0x44B],
        [-34, 26, -10, 0x0000, 0x44C]
    ],
    [       # frame 60
        [28, -36, -9, 0x0000, 0x44D],
        [20, -28, -16, 0x0001, 0x44F],
        [-4, -20, -8, 0x0008, 0x452],
        [-12, 4, -16, 0x0001, 0x454],
        [-36, 12, -8, 0x0008, 0x457]
    ],
    [       # frame 61
        [41, -49, -33, 0x0000, 0x458],
        [33, -41, -28, 0x0000, 0x459],
        [25, -33, -27, 0x0000, 0x45A],
        [17, -25, -33, 0x0001, 0x45C],
        [9, -17, -32, 0x0003, 0x460],
        [1, -9, -40, 0x0003, 0x464],
        [1, -9, -8, 0x0000, 0x465],
        [-7, -1, -39, 0x0003, 0x469],
        [-15, 7, -40, 0x0003, 0x46D],
        [-15, 7, -8, 0x0000, 0x46E],
        [-23, 15, -11, 0x0000, 0x46F]
    ],
    [       # frame 62
        [-7, -17, -38, 0x000A, 0x478],
        [9, -25, -54, 0x0005, 0x47C],
        [25, -49, -46, 0x0008, 0x47F],
        [-15, 7, -22, 0x0002, 0x482],
        [1, -17, -6, 0x0004, 0x484],
        [1, -9, -46, 0x0000, 0x485],
        [17, -25, -38, 0x0000, 0x486],
        [17, -25, -22, 0x0000, 0x487],
        [-7, -1, -14, 0x0000, 0x488],
        [9, -17, -14, 0x0000, 0x489],
        [-23, 15, -6, 0x0000, 0x48A]
    ],
    [       # frame 63
        [-13, -11, -8, 0x0008, 0x48D],
        [-11, -13, -24, 0x0009, 0x493],
        [-24, -8, -32, 0x000C, 0x497],
        [8, -24, -32, 0x0004, 0x499],
        [-17, -15, -40, 0x000C, 0x49D],
        [15, -23, -40, 0x0000, 0x49E],
        [-11, -13, -48, 0x0008, 0x4A1],
        [-2, -6, -56, 0x0000, 0x4A2]
    ],
    [       # frame 64
        [-12, -20, -24, 0x000E, 0x4AE],
        [-8, -16, -32, 0x0008, 0x4B1],
        [0, -16, -40, 0x0004, 0x4B3]
    ],
    [       # frame 65
        [19, -27, -29, 0x0000, 0x4B4],
        [11, -19, -33, 0x0002, 0x4B7],
        [3, -11, -40, 0x0003, 0x4BB],
        [3, -11, -8, 0x0000, 0x4BC],
        [-5, -3, -32, 0x0003, 0x4C0],
        [-21, 5, -28, 0x0004, 0x4C2]
    ],
    [       # frame 66
        [-17, -15, -24, 0x000E, 0x4CE],
        [-9, -7, -40, 0x0005, 0x4D2],
        [-17, 9, -32, 0x0000, 0x4D3],
        [15, -23, -24, 0x0000, 0x4D4]
    ],
    [       # frame 67
        [15, -23, -39, 0x0000, 0x4D5],
        [7, -15, -41, 0x0003, 0x4D9],
        [7, -15, -9, 0x0000, 0x4DA],
        [-1, -7, -42, 0x0003, 0x4DE],
        [-9, 1, -48, 0x0003, 0x4E2],
        [-9, 1, -16, 0x0001, 0x4E4],
        [-17, 9, -32, 0x0003, 0x4E8]
    ],
    [       # frame 68
        [-21, -11, -8, 0x000C, 0x4EC],
        [-18, -14, -24, 0x000D, 0x4F4],
        [-9, -15, -32, 0x0008, 0x4F7],
        [4, -20, -40, 0x0004, 0x4F9]
    ],
    [       # frame 69
        [-21, -11, -8, 0x000C, 0x4FD],
        [-19, -13, -16, 0x000C, 0x501],
        [-15, -9, -24, 0x0008, 0x504],
        [-7, -25, -32, 0x000C, 0x508],
        [1, -25, -40, 0x0008, 0x50B],
        [-6, -18, -48, 0x0008, 0x50E],
        [-6, -2, -56, 0x0000, 0x50F]
    ],
    [       # frame 70
        [-5, -19, -32, 0x000A, 0x518],
        [-21, -11, -8, 0x000C, 0x51C],
        [27, -35, -48, 0x0002, 0x51F],
        [19, -27, -32, 0x0001, 0x521],
        [-13, 5, -24, 0x0001, 0x523],
        [35, -43, -48, 0x0000, 0x524],
        [3, -11, -40, 0x0000, 0x525]
    ],
    [       # frame 71
        [-21, -11, -8, 0x000C, 0x529],
        [-17, -15, -16, 0x000C, 0x52D],
        [15, -47, -16, 0x000C, 0x531],
        [-11, -13, -32, 0x0009, 0x537],
        [3, -11, -40, 0x0000, 0x538]
    ],
    [       # frame 72
        [-22, -10, -16, 0x000D, 0x540],
        [10, -18, -16, 0x0001, 0x542],
        [-12, -12, -32, 0x0009, 0x548],
        [3, -11, -40, 0x0000, 0x549]
    ],
    [       # frame 73
        [-21, -11, -8, 0x000C, 0x54D],
        [-17, -15, -24, 0x000D, 0x555],
        [-11, -13, -32, 0x0008, 0x558],
        [3, -11, -40, 0x0000, 0x559]
    ],
    [       # frame 74
        [-17, -15, -8, 0x000C, 0x55D],
        [-13, -11, -16, 0x0008, 0x560],
        [-12, -12, -24, 0x0008, 0x563],
        [-7, -9, -32, 0x0004, 0x565],
        [-9, -7, -40, 0x0004, 0x567],
        [-15, -17, -48, 0x000C, 0x56B],
        [1, -25, -56, 0x0008, 0x56E],
        [2, -10, -64, 0x0000, 0x56F]
    ],
    [       # frame 75
        [-17, -15, -8, 0x000C, 0x573],
        [-13, -11, -16, 0x0008, 0x576],
        [-12, -12, -24, 0x0008, 0x579],
        [-7, -9, -32, 0x0004, 0x57B],
        [-15, -9, -40, 0x0008, 0x57E],
        [-11, -21, -48, 0x000C, 0x582],
        [21, -29, -48, 0x0000, 0x583],
        [-5, -27, -56, 0x000C, 0x587],
        [5, -21, -64, 0x0004, 0x589]
    ],
    [       # frame 76
        [-12, -12, -45, 0x000B, 0x595],
        [12, -28, -45, 0x0005, 0x599],
        [-20, 4, -13, 0x0005, 0x59D],
        [28, -36, -61, 0x0002, 0x5A0],
        [-4, -12, -53, 0x0004, 0x5A2],
        [4, -20, -5, 0x0004, 0x5A4],
        [4, -12, -61, 0x0000, 0x5A5],
        [4, -12, -13, 0x0000, 0x5A6]
    ],
    [       # frame 77
        [-12, -12, -46, 0x000B, 0x5B2],
        [28, -44, -46, 0x0005, 0x5B6],
        [-20, 4, -14, 0x0005, 0x5BA],
        [-4, -12, -54, 0x0004, 0x5BC],
        [12, -28, -38, 0x0004, 0x5BE],
        [4, -20, -6, 0x0004, 0x5C0],
        [4, -12, -62, 0x0000, 0x5C1],
        [44, -52, -46, 0x0000, 0x5C2],
        [4, -12, -14, 0x0000, 0x5C3]
    ],
    [       # frame 78
        [-17, -15, -8, 0x000C, 0x5C7],
        [-13, -11, -16, 0x0008, 0x5CA],
        [-16, -16, -24, 0x000C, 0x5CE],
        [16, -32, -24, 0x0004, 0x5D0],
        [-11, -13, -32, 0x0008, 0x5D3],
        [-6, -10, -56, 0x0006, 0x5D9],
        [1, -9, -64, 0x0000, 0x5DA]
    ],
    [       # frame 79
        [-22, -10, -8, 0x000C, 0x5DE],
        [10, -18, -8, 0x0000, 0x5DF],
        [-18, -14, -16, 0x000C, 0x5E3],
        [-12, -12, -24, 0x0008, 0x5E6],
        [-7, -9, -32, 0x0004, 0x5E8],
        [-11, -13, -40, 0x0008, 0x5EB],
        [-1, -15, -48, 0x0004, 0x5ED],
        [1, -17, -56, 0x0004, 0x5EF],
        [9, -17, -64, 0x0000, 0x5F0]
    ],
    [       # frame 80
        [-17, -15, -8, 0x000C, 0x5F4],
        [-13, -11, -16, 0x0008, 0x5F7],
        [-12, -12, -24, 0x0008, 0x5FA],
        [-7, -9, -32, 0x0004, 0x5FC],
        [-9, -15, -56, 0x000A, 0x605],
        [0, -8, -64, 0x0000, 0x606]
    ],
    [       # frame 81
        [-9, -7, -32, 0x0007, 0x60E],
        [-9, -7, -40, 0x0004, 0x610],
        [-18, -14, -56, 0x000D, 0x618],
        [-7, -9, -64, 0x0004, 0x61A]
    ]
]

patterns_blocks = [
    [0x0000, 0x0013],
    [0x0013, 0x0012],
    [0x0025, 0x0016],
    [0x003B, 0x0012],
    [0x004D, 0x0013],
    [0x0060, 0x0017],
    [0x0077, 0x0010],
    [0x0087, 0x0013],
    [0x009A, 0x0016],
    [0x00B0, 0x0010],
    [0x00C0, 0x0014],
    [0x00D4, 0x0014],
    [0x00E8, 0x0019],
    [0x0101, 0x0013],
    [0x0114, 0x0013],
    [0x0127, 0x0013],
    [0x013A, 0x0013],
    [0x014D, 0x0011],
    [0x015E, 0x000C],
    [0x016A, 0x000F],
    [0x0179, 0x0011],
    [0x018A, 0x000D],
    [0x0197, 0x000F],
    [0x01A6, 0x0013],
    [0x01B9, 0x000E],
    [0x01C7, 0x0011],
    [0x01D8, 0x0012],
    [0x01EA, 0x000E],
    [0x01F8, 0x0010],
    [0x0208, 0x0013],
    [0x021B, 0x0015],
    [0x0230, 0x0017],
    [0x0247, 0x0013],
    [0x025A, 0x0016],
    [0x0270, 0x0016],
    [0x0286, 0x0010],
    [0x0296, 0x0013],
    [0x02A9, 0x0016],
    [0x02BF, 0x0010],
    [0x02CF, 0x0014],
    [0x02E3, 0x0014],
    [0x02F7, 0x0010],
    [0x0307, 0x0010],
    [0x0317, 0x0012],
    [0x0329, 0x0012],
    [0x033B, 0x0011],
    [0x034C, 0x0012],
    [0x035E, 0x0012],
    [0x0370, 0x0012],
    [0x0382, 0x0015],
    [0x0397, 0x0012],
    [0x03A9, 0x0013],
    [0x03BC, 0x0016],
    [0x03D2, 0x0014],
    [0x03E6, 0x0014],
    [0x03FA, 0x0011],
    [0x040B, 0x0010],
    [0x041B, 0x0010],
    [0x042B, 0x0011],
    [0x043C, 0x0010],
    [0x044C, 0x000B],
    [0x0457, 0x0018],
    [0x046F, 0x001B],
    [0x048A, 0x0018],
    [0x04A2, 0x0011],
    [0x04B3, 0x000F],
    [0x04C2, 0x0012],
    [0x04D4, 0x0014],
    [0x04E8, 0x0011],
    [0x04F9, 0x0016],
    [0x050F, 0x0016],
    [0x0525, 0x0013],
    [0x0538, 0x0011],
    [0x0549, 0x0010],
    [0x0559, 0x0016],
    [0x056F, 0x001A],
    [0x0589, 0x001D],
    [0x05A6, 0x001D],
    [0x05C3, 0x0017],
    [0x05DA, 0x0016],
    [0x05F0, 0x0016],
    [0x0606, 0x0014]
]

# POI for collisions with background
poi_ga = (-6, -1)
poi_gb = (10, -1)
poi_b = (-6, 0)
poi_f = (10, 0)

stand = [(5, 1)]
stand_with_gun = [(11, 1)]
walk = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4)]
walk_with_gun = [(6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4)]
crouch_no_move = [(19, 1)]
crouch_no_move_with_gun = [(22, 1)]
crouch = [(17, 12), (18, 12), (19, 12)]
crouch_with_gun = [(20, 12), (21, 12), (22, 12)]
jump = [(41, 1)]
jump_fire = [(43, 8)]
jump_gun = [(45, 1)]
jump_shoot = [(47, 8)]
fall = [(42, 1)]
fall_fire = [(44, 8)]
fall_gun = [(46, 1)]
fall_shoot = [(48, 8)]
hit = [(57, 1)]
dead = [(58, 16), (59, 16), (60, 64), (60, 2)]
hijump_preparation = [(63, 1)]
hijump0 = [(64, 4)]
hijump1 = [(65, 255)]
hifall0 = [(66, 4)]
hifall1 = [(67, 255)]
walk_fire_1 = [(29, 2), (34, 6)]
walk_fire_2 = [(30, 2), (34, 6)]
walk_fire_3 = [(31, 2), (34, 6)]
walk_fire_4 = [(32, 2), (34, 6)]
walk_fire_5 = [(33, 2), (34, 6)]
walk_fire_6 = [(34, 8)]
walk_shoot_1 = [(35, 2), (40, 6)]
walk_shoot_2 = [(36, 2), (40, 6)]
walk_shoot_3 = [(37, 2), (40, 6)]
walk_shoot_4 = [(38, 2), (40, 6)]
walk_shoot_5 = [(39, 2), (40, 6)]
walk_shoot_6 = [(40, 8)]
punch = [(62, 12)]
slash = [(74, 2), (75, 2), (76, 2), (77, 2), (78, 4), (79, 2), (74, 2), (80, 2)]
crouch_fire_1 = [(23, 2), (25, 6)]
crouch_fire_2 = [(24, 2), (25, 6)]
crouch_fire_3 = [(25, 8)]
crouch_shoot_1 = [(26, 2), (28, 6)]
crouch_shoot_2 = [(27, 2), (28, 6)]
crouch_shoot_3 = [(28, 8)]
kick = [(50, 1), (61, 8), (50, 5)]
low_slash = [(68, 2), (69, 2), (70, 2), (71, 2), (72, 4), (68, 2), (73, 2)]
flying_kick = [(50, 2), (49, 8), (50, 5)]
flying_slash = [(51, 2), (52, 2), (53, 2), (54, 2), (55, 4), (51, 2), (56, 2)]

animations_table = [
    stand,
    stand_with_gun,
    walk,
    walk_with_gun,
    crouch_no_move,
    crouch_no_move_with_gun,
    crouch,
    crouch_with_gun,
    jump,
    jump_fire,
    jump_gun,
    jump_shoot,
    fall,
    fall_fire,
    fall_gun,
    fall_shoot,
    hit,
    dead,
    hijump_preparation,
    hijump0,
    hijump1,
    hifall0,
    hifall1,
    walk_fire_1,
    walk_fire_2,
    walk_fire_3,
    walk_fire_4,
    walk_fire_5,
    walk_fire_6,
    walk_shoot_1,
    walk_shoot_2,
    walk_shoot_3,
    walk_shoot_4,
    walk_shoot_5,
    walk_shoot_6,
    punch,
    slash,
    crouch_fire_1,
    crouch_fire_2,
    crouch_fire_3,
    crouch_shoot_1,
    crouch_shoot_2,
    crouch_shoot_3,
    kick,
    low_slash,
    flying_kick,
    flying_slash
]

STAND = 0
STAND_WITH_GUN = 1
WALK = 2
WALK_WITH_GUN = 3
CROUCH_NO_MOVE = 4
CROUCH_NO_MOVE_WITH_GUN = 5
CROUCH = 6
CROUCH_WITH_GUN = 7
JUMP = 8
JUMP_FIRE = 9
JUMP_GUN = 10
JUMP_SHOOT = 11
FALL = 12
FALL_FIRE = 13
FALL_GUN = 14
FALL_SHOOT = 15
HIT = 16
DEAD = 17
HIJUMP_PREPARATION = 18
HIJUMP0 = 19
HIJUMP1 = 20
HIFALL0 = 21
HIFALL1 = 22
WALK_FIRE_1 = 23
WALK_FIRE_2 = 24
WALK_FIRE_3 = 25
WALK_FIRE_4 = 26
WALK_FIRE_5 = 27
WALK_FIRE_6 = 28
WALK_SHOOT_1 = 29
WALK_SHOOT_2 = 30
WALK_SHOOT_3 = 31
WALK_SHOOT_4 = 32
WALK_SHOOT_5 = 33
WALK_SHOOT_6 = 34
PUNCH = 35
SLASH = 36
CROUCH_FIRE_1 = 37
CROUCH_FIRE_2 = 38
CROUCH_FIRE_3 = 39
CROUCH_SHOOT_1 = 40
CROUCH_SHOOT_2 = 41
CROUCH_SHOOT_3 = 42
KICK = 43
LOW_SLASH = 44
FLYING_KICK = 45
FLYING_SLASH = 46


rect1 = (-6, -58, 16, 59)

bounding_boxes = [
    rect1,    # bounding box 0,
    rect1,    # bounding box 1,
    rect1,    # bounding box 2,
    rect1,    # bounding box 3,
    rect1,    # bounding box 4,
    rect1,    # bounding box 5,
    rect1,    # bounding box 6,
    rect1,    # bounding box 7,
    rect1,    # bounding box 8,
    rect1,    # bounding box 9,
    rect1,    # bounding box 10,
    rect1,    # bounding box 11,
    None,    # bounding box 12,
    None,    # bounding box 13,
    None,    # bounding box 14,
    None,    # bounding box 15,
    None,    # bounding box 16,
    (-6, -30, 16, 31),    # bounding box 17,
    (-6, -30, 16, 31),    # bounding box 18,
    (-6, -30, 16, 31),    # bounding box 19,
    (-6, -30, 16, 31),    # bounding box 20,
    (-6, -30, 16, 31),    # bounding box 21,
    (-6, -30, 16, 31),    # bounding box 22,
    (-6, -30, 16, 31),    # bounding box 23,
    (-6, -30, 16, 31),    # bounding box 24,
    (-6, -30, 16, 31),    # bounding box 25,
    (-6, -30, 16, 31),    # bounding box 26,
    (-6, -30, 16, 31),    # bounding box 27,
    (-6, -30, 16, 31),    # bounding box 28,
    rect1,    # bounding box 29,
    rect1,    # bounding box 30,
    rect1,    # bounding box 31,
    rect1,    # bounding box 32,
    rect1,    # bounding box 33,
    rect1,    # bounding box 34,
    rect1,    # bounding box 35,
    rect1,    # bounding box 36,
    rect1,    # bounding box 37,
    rect1,    # bounding box 38,
    rect1,    # bounding box 39,
    rect1,    # bounding box 40,
    (-6, -47, 16, 48),    # bounding box 41,
    (-6, -47, 16, 48),    # bounding box 42,
    (-6, -47, 16, 48),    # bounding box 43,
    (-6, -47, 16, 48),    # bounding box 44,
    (-6, -47, 16, 48),    # bounding box 45,
    (-6, -47, 16, 48),    # bounding box 46,
    (-6, -47, 16, 48),    # bounding box 47,
    (-6, -47, 16, 48),    # bounding box 48,
    (-6, -47, 16, 48),    # bounding box 49,
    (-6, -47, 16, 48),    # bounding box 50,
    (-6, -47, 16, 48),    # bounding box 51,
    (-6, -47, 16, 48),    # bounding box 52,
    (-6, -47, 16, 48),    # bounding box 53,
    (-6, -47, 16, 48),    # bounding box 54,
    (-6, -47, 16, 48),    # bounding box 55,
    (-6, -47, 16, 48),    # bounding box 56,
    None, # (-6, -30, 16, 31),    # bounding box 57,
    None,    # bounding box 58,
    None,    # bounding box 59,
    None,    # bounding box 60,
    (-6, -30, 16, 31),    # bounding box 61,
    rect1,    # bounding box 62,
    (-6, -47, 16, 48),    # bounding box 63,
    (-6, -30, 16, 31),    # bounding box 64,
    (-6, -30, 16, 31),    # bounding box 65,
    (-6, -30, 16, 31),    # bounding box 66,
    (-6, -30, 16, 31),    # bounding box 67,
    (-6, -30, 16, 31),    # bounding box 68,
    (-6, -30, 16, 31),    # bounding box 69,
    (-6, -30, 16, 31),    # bounding box 70,
    (-6, -30, 16, 31),    # bounding box 71,
    (-6, -30, 16, 31),    # bounding box 72,
    (-6, -30, 16, 31),    # bounding box 73,
    rect1,    # bounding box 74,
    rect1,    # bounding box 75,
    rect1,    # bounding box 76,
    rect1,    # bounding box 77,
    rect1,    # bounding box 78,
    rect1,    # bounding box 79,
    rect1,    # bounding box 80,
    None,    # bounding box 81,
    # (-10, -58, 16, 59),    # bounding box 82,
    # (-10, -58, 16, 59),    # bounding box 83,
    # (-10, -58, 16, 59),    # bounding box 84,
    # (-10, -58, 16, 59),    # bounding box 85,
    # (-10, -58, 16, 59),    # bounding box 86,
    # (-10, -58, 16, 59),    # bounding box 87,
    # (-10, -58, 16, 59),    # bounding box 88,
    # (-10, -58, 16, 59),    # bounding box 89,
    # (-10, -58, 16, 59),    # bounding box 90,
    # (-10, -58, 16, 59),    # bounding box 91,
    # (-10, -58, 16, 59),    # bounding box 92,
    # (-10, -58, 16, 59),    # bounding box 93,
    # (-10, -30, 16, 31),    # bounding box 94,
    # (-10, -30, 16, 31),    # bounding box 95,
    # (-10, -30, 16, 31),    # bounding box 96,
    # (-10, -30, 16, 31),    # bounding box 97,
    # (-10, -30, 16, 31),    # bounding box 98,
    # (-10, -30, 16, 31),    # bounding box 99,
    # (-10, -30, 16, 31),    # bounding box 100,
    # (-10, -30, 16, 31),    # bounding box 101,
    # (-10, -30, 16, 31),    # bounding box 102,
    # (-10, -30, 16, 31),    # bounding box 103,
    # (-10, -30, 16, 31),    # bounding box 104,
    # (-10, -30, 16, 31),    # bounding box 105,
    # (-10, -58, 16, 59),    # bounding box 106,
    # (-10, -58, 16, 59),    # bounding box 107,
    # (-10, -58, 16, 59),    # bounding box 108,
    # (-10, -58, 16, 59),    # bounding box 109,
    # (-10, -58, 16, 59),    # bounding box 110,
    # (-10, -58, 16, 59),    # bounding box 111,
    # (-10, -58, 16, 59),    # bounding box 112,
    # (-10, -58, 16, 59),    # bounding box 113,
    # (-10, -58, 16, 59),    # bounding box 114,
    # (-10, -58, 16, 59),    # bounding box 115,
    # (-10, -58, 16, 59),    # bounding box 116,
    # (-10, -58, 16, 59),    # bounding box 117,
    # (-10, -47, 16, 48),    # bounding box 118,
    # (-10, -47, 16, 48),    # bounding box 119,
    # (-10, -47, 16, 48),    # bounding box 120,
    # (-10, -47, 16, 48),    # bounding box 121,
    # (-10, -47, 16, 48),    # bounding box 122,
    # (-10, -47, 16, 48),    # bounding box 123,
    # (-10, -47, 16, 48),    # bounding box 124,
    # (-10, -47, 16, 48),    # bounding box 125,
    # (-10, -47, 16, 48),    # bounding box 126,
    # (-10, -47, 16, 48),    # bounding box 127,
    # (-10, -47, 16, 48),    # bounding box 128,
    # (-10, -47, 16, 48),    # bounding box 129,
    # (-10, -47, 16, 48),    # bounding box 130,
    # (-10, -47, 16, 48),    # bounding box 131,
    # (-10, -47, 16, 48),    # bounding box 132,
    # (-10, -47, 16, 48),    # bounding box 133,
    # (-10, -30, 16, 31),    # bounding box 134,
    # None,    # bounding box 135,
    # None,    # bounding box 136,
    # None,    # bounding box 137,
    # (-10, -30, 16, 31),    # bounding box 138,
    # (-10, -58, 16, 59),    # bounding box 139,
    # (-10, -47, 16, 48),    # bounding box 140,
    # (-10, -30, 16, 31),    # bounding box 141,
    # (-10, -30, 16, 31),    # bounding box 142,
    # (-10, -30, 16, 31),    # bounding box 143,
    # (-10, -30, 16, 31),    # bounding box 144,
    # (-10, -30, 16, 31),    # bounding box 145,
    # (-10, -30, 16, 31),    # bounding box 146,
    # (-10, -30, 16, 31),    # bounding box 147,
    # (-10, -30, 16, 31),    # bounding box 148,
    # (-10, -30, 16, 31),    # bounding box 149,
    # (-10, -30, 16, 31),    # bounding box 150,
    # (-10, -58, 16, 59),    # bounding box 151,
    # (-10, -58, 16, 59),    # bounding box 152,
    # (-10, -58, 16, 59),    # bounding box 153,
    # (-10, -58, 16, 59),    # bounding box 154,
    # (-10, -58, 16, 59),    # bounding box 155,
    # (-10, -58, 16, 59),    # bounding box 156,
    # (-10, -58, 16, 59)    # bounding box 157
]

hit1 = (6, -17, 52, 13)
hit2 = (-7, -63, 32, 11)
hit3 = (25, -60, 13, 25)
hit4 = (20, -35, 31, 12)
hit5 = (3, -25, 17, 8)
hit6 = (29, -34, 21, 17)
hit7 = (0, -45, 48, 9)
hit8 = (-7, -51, 29, 12)
hit9 = (22, -48, 17, 25)
hit10 = (19, -23, 34, 16)
hit11 = (-6, -14, 25, 11)
hit12 = (0, -63, 24, 12)
hit13 = (20, -63, 18, 14)
hit14 = (23, -49, 30, 22)
hit15 = (12, -27, 25, 12)
hit16 = (6, -15, 14, 13)

hitboxes = [
	None,		# hitbox 0,
	None,		# hitbox 1,
	None,		# hitbox 2,
	None,		# hitbox 3,
	None,		# hitbox 4,
	None,		# hitbox 5,
	None,		# hitbox 6,
	None,		# hitbox 7,
	None,		# hitbox 8,
	None,		# hitbox 9,
	None,		# hitbox 10,
	None,		# hitbox 11,
	None,		# hitbox 12,
	None,		# hitbox 13,
	None,		# hitbox 14,
	None,		# hitbox 15,
	None,		# hitbox 16,
	None,		# hitbox 17,
	None,		# hitbox 18,
	None,		# hitbox 19,
	None,		# hitbox 20,
	None,		# hitbox 21,
	None,		# hitbox 22,
	None,		# hitbox 23,
	None,		# hitbox 24,
	None,		# hitbox 25,
	None,		# hitbox 26,
	None,		# hitbox 27,
	None,		# hitbox 28,
	None,		# hitbox 29,
	None,		# hitbox 30,
	None,		# hitbox 31,
	None,		# hitbox 32,
	None,		# hitbox 33,
	None,		# hitbox 34,
	None,		# hitbox 35,
	None,		# hitbox 36,
	None,		# hitbox 37,
	None,		# hitbox 38,
	None,		# hitbox 39,
	None,		# hitbox 40,
	None,		# hitbox 41,
	None,		# hitbox 42,
	None,		# hitbox 43,
	None,		# hitbox 44,
	None,		# hitbox 45,
	None,		# hitbox 46,
	None,		# hitbox 47,
	None,		# hitbox 48,
	hit1, 		# hitbox 49,
	None,		# hitbox 50,
	None,		# hitbox 51,
	hit2, 		# hitbox 52,
	hit3,		# hitbox 53,
	hit4,		# hitbox 54,
	hit5,		# hitbox 55,
	None,		# hitbox 56,
	None,		# hitbox 57,
	None,		# hitbox 58,
	None,		# hitbox 59,
	None,		# hitbox 60,
	hit6,		# hitbox 61,
	hit7,		# hitbox 62,
	None,		# hitbox 63,
	None,		# hitbox 64,
	None,		# hitbox 65,
	None,		# hitbox 66,
	None,		# hitbox 67,
	None,		# hitbox 68,
	hit8,		# hitbox 69,
	hit9,		# hitbox 70,
	hit10,		# hitbox 71,
	hit11,		# hitbox 72,
	None,		# hitbox 73,
	None,		# hitbox 74,
	hit12,		# hitbox 75,
	hit13,		# hitbox 76,
	hit14,		# hitbox 77,
	hit15,		# hitbox 78,
	hit16,		# hitbox 79,
	None,		# hitbox 80,
	None,		# hitbox 81,
	None		# hitbox 82,
]

walk_fire_anims = [WALK_FIRE_1, WALK_FIRE_2, WALK_FIRE_3, WALK_FIRE_4, WALK_FIRE_5, WALK_FIRE_6]
crouch_fire_anims = [CROUCH_FIRE_1, CROUCH_FIRE_2, CROUCH_FIRE_3]

high_close_attack_box = (0, -64, 48, 32)

sprite_data = TSpriteData(patterns, frames_table, patterns_blocks, animations_table, bounding_boxes, hitboxes, "punk")