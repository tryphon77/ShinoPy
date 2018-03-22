from genepy import GP
from globals import Globs


TSPRITE_VPOS = 0x2C0
NONE = 0
ACTIVE = 1

class TSpriteData():
	def __init__(self, patterns, frames_table, patterns_blocks, animations_table, bboxes_table, hitboxes_table, bounding_box, name):
		self.patterns = patterns
		self.frames_table = frames_table
		self.patterns_blocks = patterns_blocks
		self.animations_table = animations_table
		self.bboxes_table = bboxes_table
		self.hitboxes_table = hitboxes_table
		self.bounding_box = bounding_box
		self.name = name
	
	def __str__(self):
		return 'name: %s, patterns: %s, frames_table: %s, patterns_blocks: %s, animations_table: %s, bboxes_table: %s, hitboxes_table: %s' % (self.name, self.patterns, self.frames_table, self.patterns_blocks, self.animations_table, self.bboxes_table, self.hitboxes_table)


class TSprite():
	def __init__(self, vpos):
		self.status = NONE
		self.is_viewable = False
		
		self.data = None
		
		self.is_dynamic = False
		self.is_flipped = False
		self.vpos = vpos
		self.needs_refresh_patterns = False
		self.new_frame = False

		self.x = 0
		self.y = 0

		# self.patterns = None
		# self.frames_table = None
		# self.patterns_blocks = None
		self.frame = 0

		# self.animations_table = None
		self.animation = None
		self.animation_index = -1
		self.animation_id = -1
		self.animation_tick = 0
		self.tick = 0
		self.total_ticks_in_animation = 0
		self.is_last_tick = False
		self.is_animation_starting = False
		self.is_animation_over = False

		# self.bboxes_table = None
		# self.hitboxes_table = None
		self.bbox = None
		self.hitbox = None
		
		self.bounding_box = None


dynamic_sprites_size = 8
dynamic_sprites = [TSprite(TSPRITE_VPOS + i*0x30) for i in range(dynamic_sprites_size)]

static_sprites_size = 32
static_sprites = [TSprite(0) for _ in range(static_sprites_size)]

def allocate_tiles(patterns):
	vpos = Globs.static_tiles
	GP.load_tile_data(patterns, vpos)
	Globs.static_tiles += len(patterns)
	return vpos


def allocate_dynamic_sprite():
	for i, s in enumerate(dynamic_sprites):
		if s.status == 0:
			# print ('allocating dynamic sprite #%d' % i)
			s.is_dynamic = True
			return s
	print ("couldn't allocate dynamic sprite")
	GP.halt()
	return None

def allocate_static_sprite():
	for i, s in enumerate(static_sprites):
		if s.status == 0:
			# print ('allocating static sprite #%d' % i)
			s.is_dynamic = False
			return s
	return None


def release_sprite(self):
	# print 'disabling sprite at (%d, %d)' % (sprite.x, sprite.y)
	self.status = 0
	self.is_flipped = False
	self.animation_index = -1
	self.animation_id = -1
	self.animation_tick = 0
	self.tick = 0
	self.total_ticks_in_animation = 0


def clear_all_sprites():
	for s in dynamic_sprites:
		release_sprite(s)
	
	for s in static_sprites:
		release_sprite(s)

	GP.set_sprite(0, -128, -128, 0, 0, 0)


sizes = [1, 2, 3, 4, 2, 4, 6, 8, 3, 6, 9, 12, 4, 8, 12, 16]


def update_patterns(sprite):
	if sprite.is_viewable:
		# print ('animation: %s frame: %s' % (sprite.animation, sprite.frame))
		start, ln = sprite.data.patterns_blocks[sprite.frame]
		
		# print 'load %d, %d' % (start, ln)
		GP.load_tile_data(sprite.data.patterns[start:start + ln], sprite.vpos & 0x7FF)
	sprite.needs_refresh_patterns = False


def update_frame(sprite):
	if sprite.is_viewable:
		if sprite.is_dynamic:
			update_dynamic_frame(sprite)
		else:
			update_static_frame(sprite)


def update_dynamic_frame(sprite):
	# print 'update_frame: %d at (%d, %d)' % (sprite.frame, sprite.x, sprite.y)
	x = sprite.x
	y = sprite.y
	t_id = sprite.vpos
