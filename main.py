from flask import Flask, render_template, request, redirect, flash, jsonify
import os
from day import Day
import json
from py_scdb import Store

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

today = Day()

store = Store(
        store_path="db",
        max_keys=1000000,
        redundant_blocks=1,
        pool_capacity=10,
        compaction_interval=1800,
        is_search_enabled=True,
)


@app.route('/', methods=['GET'])
def homepage():
    data = {
        "task1": {
            "id": 1,
            "date": today.day,
            "description": "Create a todo list",
            "status": "active"
        },
        "task2": {
            "id": 2,
            "date": today.day,
            "description": "Create a presentation",
            "status": "active"
        },
    }

    all_tasks = [{key: value} for key, value in data.items()]

    message = "Please, add a new task."

    return render_template("index.html", tasks=all_tasks, day=today.day, message=message)


# @app.route('/active-tasks', methods=['GET'])
# def show_active_tasks():
#     # with open('data.json') as data_json:
#     #     data = json.load(data_json)["list1"]
#
#     active_tasks = [task for task in data["list"] if task["status"] == "active"]
#
#     message = "There are no active tasks currently."
#
#     return render_template("index.html", tasks=active_tasks, day=today.day, message=message)
#
#
# @app.route("/completed_task", methods=['GET'])
# def show_completed_tasks():
#     # with open('data.json') as data_json:
#     #     data = json.load(data_json)
#
#     completed_tasks = [task for task in data["list"] if task["status"] == "completed"]
#     message = "There are no completed tasks currently."
#
#     return render_template("index.html", tasks=completed_tasks, day=today.day, message=message)
#
#
# @app.route('/add_task', methods=['POST'])
# def add_task():
#     new_task = request.form.get('new-task')
#     # with open('data.json') as data_json:
#     #     data = json.load(data_json)["list1"]
#
#     new_task = {
#             "id": len(data) + 1,
#             "date": today.day,
#             "description": new_task,
#             "status": "active"
#     }
#
#     # with open('data.json') as data_json:
#     #     data = json.load(data_json)
#
#     data["list"].append(new_task)
#
#     with open('data.json', "w") as data_json:
#         json.dump(data, data_json, indent=4, separators=(',', ': '))
#
#     return redirect('/')
#
#
# @app.route("/update_status", methods=['GET', 'POST'])
# def update_status():
#     completed_task_id = request.form.get('task_id')
#
#     # with open('data.json') as data_json:
#     #     data = json.load(data_json)
#
#     for task in data["list"]:
#         if int(completed_task_id) == task["id"]:
#             task["status"] = "completed"
#
#     with open('data.json', "w") as data_json:
#         json.dump(data, data_json, indent=4, separators=(',', ': '))
#
#     return redirect("/")
#
#
# @app.route("/remove_task", methods=['POST'])
# def remove_task():
#     task_id = request.form.get('task_id')
#
#     # with open('data.json') as data_json:
#     #     data = json.load(data_json)
#
#     for task in data["list"]:
#         if int(task_id) == task["id"]:
#             data["list"].remove(task)
#
#     with open('data.json', "w") as data_json:
#         json.dump(data, data_json, indent=4, separators=(',', ': '))
#
#     return redirect("/")
#
#
if __name__ == '__main__':
    app.run(debug=True)