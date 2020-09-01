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

			data['new_link'] = new_link(data['link'], db)

			return render_template('result.html', data=data)

		except exceptions.MissingSchema:
			return render_template('index.html')

		except exceptions.ConnectionError:
			return render_template('index.html')

		except exceptions.InvalidURL:
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

		try:
			get(link)

			short_link = new_link(link, db)

			return jsonify({
				'error': '',
				'link': link, 
				'short_link': short_link
				})

		except exceptions.ConnectionError:
			return jsonify({'error': 'invalid link'})

		except exceptions.MissingSchema:
			return jsonify({'error': 'invalid link'})

		except exceptions.InvalidURL:
			return jsonify({'error': 'invalid link'})

	else: 
		return jsonify({'error': 'request hasn\'t link'})


if __name__ == '__main__':
	app.run()
