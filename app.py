from db import DataBase
from random import choice
from requests import get, exceptions
from string import ascii_letters, digits
from flask import Flask, render_template, redirect, request


app = Flask(__name__)
db = DataBase()


@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method=='GET':
		return render_template('index.html')

	else:
		data = {}

		data['link'] = request.form['link']

		try:
			get(data['link'])

			symbols = ascii_letters + digits

			while True:

				data['code'] = ''

				for i in range(7):
					data['code'] += choice(symbols)

				if not db.return_unit(data['code']):
					db.write(data['code'], data['link'])
					break

			return render_template('result.html', data=data)

		except exceptions.MissingSchema:
			return render_template('index.html')


@app.route('/<code>')
def redirect_to_link(code):
	unit = db.return_unit(code)

	if unit:
		return redirect(unit[0][1])

	else:
		return redirect('/')


if __name__ == '__main__':
	app.run()
