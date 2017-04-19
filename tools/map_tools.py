import sys
sys.path.append('..')
sys.path.append('C:/Users/Tryphon/Documents/workspace/MDTools')
sys.path.append('C:/Users/Tryphon/Documents/workspace/ShinoPy')

import genepy
import pygame


def make_sheet(ptrns, path):
    n = len(ptrns)
    h = n // 16
    if n % 16:
        h += 1
    res = pygame.Surface((128, h * 8), pygame.SRCALPHA)
    res.fill(pygame.Color(0xFF, 0, 0xDC, 0xFF))
    x = y = 0
    for p in ptrns:
        res.blit(p, (x, y))
        x += 8
        if x == 128:
            y += 8
            x = 0
    pygame.image.save(res, path)

def compare(s1, s2, h1, h2):
    if h1 == h2:
        if (s1 == s2).all():
            return 1
        if (s1[::-1, :] == s2).all():
            return 2
        if (s1[:, ::-1] == s2).all():
            return 3
    return 0
        

def get_datas(path):
    tileset = pygame.image.load(path)
    
    surfs = genepy.split_surf(tileset, w = 16, h = 16)
    cuts = [pygame.surfarray.pixels2d(c)\
            for c in surfs]
    
    res = []
    i = 0
    
    hash_ = []
    for s in cuts:
        hash_ += [s.flatten().sum()]
    
    ptrns = []
    for t in range(len(cuts)):
        s = cuts[t]
        for t_ in range(t):
            s_ = cuts[t_]
            cmp =  compare(s, s_, hash_[t], hash_[t_])
            if cmp:
                print ('%d and %d matched : %d' % (t, t_, cmp))
                t_id = res[t_]
                if cmp == 2:
                    t_id += 0x800
                elif cmp == 3:
                    t_id += 0x1000
                res += [t_id]
                break
        else:
            res += [i]
            ptrns += [surfs[t]]
            i += 1
    
    return {'ptrns': ptrns,
            'tiles': res}


if __name__ == '__main__':
    if False:
        datas = get_datas('../res/test.png')

        for t in range(len(datas['tiles'])/4):
            print ('\t0x%X, 0x%X, 0x%X, 0x%X,' % tuple([i + 0 for i in datas['tiles'][4*t : 4*t + 4]]))

        make_sheet(datas['ptrns'], '../res/level_1_1.png')    
    
    if True:
        OBJECT_PUNK = 1
        OBJECT_SHOOTER = 2
        objects = [
            (OBJECT_PUNK, 0, 25, 14),
            (OBJECT_SHOOTER, 0, 29, 14),
            (OBJECT_SHOOTER, 1, 37, 7),
            (OBJECT_PUNK, 0, 41, 14),
            (OBJECT_PUNK, 1, 45, 7),
            (OBJECT_SHOOTER, 0, 47, 14),
            (OBJECT_SHOOTER, 0, 49, 14),
            (OBJECT_SHOOTER, 0, 57, 14),
            (OBJECT_PUNK, 1, 59, 7),
            (OBJECT_SHOOTER, 1, 66, 7),
            (OBJECT_SHOOTER, 0, 76, 14),
            (OBJECT_PUNK, 0, 81, 14),
            (OBJECT_PUNK, 0, 82, 14),
            (OBJECT_PUNK, 0, 83, 14),
            (OBJECT_SHOOTER, 0, 91, 12),
            (OBJECT_SHOOTER, 1, 94, 7),
            (OBJECT_SHOOTER, 0, 95, 14),
            (OBJECT_PUNK, 1, 105, 7),
            (OBJECT_PUNK, 0, 109, 14),
            (OBJECT_SHOOTER, 1, 117, 7),
            (OBJECT_SHOOTER, 0, 118, 14),
            (OBJECT_SHOOTER, 0, 120, 14),
            (OBJECT_SHOOTER, 0, 122, 14),
            (OBJECT_SHOOTER, 0, 124, 14)
    ]

    objects_ = []
    for obj, floor, x, y in objects:
        objects_ += ['\t(%s, %d, %d, %d)' % (obj, floor, x*16, y*16 + 15)]
    print (',\n'.join(objects_))

