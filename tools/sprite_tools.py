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
    base_dir = 'C:/Users/Tryphon/Documents/hack/Shinobi/sheets/musashi2'
    
    if True:
        anims = load_animdefs('%s/animdefs.txt' % base_dir)

        print anims

        res = ''
        res2 = 'animations_table = [\n'
        res2_ = []
        for name in anims.keys():
            anim = anims[name]
            if not 'hflip' in anim:
                res += ('%s = %s\n' % (name, anim['steps'] + [(-1, 0)]))
                res2_ += ['\t' + name]

        print res
        res2 += ',\n'.join(res2_) + '\n]\n'
        print res2
        exit()


    print 'loading psd file'
    psd = load_psd('%s/sheet2.psd' % base_dir)
    print psd
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
    
    

        
