import pygame

source_dir = 'C:/Users/fterr/Documents/hack/Shinobi/maps/0-2'

w = h = 1024
numbers = pygame.image.load('%s/numbers.png' % source_dir)
bg_1 = pygame.Color('magenta')
bg_2 = pygame.Color('green')
fg_1 = pygame.Color('white')
fg_2 = pygame.Color('yellow')
fg_3 = pygame.Color('cyan')
fg_4 = pygame.Color('pink')

numbers_list = [numbers.subsurface((i*8, 0, 8, 8)) for i in range(16)]
ck = numbers.get_at((0, 0))
res = pygame.Surface((w, h))
# res.set_colorkey(ck)

j = 0
for y in range(0, h, 16):
	i = 0
	for x in range(0, w, 16):
		fg_col = [fg_1, fg_2, fg_3, fg_4][2*((i >> 4) & 1) + ((j >> 4) & 1)]
		
		msb = numbers_list[j & 15].copy()
		msb.fill(fg_col, special_flags = pygame.BLEND_MULT)
		lsb = numbers_list[i & 15].copy()
		lsb.fill(fg_col, special_flags = pygame.BLEND_MULT)
		msb.set_colorkey(pygame.Color('black'))
		# print (lsb.get_at((0, 0)))
		# lsb.set_colorkey(lsb.get_at((0, 0)))
		
		res.fill([bg_1, bg_2][(i + j) & 1], (x, y, 16, 16))
		res.blit(msb, (x, y + 4))
		res.blit(lsb, (x + 8, y + 4))
		i += 1
	j += 1

pygame.image.save(res, '%s/layer_a.png' % source_dir)
