from object import *
from tsprite import *
from genepy import *

from res.chars.musashi_data import *
from res.levels import all_levels

from chars import projectiles
from chars import more_objects
from chars import common


def init(entry):
	print('init and activate musashi')
	_, floor, x, y, dir, _ = entry
	self = allocate_object(objects)
	self.name = "musashi"
	friend_objects.add(self)

	self.status = ACTIVE
	
	# temporaire
	self.is_initialized = True
	self.is_activated = True
	self.is_displayable = True
	self.is_collidable = True

	self.org_x = x
	self.org_y = y

	self.x = x
	self.y = y
	self.floor = floor

	Globs.musashi = self
	print ('Globs.musashi = %s' % Globs.musashi)
	all_objects.add(self)
	
	self.back = -10
	self.front = 10
	self.global_display_box = (-16, -63, 32, 64)

	self.param1 = 0	# counter for hijumps
	self.param2 = 0 # temp floor

	sprite = allocate_dynamic_sprite()
	sprite.name = "sprite %s" % self.name

	sprite.vpos |= Globs.stage_priority
	sprite.status = 1
	sprite.x = self.x
	sprite.y = self.y
	sprite.data = sprite_data

	sprite.frame = 76
	sprite.bbox = (-6, 0, 16, 64)

	self.sprite = sprite
	init_stand(self)

def activate(self):
	pass


def init_stand(self):
	# print 'init_stand'
	set_animation(self.sprite, STAND)
	set_physics(self, 0, 0, 0, 0)
	Globs.vscroll_mode = 0
	# self.moves_to_left = self.sprite.is_flipped

	self.update_function = update_stand
	self.collision_function = init_collision
	self.hit_function = init_death


def update_stand(self):
	print ('update_stand')
	if not (collides_background(self, self.front, 1) or
			collides_background(self, self.back, 1)):
		# print ('fall (coll = %X)' % collides_background(self, self.front, 1) or
			# collides_background(self, self.back, 1))
		init_fall(self)
	elif (Globs.joy_pressed & BUTTON_B):
		init_fire(self)
	elif (Globs.joy_pressed & BUTTON_C):
		init_jump(self)
	# if FWD pressed, we have to check there's no wall 1 pixel forward

	elif Globs.joy & BUTTON_RIGHT:
		common.faces_right(self)
		if collides_background(self, self.front + 1, 0) == 0:
			init_walk(self)

	elif Globs.joy & BUTTON_LEFT:
		common.faces_left(self)
		if collides_background(self, self.front + 1, 0) == 0:
			init_walk(self)

	elif Globs.joy & BUTTON_UP:
		init_prepare_hijump_up(self)
	elif Globs.joy & BUTTON_DOWN:
		init_crouch(self)


standing_close_box = (0, -48, 56, 32)

def init_fire(self):
	set_physics(self, 0, 0, 0, 0)
	# print 'fire %d' % self.sprite.frame
	# if check_box_on_objects(self, high_close_attack_box, ennemy_objects):
	if is_near(self, standing_close_box, ennemy_objects):
		set_animation(self.sprite, PUNCH)
	else:
		set_animation(self.sprite, walk_fire_anims[self.sprite.frame])
		throw_shuriken(self, 32, -47)
	self.update_function = update_fire


def update_fire(self):
	if self.sprite.is_animation_over:
		init_stand(self)


def throw_shuriken(self, dx, dy):
	shuriken = projectiles.init_object()
	shuriken.sprite.vpos |= (self.sprite.vpos & 0x8000)
	shuriken.y = self.y + dy
	shuriken.floor = self.floor
	shuriken.attack_type = self.attack_type | 2
	if self.moves_to_left:
		shuriken.x = self.x - dx
		shuriken.speed_x = -4
		shuriken.moves_to_left = shuriken.sprite.is_flipped = True
	else:
		shuriken.x = self.x + dx
		shuriken.speed_x = 4
		shuriken.moves_to_left = shuriken.sprite.is_flipped = False
	print ('shuriken: %s, %s' % (self.moves_to_left, shuriken.speed_x))
	


