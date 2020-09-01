from requests import get, exceptions
from flask import Flask, render_template, redirect, request, jsonify

from db import DataBase
from func import new_link

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

			data['code'] = new_link(data['link'], db)

			return render_template('result.html', data=data)

		except exceptions.MissingSchema:
			return render_template('index.html')


@app.route('/<code>')
def redirect_to_link(code):
	unit = db.return_unit(code)

	if unit:
		return redirect(unit[1])

	else:
		return redirect('/')


@app.route('/api/new_link')
def api_new_link():
	if 'link' in request.args:

		link = request.args['link']
		code = new_link(link, db)

		return jsonify({
			'link': link, 
			'code': code
			})


if __name__ == '__main__':
	app.run()
