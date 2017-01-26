import pygame
import numpy
import random
import itertools

from tools.psdreader import *
from tools.animsreader import load_animdefs
from map_tools import make_sheet


def read_split_file(path):
    def read_rect(srect):
        return tuple([int(x) for x in srect.strip('()').split(',')])

    def read_rects(srects):
        srects = srects.strip(' []\r\n')
        if srects:
            return [read_rect(srect.strip()) for srect in srects.split(';')]
        else:
            return []
    
    splits = {}
    with open(path) as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('frame:'):
            f_id = int(line[6:])
        elif line.startswith('split:'):
            print 'split:', read_rects(line[6:])
            splits[f_id] = read_rects(line[6:])
    
    return splits

def get_patterns(surf):
    res = []
    w, h = surf.get_size()
    for x in range(0, w, 8):
        for y in range(0, h, 8):
            res += [surf.subsurface((x, y, 8, 8))]
    print len(res), 'patterns'
    return res

def get_subsurface(surf, rect):
    x, y, w, h = rect
    sw, sh = surf.get_size()
    
    res = pygame.Surface((w, h), pygame.SRCALPHA)
    
    rx = ry = 0
    
    if x < 0:
        rx = -x
        w += x
        x = 0
    if x + w > sw:
        w = sw

    if y < 0:
        ry = -y
        h += y
        y = 0
    if y + h > sh:
        h = sh
    
    res.blit(surf, (rx, ry), (x, y, w, h))
    return res


def compare_bottoms(img1, img2):
    a1 = pygame.surfarray.pixels2d(img1)
    a2 = pygame.surfarray.pixels2d(img2)

    w, h = a2.shape
    print w, h
    n = 0
    tot = 100
    while tot:
        x, y = random.randint(0, w - 1), random.randint(h - 32, h - 1)
        if a1[x, y] & 0xFF000000 or a2[x, y] & 0xFF000000:
            tot -= 1
            if a1[x, y] == a2[x, y]:
                n += 1
    del a2
    del a1
    return n


def similar_from_bottom(img1, img2):
    a1 = pygame.surfarray.pixels2d(img1)
    a2 = pygame.surfarray.pixels2d(img2)

    w, h = a2.shape
    res = 0
    for y in range(h - 1, -1, -1):
        c1 = numpy.logical_and(a1[:, y] & 0xFF000000 != 0, a2[:, y] & 0xFF000000 != 0) 
        c2 = numpy.logical_and(c1, a1[:, y] != a2[:, y])
        if c2.any():
            break
        res += 1
    del a2
    del a1
    return res


def get_first(img):
    a = pygame.surfarray.pixels2d(img)

    w, h = a.shape
    y = 0
    while y < h:
        c = a[:, y] & 0xFF000000 != 0
        if c.any():
            break
        y += 1
    del a
    return y


def similar_from_top(img1, y1, img2, y2):
    a1 = pygame.surfarray.pixels2d(img1)
    a2 = pygame.surfarray.pixels2d(img2)

    w, h = a2.shape
    res = 0
    while y1 < h and y2 < h:
        c1 = numpy.logical_and(a1[:, y1] & 0xFF000000 != 0, a2[:, y2] & 0xFF000000 != 0) 
        c2 = numpy.logical_and(c1, a1[:, y1] != a2[:, y2])
        if c2.any():
            break
        res += 1
        y1 += 1
        y2 += 1    
    del a2
    del a1
    return res



def similar_from_top2(img1, y1, img2, y2):
    a1 = pygame.surfarray.pixels2d(img1)
    a2 = pygame.surfarray.pixels2d(img2)

    w, h = a2.shape
    res = 0
    while y2 < h:
        c1 = a1[:, y1] & 0xFF000000 != 0 
        c2 = numpy.logical_and(c1, a1[:, y1] != a2[:, y2])
        if c2.any():
            break
        res += 1
        y1 += 1
        y2 += 1    
    del a2
    del a1
    return res