def init_walk(self):
	set_physics(self, 0, 0, 0, 0)
	if Globs.joy & BUTTON_LEFT:
		common.moves_left(self, -2)
	elif Globs.joy & BUTTON_RIGHT:
		common.moves_right(self, 2)
		
	set_animation(self.sprite, WALK)
	self.update_function = update_walk


def update_walk(self):
	# print 'update_walk'
	if self.moves_to_left and not (Globs.joy & BUTTON_LEFT):
		init_stand(self)

	elif (not self.moves_to_left) and not (Globs.joy & BUTTON_RIGHT):
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
	self.is_collidable = False
	self.collision_function = None
	Globs.vscroll_mode = 1


def update_hijump_up(self):
	if self.sprite.is_animation_over:
		init_hijump1_up(self)


def init_hijump1_up(self):
	self.speed_y = get_hijump_impulsion(self)
	print ('initial speed: %f' % self.speed_y)
	self.accel_y = 0.5
	set_animation(self.sprite, HIJUMP1)
	self.update_function = update_hijump1_up
	self.param1 = 8 # timer before leaving lower floor


def update_hijump1_up(self):
	# self.param1 -= 1
	if self.param1 > 0:
		self.param1 -= 1
		if self.param1 <= 0:
			self.floor += 1
			self.floor |= 0x80	# now on current_floor, but not detectable
	
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y >= 0:
		self.param1 = 2
		self.sprite.vpos &= 0x7FFF
		init_hifall(self)


def init_crouch(self):
	set_animation(self.sprite, CROUCH_NO_MOVE)
	set_physics(self, 0, 0, 0, 0)
	self.update_function = update_crouch


def update_crouch(self):
	if not (Globs.joy & BUTTON_DOWN):
		init_stand(self)

	elif Globs.joy & BUTTON_LEFT:
		common.faces_left(self)
		if collides_background(self, self.front + 1, 0) == 0:
			init_crawl(self)

	elif Globs.joy & BUTTON_RIGHT:
		common.faces_right(self)
		if collides_background(self, self.front + 1, 0) == 0:
			init_crawl(self)

	elif Globs.joy_pressed & BUTTON_B:
		init_crouch_fire(self)
	elif Globs.joy_pressed & BUTTON_C:
		if get_hijump_down_impulsion(self):
			init_hijump_down(self)
		else:
			init_jump(self)


def init_crawl(self):
	set_physics(self, 1, 0, 0, 0)
	set_animation(self.sprite, CROUCH)
	self.update_function = update_crawl


def update_crawl(self):
	if not (Globs.joy & BUTTON_DOWN):
		init_stand(self)
	elif not (Globs.joy & (BUTTON_LEFT | BUTTON_RIGHT)):
		init_crouch(self)
	elif Globs.joy_pressed & BUTTON_B:
		init_crouch_fire(self)
	elif Globs.joy_pressed & BUTTON_C:
		if get_hijump_down_impulsion(self):
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

crouch_close_attack = (0, -24, 40, 32)

def init_crouch_fire(self):
	set_physics(self, 0, 0, 0, 0)
	# print 'fire %d' % self.sprite.frame
	if is_near(self, crouch_close_attack, ennemy_objects):
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
	Globs.vscroll_mode = 1


def update_hijump_down(self):
	if self.sprite.is_animation_over:
		init_hijump1_down(self)


def init_hijump1_down(self):
	self.speed_y = get_hijump_down_impulsion(self)
	self.accel_y = 0.5
	set_animation(self.sprite, HIFALL1)
	self.update_function = update_hijump1_down


def update_hijump1_down(self):
	self.speed_y += self.accel_y
	self.y += self.speed_y
	if self.speed_y >= 0:
		self.floor -= 1
		self.floor |= 0x80	# now on lower floot, but not detectable
		self.param1 = 28	# timer before becoming detectable
		self.sprite.vpos |= 0x8000
		init_hifall(self)


