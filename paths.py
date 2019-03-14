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
				if str(board.name) == 'pins':
					print(str(board.name))
				else:
					vbp.append(board)

# Valid pins
def valid_pins(path, vpp):
	for pin in path.iterdir():
		if pin.is_dir():
			if has_file(pin, 'image.jpg') and has_file(pin, 'source.html'):
				# print(pin)
				vpp.append(pin)

def savePath(path, fname, conj):
	a = list(conj)
	a.sort()
	with open(path + fname, 'w') as f:
		for item in a:
			f.write("%s\n" % item)


def main():
	# path de origen
	p = Path('./data')
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
	# pins únicos válidos
	u_pins = set()
	for pin in v_pins:
		u_pins.add(pin.name)
	# boards validos
	v_boards = set()
	for x in v_pins:
		v_boards.add(x.parent)
	# users validos
	v_users = set()
	for x in v_boards:
		v_users.add(x.parent)

	pathDir = str(p) + '-paths/'
	savePath(pathDir, 'unique_pins.txt', u_pins)
	savePath(pathDir, 'valid_boards.txt', v_boards)
	savePath(pathDir, 'valid_pins.txt', v_pins)
	savePath(pathDir, 'valid_users.txt', v_users)


if __name__ == '__main__':
	main()