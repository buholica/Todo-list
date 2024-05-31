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


@app.route('/', methods=['GET'])
def homepage():
    sheets_response = requests.get(sheets_endpoint, headers=sheets_headers)
    data = sheets_response.json()["list1"]
    print(data)

    message = "Please, add a new task."

    return render_template("index.html", tasks=data, day=today.day, message=message)


@app.route('/active-tasks', methods=['GET'])
def show_active_tasks():
    sheets_response = requests.get(sheets_endpoint, headers=sheets_headers)
    data = sheets_response.json()["list1"]
    active_tasks = [task for task in data if task["status"] == "active"]

    message = "There are no active tasks currently."

    return render_template("index.html", tasks=active_tasks, day=today.day, message=message)


@app.route("/completed_task", methods=['GET'])
def show_completed_tasks():
    sheets_get_response = requests.get(sheets_endpoint, headers=sheets_headers)
    data = sheets_get_response.json()["list1"]

    completed_tasks = [task for task in data if task["status"] == "completed"]
    message = "There are no completed tasks currently."

    return render_template("index.html", tasks=completed_tasks, day=today.day, message=message)


@app.route('/add_task', methods=['POST'])
def add_task():
    sheets_get_response = requests.get(sheets_endpoint, headers=sheets_headers)
    data = sheets_get_response.json()["list1"]

    new_task = request.form.get('new-task')
    new_task = {
        "list1": {
            "id": len(data) + 1,
            "date": today.day,
            "description": new_task,
            "status": "active"
        }
    }

    sheets_post_response = requests.post(sheets_endpoint, json=new_task, headers=sheets_headers)
    sheets_post_response.raise_for_status()

    return redirect('/')


@app.route("/update_status", methods=['GET', 'POST'])
def update_status():
    completed_task_id = request.form.get('task_id')
    completed_task_id_int = int(completed_task_id)

    sheets_get_response = requests.get(sheets_endpoint, headers=sheets_headers)
    data = sheets_get_response.json()["list1"]

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

    sheets_get_response = requests.get(sheets_endpoint, headers=sheets_headers)
    data = sheets_get_response.json()["list1"]

    for task in data:
        if task_id_int == task["id"]:
            sheets_delete_response = requests.delete(sheets_endpoint + f"/{task_id_int}", headers=sheets_headers)
            sheets_delete_response.raise_for_status()
            break

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=False)