def init_hifall(self):
	self.is_collidable = True
	self.update_function = update_hifall
	self.collision_function = init_collision


def update_hifall(self):
	# print (self.param1, self.floor)
	if self.param1 > 0:
		self.param1 -= 1
		if self.param1 <= 0:
			self.floor &= 0x7F

	self.speed_y += self.accel_y
	self.y += self.speed_y
	# if collides_background(self, self.front, 1) or\
			# collides_background(self, self.back, 1):
		# fix_vpos(self)
	if handle_fall(self):
		self.floor &= 0x7F
		init_stand(self)


def init_jump(self):
	# print 'init_jump:',
	set_animation(self.sprite, JUMP)
	self.speed_y = -9 #-8.5
	self.accel_y = 0.5
	self.update_function = update_jump
	Globs.vscroll_mode = 1


def clamp(val, min_, max_):
	return min_ if val < min_ else max_ if val > max_ else val


def update_jump_action(self):
	self.accel_x = 0
	if Globs.joy & BUTTON_LEFT:
		ax = -0.125
	elif Globs.joy & BUTTON_RIGHT:
		ax = .125
	else:
		ax = 0

	self.speed_x += ax
	self.speed_x = clamp(self.speed_x, -2, 2)
	self.x += self.speed_x

	if self.moves_to_left:
		if self.speed_x > 0:
			common.faces_right(self)
	elif self.speed_x < 0:
		common.faces_left(self)


def update_jump_position(self):
	update_jump_action(self)
	
	old_y = self.y
	self.speed_y += self.accel_y
	self.y += self.speed_y
	
	if Globs.level == all_levels.LEVEL_2_3:
		more_objects.check_splash(self.x, old_y, self.y)
	
	if self.y < 0:
		self.speed_y = 0
		self.y = 0

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = 0


def update_fall_position(self):
	update_jump_action(self)

	if collides_background(self, self.front, 0):
		fix_hpos(self)
		self.speed_x = 0

	old_y = self.y
	self.speed_y += self.accel_y
	self.y += self.speed_y
	
	# @TODO: conditionnal
	
	if Globs.level == all_levels.LEVEL_2_3:
		more_objects.check_splash(self.x, old_y, self.y)

	print ('@')
	
	if handle_fall(self):
		print ('FALL END')
		init_stand(self)

	
	# coll = collides_background(self, self.front, 0) | collides_background(self, self.back, 0)
	# print ('coll: %X' % self.coll_value)
	# if coll:
		# print ('!')
		# fix_vpos(self)
		# init_stand(self)


def update_jump(self):
	print ('musashi vpos = %X' % self.sprite.vpos)
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
	self.speed_y = 0.5
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
	other = self.other_object

	# commented, use impulsion instead
	# if self.x < other.x:
		# self.speed_x = -2
	# else:
		# self.speed_x = 2
	if self.impulsion_x > 0:
		self.speed_x = 2
	else:
		self.speed_x = -2
	
	self.speed_y = -4
	self.accel_y = 0.5

	set_animation(self.sprite, HIT)
	self.update_function = update_collision

def init_death(self):
	# print 'musashi collided'
	init_collision(self)

	
def update_collision(self):
	print ('[musashi] update_collision')
	self.x += self.speed_x

	if collides_background(self, self.front, 0)\
	or collides_background(self, self.back, 0):
		# print 'before:', (self.x, self.back, self.front)
		fix_hpos(self)
		# print 'after:', (self.x, self.back, self.front), '\n'
		# self.speed_x = 0

	self.speed_y += self.accel_y
	self.y += self.speed_y

	if self.speed_y > 0:
		# coll = collides_background(self, self.front, 1) | collides_background(self, self.back, 1)
		# if coll & 7:
			# print (self.speed_y)
			# print ('front = %d, back = %d' % (self.front, self.back))
			# # GP.halt()
			# fix_vpos(self)
		if handle_fall(self):
			self.floor &= 0x7F	# when collided during hijump, must become detectable
			init_stand(self)



