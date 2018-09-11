#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'pulp':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)	

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

@app.route('/todo/api/v1/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
	return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1/tasks/<int:task_id>', methods = ['GET'])
@auth.login_required
def get_task(task_id):
	task = filter(lambda task: task['id'] == task_id, tasks)
	if len(task) == 0:
		abort(404)
	return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1/tasks', methods = ['POST'])
@auth.login_required
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
	return jsonify({'tasks': make_public_task(task)}), 201

@app.route('/todo/api/v1/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = filter(lambda task: task['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

if __name__ == '__main__':
	app.run(debug = True)