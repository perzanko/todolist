import datetime
import json
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Task


@app.route('/tasks', methods=['POST'])
def create():
    try:
        data = json.loads(request.data)
        task = Task()
        task.title = data['title']
        task.description = data['description']
        db.session.add(task)
        db.session.commit()
        return jsonify(task.serialize())
    except Exception as e:
        str(e)


@app.route('/tasks')
def find():
    try:
        tasks = Task.query.all()
        serialized_tasks = list(map(lambda x: x.serialize(), tasks))
        return jsonify(serialized_tasks)
    except Exception as e:
        str(e)


@app.route('/tasks/<task_id>/resolve', methods=['POST'])
def resolve(task_id):
    try:
        task = Task.query.get(task_id)
        task.is_resolved = True
        task.resolved_at = datetime.datetime.now()
        db.session.add(task)
        db.session.commit()
        return jsonify(task.serialize())
    except Exception as e:
        str(e)


@app.route('/tasks/<task_id>')
def get(task_id):
    try:
        task = Task.query.get(task_id)
        return jsonify(task.serialize())
    except Exception as e:
        str(e)


if __name__ == '__main__':
    app.run()
