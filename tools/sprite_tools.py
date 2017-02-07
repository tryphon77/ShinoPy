import sys
sys.path.append('..')
sys.path.append('C:/Users/Tryphon/Documents/workspace/MDTools')

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


if __name__ == '__main__':
    # base_dir = 'C:/Users/Tryphon/Documents/hack/Shinobi/sheets/musashi2'
    base_dir = 'C:/Users/Tryphon/Documents/hack/Shinobi/sheets/spidey'
    hotspot_x = 64
    hotspot_y = 84


    if False:
        # generate anims

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
                res += ('%s = %s\n' % (name, anim['steps']))
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
    else:
        frames = [pygame.image.load('frames/frame%02d.png' % i) for i in range(82)]

    if True:
        # generating frames_table and patterns_blocks
        splits = read_split_file('%s/split.txt' % base_dir)

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
                x_ = x - hotspot_x
                y_ = y - hotspot_y
                bx_ = -x_ - w
                sw, sh = w / 8, h / 8
                flags = ((sw - 1) << 2) + sh - 1
                res__ += ['\t\t[%d, %d, %d, 0x%04X, 0x%02X]' % (x_, bx_, y_, flags, dp)]
                dp += sw * sh
            res_ += ['\t[\t\t# frame %d\n%s\n\t]' % (i, ',\n'.join(res__))]
            
            ptrn_blocks += [(dp0, dp - dp0)]

        res += '[\n%s\n]\n' % ',\n'.join(res_)

        print res

        print 'patterns_blocks = [\n%s\n]\n' % ',\n'.join(['\t[0x%04X, 0x%04X]' % (p, l)\
                                                           for (p, l) in ptrn_blocks])
        
        exit()


    if False:
        # generate splits if not presents
        from tools.surface import *
        from tools.colors import *
        import tools.plugins.basic_splitter
        import tools.plugins.group_splitter
        import tools.plugins.row_splitter
        import tools.plugins.best_splitter

        splitters = [(tools.plugins.basic_splitter.splitter, []),
                     (tools.plugins.group_splitter.splitter, []),
                     (tools.plugins.row_splitter.splitter, [])]

        ennemy_palette = Palette.from_rgb_values([0x4CFF00, 0x000000, 0xFF0000, 0x524252,
                                                  0x4A4A4A, 0x6B5B6B, 0x847384, 0xAD7B00,
                                                  0xAD7B42, 0x949400, 0x9C8C9C, 0xD6A400,
                                                  0xD69C6B, 0xB5A4B5, 0xFFC594, 0xF7F7F7], 
                                                 id_ = 1)

        psd = load_psd('%s/sheet.psd' % base_dir)

        res = ''
        for i, layer in enumerate(psd.get_layers()):
            nm = layer.get_name()
            if nm.startswith('frame'):
                nm, j_ = nm.split(' ')
                j = int(j_)

                res += 'frame: %d\n' % j
                surf = layer.get_surface()
                frame = Surface4bpp.from_pygame_surface(surf, palette = ennemy_palette)

                rects = tools.plugins.best_splitter.splitter(frame, splitters)
                print rects
                res += 'split: [%s]\n\n' % (' ; '.join([str(x) for x in rects]))

        print res
        exit()

    if True:
        # generating patterns    
        psd = load_psd('%s/sheet.psd' % base_dir)
    
        splits = read_split_file('%s/split.txt' % base_dir)
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
    
    

        
