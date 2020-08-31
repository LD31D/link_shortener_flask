from random import choice
from string import ascii_letters, digits

from db import DataBase


def create_code():
	symbols = ascii_letters + digits

	code = ''
	for i in range(7):
		code += choice(symbols)

	return code


def new_link(link: str, db=DataBase()):
	while True:
		code = create_code()

		if not db.return_unit(code):
			db.write(code, link)
			break

	return code
