size = 32
# a = [0xB0C152F9, 0xEBF2831F]
a = [0xEBF2831F, 0xB0C152F9]
b = [0, 0, 0, 0]

def binary_to_polynom(b):
	res = []
	for i in range(32):
		res += [b & 1]
		b = b >> 1
	res.reverse()
	return res
	
def poly_deg(p):
	return len(p) - 1

def poly_coef(p, i):
	if i >= len(p):
		return 0
	return p[i]

def poly_mul(a, b):
	da = poly_deg(a)
	db = poly_deg(b)
	
	res = []
	for i in range(da + db + 1):
		c = 0
		for j in range(i + 1):
			c += poly_coef(a, j) * poly_coef(b, i - j)
		res += [c & 1]
	return res

def monom_to_str(c, i):
	if i == 0:
		return str(c)
	if c == 1:
		c_ = ''
	else:
		c_ = str(c)
	if i == 1:
		return '%sX' % c_
	else:
		return '%sX^%d' % (c_, i)

def poly_print(p):
	res = []
	for i, c in enumerate(reversed(p)):
		if c:
			res += [monom_to_str(c, i)]
	if res:
		print (' + '.join(reversed(res)))
	else:
		print ('0')

		
p = [1, 1, 1]
p1 = binary_to_polynom(a[0])
p2 = binary_to_polynom(a[1])

poly_print (p1)
poly_print (p2)

q = poly_mul(p1, p2)
poly_print(q)

res = []
for k in range(256):
	for l in range(k, 256):
		a = binary_to_polynom(k)
		b = binary_to_polynom(l)
		c = poly_mul(a, b)
		if c not in res:
			res += [c]
			
print (len(res))
exit()

def poly_to_binary(p, n):
	res = 0
	for d in p: #reversed(p):
		res = res << 1
		res += d
	return res
	

x1 = poly_to_binary(p1, 32)
x2 = poly_to_binary(p2, 32)
y = poly_to_binary(q, 64)

print ('%X * %X = %X' % (x1, x2, y))

exit()

def encode(a, size):
	b = [0, 0]
	for i in range(size):
		for j in range(size):
			mask = ((a[i//32] >> (i%32)) & (a[j//32 + size//32] >> (j % 32)) & 1) << ((i + j)%32)
			b[(i + j)//32] ^= mask
	
	return b

if False:
	print (' '.join(['%08X' %x for x in a]))
	b = encode(a, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	b = encode(b, 32)
	print (' '.join(['%08X' %x for x in b]))
	exit()

ops = []
for i in range(size):
	for j in range(size):
		mask = ((a[i//32] >> (i%32)) & (a[j//32 + size//32] >> (j % 32)) & 1) << ((i + j)%32)
		# print ('b[%d] ^= (a[%d] & a[%d])' % ((i + j)//32 * 32 + (i + j) % 32, (i // 32)*32 + i%32, (j // 32 + size // 32)*32 + (j % 32))) 
		# print ('b[%d] ^= (a[%d] & a[%d])' % (i + j, i, j + size))
		ops += [(i + j, i, j + size)]
		print ("b[%d] ^= %08X = ((a[%d] >> %d) & (a[%d] >> %d) & 1) << %d" % ((i + j)//32, mask, i//32, i%32, j//32 + 1, j%32, (i + j)%32))
		b[(i + j)//32] ^= mask

ops.sort()

for op in ops:
	print ('b[%d] ^= (a[%d] & a[%d])' % op)
		


print (' '.join(['%08X' %x for x in a]))
print (' '.join(['%08X' %x for x in b]))
