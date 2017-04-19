from object import *
from tsprite import *
from genepy import *
from res.musashi_data import *
from res import projectiles


def init_object():
	print('init musashi')
	self = allocate_object()
	self.name = "musashi"
	friend_objects.add(self)

	self.status = ACTIVE

	self.x = 512
	self.y = 127
	self.floor = 1

	self.back = -10
	self.front = 10

	self.param1 = 0	# counter for hijumps
	self.param2 = 0 # temp floor

	self.sprite = sprite = allocate_dynamic_sprite()
	sprite.name = "sprite %s" % self.name

	sprite.vpos ^= 0x8000
	sprite.status = 1
	sprite.x = self.x
	sprite.y = self.y
	sprite.patterns = load_data_from_png('res/musashi_patterns.png')
	sprite.frames_table = frames_table
	sprite.animations_table = animations_table
	sprite.bboxes_table = bounding_boxes
	sprite.hitboxes = hitboxes

	sprite.frame = 76
	sprite.patterns_blocks = patterns_blocks
	sprite.bbox = (-6, 0, 16, 64)

	init_stand(self)


def init_stand(self):
	# print 'init_stand'
	set_animation(self.sprite, STAND)
	set_physics(self, 0, 0, 0, 0)
	self.moves_to_left = self.sprite.is_flipped

	self.update_function = update_stand
	self.collision_function = init_collision
	self.hit_function = init_death


def update_stand(self):
	# print 'update_stand'
	if not (collides_background(self, self.front, 1) or
			collides_background(self, self.back, 1)):
		init_fall(self)
	elif (Globs.joy_pressed & BUTTON_B):
		init_fire(self)
	elif (Globs.joy_pressed & BUTTON_C):
		init_jump(self)
	# if FWD pressed, we have to check there's no wall 1 pixel forward
	elif (Globs.joy & Globs.forward)\
			and collides_background(self, self.front + 1, 0) == 0:
		# print "x = %s, dx = %s, x_ = %s : let's walk forward!" % (self.x, self.front + 1, self.x + signate(self, self.front + 1))
		init_walk(self)
	elif Globs.joy & Globs.backward:
		# print "x = %s, dx = %s : let's walk backward!" % (self.x, self.front)
		flip_controls()
		flip(self)
		init_walk(self)
	elif Globs.joy & BUTTON_UP:
		init_prepare_hijump_up(self)
	elif Globs.joy & BUTTON_DOWN:
		init_crouch(self)


def init_fire(self):
	set_physics(self, 0, 0, 0, 0)
	# print 'fire %d' % self.sprite.frame
	# if check_box_on_objects(self, high_close_attack_box, ennemy_objects):
	if is_near(self, 48, 48, ennemy_objects):
		set_animation(self.sprite, PUNCH)
	else:
		set_animation(self.sprite, walk_fire_anims[self.sprite.frame])
		throw_shuriken(self, 32, -48)
	self.update_function = update_fire


def update_fire(self):
	if self.sprite.is_animation_over:
		init_stand(self)


def throw_shuriken(self, dx, dy):
	shuriken = projectiles.init_object()
	shuriken.x = self.x + signate(self, dx)
	shuriken.y = self.y + dy
	shuriken.floor = self.floor
	shuriken.speed_x = signate(self, 4)
	shuriken.sprite.is_flipped = self.sprite.is_flipped
	# print 'throw .x = %d, .speed = %d, .front = %d' % (shuriken.x, shuriken.speed_x, shuriken.front)


def init_walk(self):
	# print 'init_walk'
	set_animation(self.sprite, WALK)
	set_physics(self, 2, 0, 0, 0)
	self.update_function = update_walk


def update_walk(self):
	# print 'update_walk'
	if not (Globs.joy & Globs.forward):
		init_stand(self)
	elif (Globs.joy_pressed & BUTTON_B):
		init_fire(self)
	elif (Globs.joy_pressed & BUTTON_C):
		init_jump(self)
	elif Globs.joy & BUTTON_DOWN:
		init_crawl(self)
	else:
		self.x += self.speed_x
		# print 'collision:', collides_background(self, self.front, 0)
		# print 'moving: x = %d' % self.x

		if not (collides_background(self, self.front, 1) or
				collides_background(self, self.back, 1)):
			init_fall(self)
		elif collides_background(self, self.front, 0):
			# print 'collision'
			fix_hpos(self)
			init_stand(self)


