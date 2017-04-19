import pygame
import numpy

# utils functions

def load_data_from_png(path):
    surf = pygame.image.load(path).convert()
    return split_surf(surf)

def split_surf(surf, n = 1000000, w = 8, h = 8):
    """Cuts a Surface in n 8x8 patterns. If n isn't specified, the whole
    surface is processed"""
    x = y = 0
    w_, h_ = surf.get_size()
    res = []
    for _ in range(n):
        res += [surf.subsurface((x, y, w, h))]
        x += w
        if x >= w_:
            x = 0
            y += h
            if y >= h_:
                break

    if w == 8 and h == 8:
        return res

    res_ = []
    for t in res:
        res_ += split_surf(t)
    return res_


# constants
JOY_0 = 0
JOY_1 = 1
BUTTON_UP = 1
BUTTON_DOWN = 2
BUTTON_LEFT = 4
BUTTON_RIGHT = 8
BUTTON_A = 16
BUTTON_B = 32
BUTTON_C = 64
BUTTON_START = 128


class GPSprite():
    def __init__(self):
        self.id_ = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.t_id = 0
        self.link = 0
        self.surface = None

    def set(self, id_, x, y, sw, sh, t_id, link):
        self.id_ = id_
        self.x = x
        self.y = y
        self.w = sw
        self.h = sh
        self.t_id = t_id
        self.link = link


class GP():
    display = pygame.display.set_mode((320, 224))
    clock = pygame.time.Clock()
    fps = 60
    tiles = []
    plane_A = None
    plane_A_offset = (0, 0)
    plane_B = None
    plane_B_offset = (0, 0)
    joypad_state = 0
    sprite_cache = [GPSprite() for _ in range(80)]
    frame_counter = 0
    is_recording = False
    record_path = 'record'

    @staticmethod
    def init():
        # print 'Init GenePy'
        pygame.init()
#        self.display = pygame.display.set_mode((320, 224))
        pygame.display.set_caption('GenePy version 0.1')

#        self.clock = pygame.time.Clock()

        GP.blank_tile = pygame.Surface((8, 8)).convert()
        GP.blank_tile.fill(0xFF00DC)

        GP.tiles = [GP.blank_tile.copy() for _ in range(0x800)]

#        self.plane_A = pygame.Surface((512, 512))
        GP.plane_A = [pygame.Surface((512, 512)).convert(),
                      pygame.Surface((512, 512)).convert()]
        GP.plane_A[0].fill(0xFF00DC)
        GP.plane_A[0].set_colorkey(0xFF00DC)
        GP.plane_A[1].fill(0xFF00DC)
        GP.plane_A[1].set_colorkey(0xFF00DC)
#        self.plane_A_offset = (0, 0)

#        self.plane_B = pygame.Surface((512, 512))
        GP.plane_B = [pygame.Surface((512, 512)).convert(),
                      pygame.Surface((512, 512)).convert()]
        GP.plane_B[0].fill(0xFF00DC)
        GP.plane_B[0].set_colorkey(0xFF00DC)
        GP.plane_B[1].fill(0xFF00DC)
        GP.plane_B[1].set_colorkey(0xFF00DC)
#        self.plane_B_offset = (0, 0)

    @staticmethod
    def read_joypad(joy_id):
        return GP.joypad_state

    @staticmethod
    def load_tile_data(data, start):
        GP.tiles[start:start + len(data)] = data

    @staticmethod
    def set_tilemap(plane, tile_id, x, y):
        priority = (tile_id & 0x8000) != 0
        hflip = (tile_id & 0x800)
        vflip = (tile_id & 0x1000)
        t_id = tile_id & 0x7FF

        tile = pygame.transform.flip(GP.tiles[t_id], hflip, vflip)

        pos = ((x % 64) * 8, (y % 64) * 8)
        plane[priority].blit(tile, pos)
        plane[1 - priority].blit(GP.blank_tile, pos)

    @staticmethod
    def draw_subplane(subplane, offset):
        x, y = offset
        x1 = (-x) % 512
        y1 = y % 512
        x2 = x1 + 320
        y2 = y1 + 224
#        print x, y, x1, y1, x2, y2
        if x2 < 512:
            if y2 < 512:
                GP.display.blit(subplane, (0, 0), (x1, y1, 320, 224))
            else:
                GP.display.blit(subplane, (0, 0), (x1, y1, 320, 512 - y1))
                GP.display.blit(subplane, (0, 512 - y1), (x1, 0, 320, y2 - 512))                
        else:
            if y2 < 512:
#                print 'blit1:', (0, 0), (x1, y1, 512 - x1, 224)
                GP.display.blit(subplane, (0, 0), (x1, y1, 512 - x1, 224))
