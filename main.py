from flask import Flask, render_template, request, redirect, flash
import os
from day import Day
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

today = Day()


@app.route('/', methods=['GET'])
def homepage():
    with open('data.json') as data_json:
        data = json.load(data_json)["list1"]
    all_tasks = [task for task in data]

    message = "Please, add a new task."

    return render_template("index.html", tasks=all_tasks, day=today.day, message=message)


@app.route('/active-tasks', methods=['GET'])
def show_active_tasks():
    with open('data.json') as data_json:
        data = json.load(data_json)["list1"]
    active_tasks = [task for task in data if task["status"] == "active"]

    message = "There are no active tasks currently."

    return render_template("index.html", tasks=active_tasks, day=today.day, message=message)


@app.route("/completed_task", methods=['GET'])
def show_completed_tasks():
    with open('data.json') as data_json:
        data = json.load(data_json)
    completed_tasks = [task for task in data["list1"] if task["status"] == "completed"]

    message = "There are no completed tasks currently."

    return render_template("index.html", tasks=completed_tasks, day=today.day, message=message)


@app.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.form.get('new-task')
    with open('data.json') as data_json:
        data = json.load(data_json)["list1"]

    new_data = {
            "id": len(data),
            "date": today.day,
            "description": new_task,
            "status": "active"
    }

    with open('data.json') as data_json:
        data = json.load(data_json)

    data["list1"].append(new_data)

    with open('data.json', "w") as data_json:
        json.dump(data, data_json, indent=4, separators=(',', ': '))

    return redirect('/')


@app.route("/update_status", methods=['GET', 'POST'])
def update_status():
    completed_task_id = request.form.get('task_id')

    with open('data.json') as data_json:
        data = json.load(data_json)

    for task in data["list1"]:
        if int(completed_task_id) == task["id"]:
            task["status"] = "completed"

    with open('data.json', "w") as data_json:
        json.dump(data, data_json, indent=4, separators=(',', ': '))

    return redirect("/")


@app.route("/remove_task", methods=['POST'])
def remove_task():
    task_id = request.form.get('task_id')

    with open('data.json') as data_json:
        data = json.load(data_json)

    for task in data["list1"]:
        if int(task_id) == task["id"]:
            data["list1"].remove(task)

    with open('data.json', "w") as data_json:
        json.dump(data, data_json, indent=4, separators=(',', ': '))

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=False)