def init_prepare_hijump_up(self):
	set_animation(self.sprite, HIJUMP_PREPARATION)
	self.speed_y = 0
	self.accel_y = 0
	self.update_function = update_prepare_hijump_up


def update_prepare_hijump_up(self):
	if not (Globs.joy & BUTTON_UP):
		init_stand(self)
	elif Globs.joy_pressed & BUTTON_C:
		if get_hijump_impulsion(self):
			init_hijump_up(self)
		else:
			init_jump(self)


def init_hijump_up(self):
	self.speed_y = self.accel_y = 0
	set_animation(self.sprite, HIJUMP0)
	self.update_function = update_hijump_up
	self.collision_function = None
	self.param2 = self.floor + 1


def update_hijump_up(self):
	if self.sprite.is_animation_over:
		init_hijump1_up(self)


def init_hijump1_up(self):
	self.speed_y = get_hijump_impulsion(self)
	print ('initial speed: %f' % self.speed_y)
	self.accel_y = 0.5
	set_animation(self.sprite, HIJUMP1)
	self.update_function = update_hijump1_up
	self.param1 = 8


def update_hijump1_up(self):
	self.param1 -= 1
	if self.param1 > 0:
		self.param1 -= 1
		if self.param1 == 0:
			self.floor += 1
			self.floor |= 0x80
	
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y >= 0:
		self.param1 = 2
		init_hifall(self)


def init_crouch(self):
	set_animation(self.sprite, CROUCH_NO_MOVE)
	self.speed_y = 0
	self.accel_y = 0
	self.update_function = update_crouch


def update_crouch(self):
	if not (Globs.joy & BUTTON_DOWN):
		init_stand(self)
	elif Globs.joy & Globs.backward:
		flip_controls()
		flip(self)
		init_crawl(self)
	elif Globs.joy_pressed & BUTTON_B:
		init_crouch_fire(self)
	elif Globs.joy_pressed & BUTTON_C:
		if self.floor > 1:
			init_hijump_down(self)
		else:
			init_jump(self)
	elif Globs.joy & Globs.forward\
			and collides_background(self, self.front + 1, 0) == 0:
		init_crawl(self)


def init_crawl(self):
	set_physics(self, 1, 0, 0, 0)
	set_animation(self.sprite, CROUCH)
	self.update_function = update_crawl


def update_crawl(self):
	if not (Globs.joy & BUTTON_DOWN):
		init_stand(self)
	elif not (Globs.joy & Globs.forward):
		init_crouch(self)
	elif Globs.joy_pressed & BUTTON_B:
		init_crouch_fire(self)
	elif Globs.joy_pressed & BUTTON_C:
		if self.floor > 1:
			init_hijump_down(self)
		else:
			init_jump(self)
	else:
		self.x += self.speed_x
		# print 'collision:', collides_background(self, self.front, 0)
		# print 'moving: x = %d' % self.x

		if not (collides_background(self, self.front, 1) or
				collides_background(self, self.back, 1)):
			init_fall(self)
		elif collides_background(self, self.front, 0):
			# print 'collision'
			fix_hpos(self)
			init_crouch(self)


def init_crouch_fire(self):
	set_physics(self, 0, 0, 0, 0)
	# print 'fire %d' % self.sprite.frame
	if is_near(self, 40, 24, ennemy_objects):
		set_animation(self.sprite, KICK)
	else:
		set_animation(self.sprite, crouch_fire_anims[self.sprite.frame - 17])
		throw_shuriken(self, 32, -24)
	self.update_function = update_crouch_fire


def update_crouch_fire(self):
	if self.sprite.is_animation_over:
		init_crouch(self)


def init_hijump_down(self):
	set_animation(self.sprite, HIFALL0)
	self.update_function = update_hijump_down


def update_hijump_down(self):
	if self.sprite.is_animation_over:
		init_hijump1_down(self)


def init_hijump1_down(self):
	self.speed_y = -6
	self.accel_y = 0.5
	set_animation(self.sprite, HIFALL1)
	self.update_function = update_hijump1_down