#                print 'blit2:', (512 - x1, 0), (0, y1, x2 - 512, 224)
                GP.display.blit(subplane, (512 - x1, 0), (0, y1, x2 - 512, 224))
            else:
                GP.display.blit(subplane, (0, 0), (x1, y1, 512 - x1, 512 - y1))
                GP.display.blit(subplane, (0, 512 - y1), (x1, 0, 512 - x1, y2 - 512))
                GP.display.blit(subplane, (512 - x1, 0), (0, y1, x2 - 512, 512 - y1))
                GP.display.blit(subplane, (512 - x1, 512 - y1), (0, 0, x2 - 512, y2 - 512))
    
    @staticmethod
    def set_sprite(id_, x, y, sz, t_id, link):
        sw, sh = (sz >> 2) + 1, (sz & 3) + 1
        # print 'defining sprite #%d' % id_
        # print 'pos: (%d, %d)' % (x, y)
        # print 'size: %dx%d' % (sw, sh)
        # print 'from tile: %X' % t_id
        # print 'link to sprite #%d' % link
        GP.sprite_cache[id_].set(id_, x, y, sw, sh, t_id, link)

    @staticmethod
    def draw_sprites(l):
        for s in l:
            GP.display.blit(s.surface, (s.x, s.y))

    @staticmethod
    def render_sprite(s):
        s.priority = 0
        if s.w * s.h == 0:
            return None
        res = pygame.Surface((s.w * 8, s.h * 8))
        res.fill(0xFF00DC)
        res.set_colorkey(0xFF00DC)

        x = 0
        if s.t_id & 0x8000:
            s.priority = 1

        tid = s.t_id & 0x7FF
        for _ in range(s.w):
            y = 0
            for _ in range(s.h):
                res.blit(GP.tiles[tid], (x, y))
                y += 8
                tid += 1
            x += 8

        hflip, vflip = s.t_id & 0x800, s.t_id & 0x1000
        if hflip or vflip:
            res = pygame.transform.flip(res, True, False)
        s.surface = res
        return res

    @staticmethod
    def render_sprites():
        id_ = 0
        GP.low_sprites = []
        GP.hi_sprites = []

        while True:
            spr = GP.sprite_cache[id_]
            GP.render_sprite(spr)
            if spr.priority:
                GP.hi_sprites += [spr]
            else:
                GP.low_sprites += [spr]
            id_ = spr.link
            if id_ == 0:
                break

    @staticmethod
    def wait_vblank():
        # print 'VInt'
        # handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print('Quit GenePy')
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    print('Escape GenePy')
                    if True:
                        GP.dump_tiles('debug/vram')
                        GP.dump_sprites('debug/sprite')
                        GP.dump_planes('debug/plane')
                    exit()

            key = pygame.key.get_pressed()
            GP.joypad_state = (key[pygame.K_UP]) \
                | (key[pygame.K_DOWN] << 1) \
                | (key[pygame.K_LEFT] << 2) \
                | (key[pygame.K_RIGHT] << 3) \
                | (key[pygame.K_a] << 4) \
                | (key[pygame.K_s] << 5) \
                | (key[pygame.K_d] << 6) \
                | (key[pygame.K_RETURN] << 7)

        # draw planes
        # GP.display.fill(0xFF808080)
        GP.draw_subplane(GP.plane_B[0], GP.plane_B_offset)
        GP.draw_subplane(GP.plane_A[0], GP.plane_A_offset)

        # draw sprites
        GP.render_sprites()
        GP.draw_sprites(GP.low_sprites)

        GP.draw_subplane(GP.plane_B[1], GP.plane_B_offset)
        GP.draw_subplane(GP.plane_A[1], GP.plane_A_offset)

        GP.draw_sprites(GP.hi_sprites)

        GP.frame_counter += 1
        
        if GP.is_recording:
            pygame.image.save(GP.display, '%s/%06d.png' % (GP.record_path, GP.frame_counter))

        # flip buffers
        pygame.display.flip()

        # wait clock
        GP.clock.tick(GP.fps)

    @staticmethod
    def dump_tiles(path):
        s = pygame.Surface((128, 1024))
        x = y = 0
        for t in GP.tiles:
            s.blit(t, (x, y))
            x += 8
            if x >= 128:
                x = 0
                y += 8

        pygame.image.save(s, '%s.png' % path)

    @staticmethod
    def dump_sprites(path):
        for i in range(80):
            s = GP.sprite_cache[i]
            if s.surface:
                pygame.image.save(s.surface,
                                  '%s-%02d (%02d).png' % (path, i, s.link))

    @staticmethod
    def dump_planes(path):
        surf = GP.plane_A[0].copy()
        surf.blit(GP.plane_A[1], (0, 0))
        pygame.image.save(surf, '%s-A.png' % path)

        surf = GP.plane_B[0].copy()
        surf.blit(GP.plane_B[1], (0, 0))
        pygame.image.save(surf, '%s-B.png' % path)

    @staticmethod
    def halt():
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print('Quit GenePy')
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        print('Escape GenePy')
                        if True:
                            GP.dump_tiles('debug/vram')
                            GP.dump_sprites('debug/sprite')
                            GP.dump_planes('debug/plane')
                        exit()
                    return
            # wait clock
            GP.clock.tick(GP.fps)



# GP = GenePy()

    
    