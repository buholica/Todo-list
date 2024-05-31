from flask import Flask, render_template, request, redirect, session
import os
from day import Day
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')
DOC_ID = os.environ.get('DOC_ID')

today = Day()
sheets_endpoint = f"https://api.sheety.co/{DOC_ID}/todoList/list1"
sheets_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}",
}


def get_tasks_from_sheet():
    """Function to get tasks from Google Sheets using Sheety API"""
    response = requests.get(sheets_endpoint, headers=sheets_headers)
    response.raise_for_status()
    return response.json()["list1"]


@app.route('/', methods=['GET'])
def homepage():
    data = get_tasks_from_sheet()

    if "tasks" not in session:
        session["tasks"] = []

    tasks_set = set(session["tasks"])

    for task in data:
        if task["id"] in session["tasks"]:
            tasks_set.add(task["id"])

    session.modified = True

    valid_tasks = [task for task in data if task["id"] in session["tasks"]]

    message = "Please, add a new task."

    return render_template("index.html", tasks=valid_tasks, day=today.day, message=message)


@app.route('/active-tasks', methods=['GET'])
def show_active_tasks():
    data = get_tasks_from_sheet()

    active_tasks = [task for task in data if task["status"] == "active"]
    valid_tasks = [task for task in active_tasks if task["id"] in session["tasks"]]

    message = "There are no active tasks currently."

    return render_template("index.html", tasks=valid_tasks, day=today.day, message=message)


@app.route("/completed_task", methods=['GET'])
def show_completed_tasks():
    data = get_tasks_from_sheet()

    completed_tasks = [task for task in data if task["status"] == "completed"]
    valid_tasks = [task for task in completed_tasks if task["id"] in session["tasks"]]

    message = "There are no completed tasks currently."

    return render_template("index.html", tasks=valid_tasks, day=today.day, message=message)


@app.route('/add_task', methods=['POST'])
def add_task():
    data = get_tasks_from_sheet()

    new_task = request.form.get('new-task')
    new_task = {
        "list1": {
            "id": data[-1]["id"] + 1,
            "date": today.day,
            "description": new_task,
            "status": "active"
        }
    }

    session["tasks"].append(new_task["list1"]["id"])
    session.modified = True

    sheets_post_response = requests.post(sheets_endpoint, json=new_task, headers=sheets_headers)
    sheets_post_response.raise_for_status()

    return redirect('/')


@app.route("/update_status", methods=['GET', 'POST'])
def update_status():
    completed_task_id = request.form.get('task_id')
    completed_task_id_int = int(completed_task_id)

    data = get_tasks_from_sheet()

    for task in data:
        if completed_task_id_int == task["id"]:
            updated_task = {
                "list1": {
                    "id": completed_task_id_int,
                    "date": task["date"],
                    "description": task["description"],
                    "status": "completed"
                }
            }
            sheets_put_response = requests.put(sheets_endpoint + f"/{completed_task_id_int}", json=updated_task, headers=sheets_headers)
            sheets_put_response.raise_for_status()
            break

    return redirect("/")


@app.route("/remove_task", methods=['POST'])
def remove_task():
    task_id = request.form.get('task_id')
    task_id_int = int(task_id)

    data = get_tasks_from_sheet()

    for task in data:
        if task_id_int == task["id"]:
            session["tasks"].remove(task_id_int)
            session.modified = True
            sheets_delete_response = requests.delete(sheets_endpoint + f"/{task_id_int}", headers=sheets_headers)
            sheets_delete_response.raise_for_status()
            break

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=False)