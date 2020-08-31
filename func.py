from random import choice
from string import ascii_letters, digits


def create_code():
	symbols = ascii_letters + digits

	code = ''
	for i in range(7):
		code += choice(symbols)

	return code