def update_hijump1_down(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y >= 0:
		self.floor -= 1
		self.floor |= 0x80
		self.param1 = 28
		init_hifall(self)


def init_hifall(self):
	self.sprite.vpos ^= 0x8000
	self.update_function = update_hifall
	self.collision_function = init_collision


def update_hifall(self):
	print (self.param1, self.floor)
	if self.param1 > 0:
		self.param1 -= 1
		if self.param1 == 0:
			self.floor &= 0x7F

	self.speed_y += self.accel_y
	self.y += self.speed_y
	if collides_background(self, self.front, 1) or\
			collides_background(self, self.back, 1):
		fix_vpos(self)
		self.floor &= 0x7F
		init_stand(self)


def init_jump(self):
	# print 'init_jump:',
	set_animation(self.sprite, JUMP)
	self.speed_y = -8.5
	self.accel_y = 0.5
	self.update_function = update_jump


def clamp(val, min_, max_):
	return min_ if val < min_ else max_ if val > max_ else val


def update_jump_action(self):
	self.accel_x = 0
	if Globs.joy & Globs.forward:
		self.accel_x = signate(self, 0.125)
	elif Globs.joy & Globs.backward:
		self.accel_x = signate(self, -0.125)

	self.speed_x += self.accel_x
	self.speed_x = clamp(self.speed_x, -2, 2)
	self.x += self.speed_x

	if self.moves_to_left:
		if self.speed_x > 0:
			flip_controls()
			flip(self)
	elif self.speed_x < 0:
			flip_controls()
			flip(self)


def update_jump_position(self):
	update_jump_action(self)
	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = 0


def update_fall_position(self):
	update_jump_action(self)

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = 0

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0) or\
			collides_background(self, self.back, 0):
		fix_vpos(self)
		init_stand(self)


def update_jump(self):
	# print 'update_jump:',
	if self.speed_y >= 0:
		init_fall(self)
	elif Globs.joy_pressed & BUTTON_B:
		init_jump_fire(self)
	update_jump_position(self)


def init_jump_fire(self):
	# print 'init_jump_fire:',
	set_animation(self.sprite, JUMP_FIRE)
	throw_shuriken(self, 32, -48)
	self.update_function = update_jump_fire


def update_jump_fire(self):
	# print 'update_jump_fire:',
	if self.sprite.is_animation_over:
		set_animation(self.sprite, JUMP)
		self.update_function = update_jump
	elif self.speed_y >= 0:
		change_animation(self.sprite, FALL_FIRE)
		self.update_function = update_fall_fire
	update_jump_position(self)


def init_fall(self):
	# print 'init_fall:',
	set_animation(self.sprite, FALL)
	self.accel_y = 0.5
	self.update_function = update_fall


def update_fall(self):
	# print 'update_fall:',
	if Globs.joy_pressed & BUTTON_B:
		init_fall_fire(self)
	else:
		update_fall_position(self)


def init_fall_fire(self):
	# print 'init_fall_fire:',
	set_animation(self.sprite, FALL_FIRE)
	throw_shuriken(self, 32, -48)
	self.update_function = update_fall_fire


def update_fall_fire(self):
	# print 'update_fall_fire:',
	if self.sprite.is_animation_over:
		set_animation(self.sprite, FALL)
		self.update_function = update_fall
	update_fall_position(self)



def init_collision(self):
	# print 'musashi collided'
	other = self.collided_object
	
	generic_collision(self)

	self.speed_y = -4
	self.accel_y = 0.5

	set_animation(self.sprite, HIT)
	self.update_function = update_collision

def init_death(self):
	# print 'musashi collided'
	other = self.hit_object

	generic_collision(self)

	self.speed_y = -4
	self.accel_y = 0.5

	set_animation(self.sprite, HIT)
	self.update_function = update_collision

	
def update_collision(self):
	self.x += self.speed_x

	if collides_background(self, self.front, 0):
		# print 'before:', (self.x, self.back, self.front)
		fix_hpos(self)
		# print 'after:', (self.x, self.back, self.front), '\n'
		self.speed_x = 0

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if collides_background(self, self.front, 0):
		fix_vpos(self)
		init_stand(self)



