# log functions, for debug purpose

buffer = []
state = 0
updatables = []
displayables = []

def set_state(flags):
	global state
	state = flags

def write(flags, text):
	global buffer
	
	if state & flags != 0:
		buffer += [text]
		# print (text)

def refresh_max_updatables(v):
	global updatables
	
	updatables += [v]
	
	
def save():
	global max_updatables
	
	with open('debug/log.txt', 'w') as f:
		f.write('\n'.join(buffer))
	
	print ('max updatables: %s' % max(updatables))
	print ('max displayables: %s' % max(displayables))