def show_diffs(src, part1, part2):
    res = pygame.Surface((128, 64))

    s = pygame.surfarray.pixels2d(src)
    p1 = pygame.surfarray.pixels2d(part1)
    p2 = pygame.surfarray.pixels2d(part2)
    r = pygame.surfarray.pixels2d(res)

    m1 = (p1 & 0xFF000000) != 0
    m2 = (p2 & 0xFF000000) != 0
    m = numpy.logical_and(m1, m2)

    r[(s & 0xFF000000) != 0] = 0xFFFF0000
    r[m1] = 0xFF00FF00
    r[m2] = 0xFF00FF00
    r[m] = 0xFF0000FF
    r[numpy.logical_and(m, (s & 0x00FFFFFF) != (p1 & 0x00FFFFFF))] = 0xFFFF00FF

    del r
    del p1
    del p2
    del s

    return res


def get_surrounding_band(surf):
    a = pygame.surfarray.pixels2d(surf)

    y0 = 0
    while True:
        if (a[:, y0] & 0xFF000000).any():
            break
        y0 += 1

    y1 = 63
    while True:
        if (a[:, y1] & 0xFF000000).any():
            break
        y1 -= 1

    del a
    return (y0, y1 - y0 + 1)



if __name__ == '__main__':
    base_dir = 'C:/Users/Tryphon/Documents/hack/Shinobi/sheets/musashi2'

    if False:
        anims = load_animdefs('%s/animdefs.txt' % base_dir)

        print anims

        res = ''
        res2 = 'animations_table = [\n'
        res2_ = []
        name_id = 0
        name_ids = ''

        for name in anims.keys():
            anim = anims[name]
            if not 'hflip' in anim:
                name = name.replace('_right', '')
                res += ('%s = %s\n' % (name, anim['steps'] + [(-1, 0)]))
                res2_ += ['\t' + name]

                name_ids += '%s = %s\n' % (name.upper(), name_id)
                name_id += 1

        print res
        res2 += ',\n'.join(res2_) + '\n]\n'
        print res2

        print name_ids
        exit()


    if False:
        # extract frames (to speed up process)
        print 'loading psd file'
        psd = load_psd('%s/sheet2.psd' % base_dir)
        print psd

        frames = {}
        for i, layer in enumerate(psd.get_layers()):
            nm = layer.get_name()
            if nm.startswith('frame'):
                nm, j_ = nm.split(' ')
                j = int(j_)
                surf = layer.get_surface()
                frames[j] = surf
                pygame.image.save(frames[j], 'frames/frame%02d.png' % j)
        exit()

    frames = [pygame.image.load('frames/frame%02d.png' % i) for i in range(82)]

    bottoms = [[[6, 0, 29, 35], 32],
               [[7, 1, 30, 36], 32],
               [[8, 2, 31, 37], 32],
               [[9, 3, 32, 38], 32],
               [[10, 4, 33, 39], 32],
               [[34, 11, 5, 40, 74, 75, 76, 77, 78, 79], 32],
               [[17, 20, 23, 26], 16],
               [[18, 21, 24, 27], 16],
               [[22, 19, 25, 28, 68, 69, 70, 71, 72, 73], 16],
               [[43, 41, 45, 47, 52, 53, 54, 55, 56], 32],
               [[44, 42, 46, 48], 32]]

    tops = [[[0, 5], 28],
            [[1, 4], 26],
            [[2, 3], 28],
            [[6, 7, 8, 9, 10, 11], 25],
            [[20, 21, 22], 18],
            [[23, 24, 25], 17],
            [[26, 27, 28], 17],
            [[29, 30, 31, 32, 33, 34], 26],
            [[35, 36, 37, 38, 39, 40], 23],
            [[41, 42], 15],
            [[43, 44], 19],
            [[45, 46], 21],
            [[47, 48], 17],
            [[51, 68], 24],
            [[52, 69], 34],
            [[53, 70], 30],
            [[54, 71], 18],
            [[55, 72], 18],
            [[56, 73], 18]]


    if False:
    # make tops
        tsprites = [{'top': None, 'bottom': None} for _ in range(82)]
        parts = []

        delta_y = [get_first(frames[k]) for k in range(82)]

        i = 0
        for ids, _ in tops:
            y = max(delta_y[k] for k in ids)
            h = 64 - y

            ts = [pygame.surfarray.pixels2d(frames[k])[:, delta_y[k] : delta_y[k] + h] for k in ids]
            print ', '.join(['(%d -> %d)' % (delta_y[k], delta_y[k] + h) for k in ids])
            t0 = ts[0]
            mask = numpy.ones((128, h), dtype = bool)
            print mask.shape, t0.shape

            for t in ts[1:]:
                mask = numpy.logical_and(mask, t0 != t)

            del ts
            res = frames[ids[0]].copy()
            res_ = pygame.surfarray.pixels2d(res)
            res_[:, delta_y[ids[0]] : delta_y[ids[0]] + h][mask] = 0
            del res_

            pygame.image.save(res, 'temp/top%02d.png' % i)
            i += 1

        exit()

    if True:
        # Second attempt, with preloaded tops
        delta_y = [get_first(frames[k]) for k in range(82)]
        tsprites = [{'top': None, 'bottom': None} for _ in range(82)]
        parts = []
        i = 0
        while True:
            try:
                part = pygame.image.load('frames/top%02d.png' % i)
                y, h = get_surrounding_band(part)
                print 'top%02d : %d, %d' % (i, y, h)
                parts += [part.subsurface((0, y, 128, h))]
                i += 1
            except Exception:
                break

        i = 0
        for ids, _ in tops:
            for k in ids:
                tsprites[k]['top'] = i
            i += 1

        top_error = [0] * 82
        for ids, _ in bottoms:
            for k in ids:
