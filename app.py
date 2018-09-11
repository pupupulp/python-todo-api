#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

tasks = [
	{
		'id': 1,
		'title': u'Python API Development',
		'description': 'Study different approach and frameworks used to develop API using python',
		'done': False
	},
	{
		'id': 2,
		'title': u'GCP Machine Learning Development',
		'description': 'Study different application and approach on machine learning for finance systems',
		'done': False
	},
]

@app.route('/todo/api/v1/tasks', methods = ['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(404)
	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	tasks.append(task)
	return jsonify({'tasks': task}), 201

@app.route('/todo/api/v1/tasks', methods = ['GET'])
def get_tasks():
	return jsonify({'tasks': tasks})

@app.route('/todo/api/v1/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug = True)