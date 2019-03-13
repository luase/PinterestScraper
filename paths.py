from pathlib import Path

"""
data structure:

	user(s)
		source.html
		board(s)
			source.html
			pin(s)
				image.jpg
				source.html

	first i need to know if a user seems to be is valid.
	rules:
		- it contains at least one board directory
		- it has a source.html

	second i need to know what boards will be usefull, and which ones wont.
	rules:
		- it has a source.html
		- it cointains at least one pin directory

	last i need to know if a pin is valid.
	rules:
		- it doesn't contain any directories
		- it has an image
		- it has a source.html
"""

# funcion para revisar si un directorio contiene el archivo 'source.html'
def has_file(path, file):
	if path / file in path.iterdir():
		return True
	else:
		return False
	
# funcion para revisar si un directorio contiene otros directorios
def has_directory(path):
	hd = False
	for elem in path.iterdir():
		if elem.is_dir():
			hd = True
	return hd

# Valid user paths:
# tiene el elemento source.html y ademas contiene al menos un directorio
def valid_users(path):
	vup = []
	for user in path.iterdir():
		if user.is_dir():
			if has_file(user, 'source.html') and has_directory(user):
				# print(user)
				vup.append(user)
	return vup

# Valid board paths:
# conditions: must have source.html and at least one pin
def valid_boards(path, vbp):
	for board in path.iterdir():
		if board.is_dir():
			if has_file(board, 'source.html') and has_directory(board):
				# print(board)
				vbp.append(board)

# Valid pins
def valid_pins(path, vpp):
	for pin in path.iterdir():
		if pin.is_dir():
			if has_file(pin, 'image.jpg') and has_file(pin, 'source.html'):
				# print(pin)
				vpp.append(pin)


def main():
	# path de origen
	p = Path('./sample')

	# usuarios pre-validados (tienen source.html y directorios)
	pv_users = valid_users(p)

	# boards pre-validados
	pv_boards = []
	for user in pv_users:
		valid_boards(user, pv_boards)

	# pins validos
	v_pins = []
	for board in pv_boards:
		valid_pins(board, v_pins)

	v_pins.sort()
	# # pins únicos válidos
	# u_pins = set()
	# for pin in v_pins:
	# 	u_pins.add(pin.name)

	v_boards = set()
	for x in v_pins:
		v_boards.add(x.parent)

	v_users = set()
	for x in v_boards:
		v_users.add(x.parent)

	a = list(v_users)
	a.sort()
	with open('./sample-paths/invalid_pins.txt', 'w') as f:
		for item in v_pins:
			f.write("%s\n" % item)

	# print('valid pins:', len(v_pins))
	# print('unique pins:', len(u_pins))

	# print('\nprevalidated boards:', len(pv_boards))
	# print('valid boards:', len(v_boards))

	# print('\nprevalidated users:', len(pv_users))
	# print('valid users:', len(v_users))

if __name__ == '__main__':
	main()