#                print k
                frame = frames[k]
                y, h = get_surrounding_band(frame)
#                print 'rect:', (y, h)
#                print tsprites[k]
                bot_h = 0
                if tsprites[k]['top'] is not None:
                    top = parts[tsprites[k]['top']]
                    bot_h_ = 64 - y - similar_from_top2(frame, y, top, 0)
                    print k, ':', bot_h_
                    bot_h = max(bot_h, bot_h_)
                else:
                    print '%d has bottom but no top' % k

            print 'bottom height should be %d' % bot_h
            for k in ids:
                top_error[k] = max(top_error[k], bot_h)

        for k in range(82):
            print 'top error for %s (frame %d): %d' % (tsprites[k]['top'], k, top_error[k])



        exit()


        delta_y = [get_first(frames[k]) for k in range(82)]

        i = 0
        for ids, _ in tops:
            y = max(delta_y[k] for k in ids)
            h = 64 - y

            ts = [pygame.surfarray.pixels2d(frames[k])[:, delta_y[k] : delta_y[k] + h] for k in ids]
            print ', '.join(['(%d -> %d)' % (delta_y[k], delta_y[k] + h) for k in ids])
            t0 = ts[0]
            mask = numpy.ones((128, h), dtype = bool)
            print mask.shape, t0.shape

            for t in ts[1:]:
                mask = numpy.logical_and(mask, t0 != t)

            del ts
            res = frames[ids[0]].copy()
            res_ = pygame.surfarray.pixels2d(res)
            res_[:, delta_y[ids[0]] : delta_y[ids[0]] + h][mask] = 0
            del res_

            pygame.image.save(res, 'temp/top%02d.png' % i)
            i += 1

        exit()


        i = 0
        for ids, h in bottoms:
            for k in ids:
                tsprites[k]['bottom'] = (i, (64 - h, h))
            frame = frames[ids[0]]
            parts += [frame.subsurface((0, 64 - h, 128, h))]
            i += 1

        for ids, h in tops:
            for k in ids:
                tsprites[k]['top'] = (i, (get_first(frames[k]), h))
            frame = frames[ids[0]]
            y = get_first(frame)
            parts += [frame.subsurface((0, y, 128, h))]
            i += 1

        for k in range(82):
            tspr = tsprites[k]
            frame = frames[k]

            if tspr['bottom'] and not tspr['top']:
                _, (y1, h) = tspr['bottom']
                y0 = get_first(frame)
                tspr['top'] = (i, (y0, y1 - y0))
                parts += [frame.subsurface((0, y0, 128, y1 - y0))]
                i += 1

            elif tspr['top'] and not tspr['bottom']:
                _, (y0, h) = tspr['top']
                y1 = y0 + h
                tspr['bottom'] = (i, (y1, 64 - y1))
                parts += [frame.subsurface((0, y1, 128, 64 - y1))]
                i += 1

            elif not tspr['top'] and not tspr['bottom']:
                y0 = get_first(frame)
                tspr['top'] = (i, (y0, 64 - y0))
                parts += [frame.subsurface((0, y0, 128, 64 - y0))]
                i += 1


            print 'frame %s : top = %s, bottom = %s' % (k, tspr['top'], tspr['bottom'])

        if True:
            for i, part in enumerate(parts):
                pygame.image.save(part, 'part%02d.png' % i)

        for k in range(82):
            res = frames[k].copy()
            tspr = tsprites[k]

            dst2 = pygame.Surface((128, 64), pygame.SRCALPHA)
            if tspr['bottom']:
                i, (y, h) = tspr['bottom']
                res.blit(parts[i], (0, y)) #, special_flags = pygame.BLEND_SUB)
                dst2.blit(parts[i], (0, y))

            i, (y, h) = tspr['top']
            res.blit(parts[i], (0, y)) #, special_flags = pygame.BLEND_SUB)
            dst1 = pygame.Surface((128, 64), pygame.SRCALPHA)
            dst1.blit(parts[i], (0, y))


            pygame.image.save(frames[k], 'temp/res%02d-0.png' % k)
            pygame.image.save(dst1, 'temp/res%02d-1.png' % k)
            pygame.image.save(dst2, 'temp/res%02d-2.png' % k)
            pygame.image.save(res, 'temp/res%02d-3.png' % k)
            pygame.image.save(show_diffs(frames[k], dst1, dst2), 'temp/res%02d-4.png' % k)

        exit()

    if True:
        # First attempt
        tsprites = [{'top': None, 'bottom': None} for _ in range(82)]
        parts = []

        i = 0
        for ids, h in bottoms:
            for k in ids:
                tsprites[k]['bottom'] = (i, (64 - h, h))
            frame = frames[ids[0]]
            parts += [frame.subsurface((0, 64 - h, 128, h))]
            i += 1

        for ids, h in tops:
            for k in ids:
                tsprites[k]['top'] = (i, (get_first(frames[k]), h))
            frame = frames[ids[0]]
            y = get_first(frame)
            parts += [frame.subsurface((0, y, 128, h))]
            i += 1

        for k in range(82):
            tspr = tsprites[k]
            frame = frames[k]

            if tspr['bottom'] and not tspr['top']:
                _, (y1, h) = tspr['bottom']
                y0 = get_first(frame)
                tspr['top'] = (i, (y0, y1 - y0))
                parts += [frame.subsurface((0, y0, 128, y1 - y0))]
                i += 1

            elif tspr['top'] and not tspr['bottom']:
                _, (y0, h) = tspr['top']
                y1 = y0 + h
                tspr['bottom'] = (i, (y1, 64 - y1))
                parts += [frame.subsurface((0, y1, 128, 64 - y1))]
                i += 1

            elif not tspr['top'] and not tspr['bottom']:
                y0 = get_first(frame)
                tspr['top'] = (i, (y0, 64 - y0))
                parts += [frame.subsurface((0, y0, 128, 64 - y0))]
                i += 1


            print 'frame %s : top = %s, bottom = %s' % (k, tspr['top'], tspr['bottom'])

        if True:
            for i, part in enumerate(parts):
                pygame.image.save(part, 'part%02d.png' % i)

        for k in range(82):
            res = frames[k].copy()
            tspr = tsprites[k]

            dst2 = pygame.Surface((128, 64), pygame.SRCALPHA)
            if tspr['bottom']:
                i, (y, h) = tspr['bottom']
                res.blit(parts[i], (0, y)) #, special_flags = pygame.BLEND_SUB)
                dst2.blit(parts[i], (0, y))

            i, (y, h) = tspr['top']
            res.blit(parts[i], (0, y)) #, special_flags = pygame.BLEND_SUB)
            dst1 = pygame.Surface((128, 64), pygame.SRCALPHA)
            dst1.blit(parts[i], (0, y))


            pygame.image.save(frames[k], 'temp/res%02d-0.png' % k)
            pygame.image.save(dst1, 'temp/res%02d-1.png' % k)
            pygame.image.save(dst2, 'temp/res%02d-2.png' % k)
            pygame.image.save(res, 'temp/res%02d-3.png' % k)
            pygame.image.save(show_diffs(frames[k], dst1, dst2), 'temp/res%02d-4.png' % k)

        exit()

    if True:
        print 'bottom'
        for part, _ in bottoms:

            for i, j in itertools.combinations(part, 2):
                src = frames[i]
                dst = frames[j]
                bot_sim = similar_from_bottom(src, dst)
                print 'frame %d and %d : %d' % (i, j, bot_sim)
            print '=========================================='


        print 'top'
        for part, _ in tops:
            for i, j in itertools.combinations(part, 2):
                src = frames[i]
                y1 = get_first(src)
                dst = frames[j]
                y2 = get_first(dst)
                top_sim = similar_from_top(src, y1, dst, y2)
                print 'frame %d and %d : %d' % (i, j, top_sim)
            print '=========================================='
        exit()

        # detect similarities in frames 0, 6, 29, 35
        src = frames[6]
        y1 = get_first(src)
        for i in [0, 6, 29, 35]:
            dst = frames[i]
            bot_sim = similar_from_bottom(src, dst)
            sim = min(63 - bot_sim, 32)
            print 'frame %d : bottom: % d, remains %d' % (i, sim, 64 - get_first(dst) - sim)

        exit()


    splits = read_split_file('%s/split.txt' % base_dir)
    
    if True:
        # generating frames_table and patterns_blocks
        res = 'frames_table = '
        dp = 0
        res_ = []
        ptrn_blocks = []
        for i in splits.keys():
            print 'frame:', i
            split = splits[i]
            print split
            res__ = []
            dp0 = dp
            for j, (x, y, w, h) in enumerate(split):
                x_ = x - 64
                y_ = y - 64
                bx_ = -x_ - w
                sw, sh = w / 8, h / 8
                flags = ((sw - 1) << 2) + sh - 1
                dp += sw * sh
                res__ += ['\t\t[%d, %d, %d, 0x%04X, 0x%02X]' % (x_, bx_, y_, flags, dp)]
            res_ += ['\t[\t\t# frame %d\n%s\n\t]' % (i, ',\n'.join(res__))]
            
            ptrn_blocks += [(dp0, dp - dp0)]

        res += '[\n%s\n]\n' % ',\n'.join(res_)

        print res

        print 'patterns_blocks = [\n%s\n]\n' % ',\n'.join(['\t[0x%04X, 0x%04X]' % (p, l)\
                                                           for (p, l) in ptrn_blocks])
        
        exit()

    if True:
        # generating patterns    
        patterns = []
        for i, layer in enumerate(psd.get_layers()):
            nm = layer.get_name()
            if nm.startswith('frame'):
                nm, j_ = nm.split(' ')
                j = int(j_)
                surf = layer.get_surface()
    
                print '%d: frame %d (%s) -> %x' % (i, j, surf.get_size(), len(patterns))
                
                for k, rect in enumerate(splits[j]):
                    sub = get_subsurface(surf, rect)
                    patterns += get_patterns(sub)
                    pygame.image.save(sub, '%s/debug/%02d-%02d.png' % (base_dir, i, k))
                    pygame.draw.rect(surf, pygame.Color('red'), rect, 1)
                
                pygame.image.save(surf, '%s/debug/%02d.png' % (base_dir, i))
        
        print '%d patterns generated' % len(patterns)
        make_sheet(patterns, '%s/patterns.png' % base_dir)
    
    

        
