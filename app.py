#!flask/bin/python
from flask import Flask

app = Flask(__name__)

tasks = [
	{
		'id': 1,
		'title': u'Python API Development',
		'description': 'Study different approach and frameworks used to develop API using python',
		'done': False
	},
	{
		'id': 1,
		'title': u'GCP Machine Learning Development',
		'description': 'Study different application and approach on machine learning for finance systems',
		'done': False
	},
]

@app.route('/todo/api/v1/tasks', methods = ['GET'])

def get_tasks():
	return jsonify({'tasks': tasks})

if __name__ == '__main__':
	app.run(debug = True)