#    print sprite.frames_table[sprite.frame]

	if sprite.is_flipped:
		t_id |= 0x800
		for (_, dx, dy, sz, dp) in sprite.data.frames_table[sprite.frame]:
			GP.set_sprite(Globs.link,
						  x + dx,
						  y + dy,
						  sz,
						  t_id,
						  Globs.link + 1)
			t_id += sizes[sz]
			Globs.link += 1
	else:
		for (dx, _, dy, sz, dp) in sprite.data.frames_table[sprite.frame]:
			GP.set_sprite(Globs.link,
						  x + dx,
						  y + dy,
						  sz,
						  t_id,
						  Globs.link + 1)
			t_id += sizes[sz]
			Globs.link += 1


def update_static_frame(sprite):
	# print ('[%s] update_static_frame' % (None))
	# print ('update_static_frame: %d at (%d, %d) vpos: %X' % (sprite.frame, sprite.x, sprite.y, sprite.vpos))
	x = sprite.x
	y = sprite.y
	t_id = sprite.vpos
#    print sprite.frames_table[sprite.frame]

	if sprite.is_flipped:
		t_id |= 0x800
		for (_, dx, dy, sz, dp) in sprite.data.frames_table[sprite.frame]:
			GP.set_sprite(Globs.link,
						  x + dx,
						  y + dy,
						  sz,
						  t_id + dp,
						  Globs.link + 1)
			Globs.link += 1
	else:
		for (dx, _, dy, sz, dp) in sprite.data.frames_table[sprite.frame]:
			GP.set_sprite(Globs.link,
						  x + dx,
						  y + dy,
						  sz,
						  t_id + dp,
						  Globs.link + 1)
			Globs.link += 1


def set_animation(self, anim):
	# print ('set_animation: %d' % (anim))
	self.total_ticks_in_animation = 0
	if self.animation_id != anim:
#		self.is_animation_over = False
		self.animation_id = anim
		self.animation = self.data.animations_table[anim]
		self.animation_tick = len(self.animation)
		self.animation_index = 0
		self.is_animation_over = False
		self.new_frame = True
		self.is_animation_starting = True
		load_next_frame(self)


def change_animation(self, anim):
	if self.animation_id != anim:
		self.animation_id = anim
		self.animation = self.data.animations_table[anim]
		self.animation_index -= 1   # recode ?
		# print 'change_animation: animation_index = %d' % (self.animation_index)
		frame_id, _ = self.animation[self.animation_index]

		if self.frame != frame_id:
			self.frame = frame_id
			self.bbox = self.data.bboxes_table[frame_id]
			self.hitbox = self.data.hitboxes_table[frame_id]
			self.needs_refresh_patterns = True

def load_next_frame(self):

	# print 'load_next_frame: id = %d index = %d' % (self.animation_id, self.animation_index)
	self.animation_tick -= 1
	if self.animation_tick < 0:
		self.animation_tick = len(self.animation) - 1
		self.animation_index = 0

	frame_id, ticks = self.animation[self.animation_index]
#    self.bbox = self.bboxes_table[frame_id]
#    print (frame_id, ticks)

	if self.frame != frame_id:
		self.frame = frame_id
		self.bbox = self.data.bboxes_table[frame_id]
		self.hitbox = self.data.hitboxes_table[frame_id]
		self.needs_refresh_patterns = self.is_dynamic

	self.tick = ticks

	self.animation_index += 1


def update_animation(self):
	self.new_frame = False
	self.total_ticks_in_animation += 1
	# print ('update_animation: %s : ticks = %d' % (self.name, self.tick))
	self.is_last_tick = (self.tick == 1)
	if self.tick == 0:
		self.new_frame = True
		load_next_frame(self)
	self.tick -= 1
	self.is_animation_over = (self.animation_tick == 0) and (self.tick == 0)	


def sprite_update(spr):
#    print 'sprite_update:', spr	
	spr.is_animation_starting = False
	if (not spr.is_dynamic) or Globs.is_refresh_available > 0:
		x, y, w, h = spr.data.bounding_box
		left, top = spr.x + x, spr.y + y
		right, bottom = left + w - 1, top + h - 1
		is_viewable = (left < 320) and (right >= 0) and (top < 224) and (bottom >= 0)
		# print ('is_viewable: (%d, %d, %d, %d)' % (left, right, top, bottom)) 
		if not spr.is_viewable and is_viewable:
			spr.is_viewable = True
			spr.needs_refresh_patterns = spr.is_dynamic
		else:
			spr.is_viewable = is_viewable
			
		if spr.status:
			update_animation(spr)
		if spr.needs_refresh_patterns:
			# print 'frame %d: refresh sprite %s' % (GP.frame_counter, spr)
			update_patterns(spr)
			Globs.is_refresh_available -= 1
	else:
		print ('sprite %s delayed' % spr)
	update_frame(spr)

