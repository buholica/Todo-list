from flask import Flask, render_template, request, redirect, session, flash
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
    try:
        response = requests.get(sheets_endpoint, headers=sheets_headers)
        response.raise_for_status()
        return response.json()["list1"]
    except requests.exceptions.HTTPError as error:
        if response.status_code == 402:
            print("402. The 200 requests quota is past for SHEETY API.")
        else:
            print(f"HTTP error occurred: {error}")

        with open('data.json') as data_json:
            return json.load(data_json)["list1"]


@app.route('/', methods=["GET"])
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


@app.route('/add_task', methods=["GET", "POST"])
def add_task():
    data = get_tasks_from_sheet()

    new_task = request.form.get('new-task')

    if len(new_task) == 0:
        flash("Please, type a new task.")
    else:
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

        try:
            sheets_post_response = requests.post(sheets_endpoint, json=new_task, headers=sheets_headers)
            sheets_post_response.raise_for_status()
        except Exception as error:
            print(f"The error occurred:\n {type(error).__name__} - {error}")

            with open('data.json') as data_json:
                data = json.load(data_json)
            data["list1"].append(new_task["list1"])
            with open('data.json', "w") as data_json:
                json.dump(data, data_json,
                          indent=4,
                          separators=(',', ': '))

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
            try:
                sheets_put_response = requests.put(sheets_endpoint + f"/{completed_task_id_int}", json=updated_task,
                                                   headers=sheets_headers)
                sheets_put_response.raise_for_status()
                break
            except Exception as error:
                print(f"The error occurred:\n {type(error).__name__} - {error}")

                with open('data.json') as data_json:
                    data = json.load(data_json)

                task_index = data["list1"].index(task)
                del data["list1"][task_index]
                data["list1"].append(updated_task["list1"])
                with open('data.json', "w") as data_json:
                    json.dump(data, data_json,
                              indent=4,
                              separators=(',', ': '))

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

            try:
                sheets_delete_response = requests.delete(sheets_endpoint + f"/{task_id_int}", headers=sheets_headers)
                sheets_delete_response.raise_for_status()
                break
            except Exception as error:
                print(f"The error occurred:\n {type(error).__name__} - {error}")

                with open('data.json') as data_json:
                    data = json.load(data_json)

                task_index = data["list1"].index(task)
                del data["list1"][task_index]
                with open('data.json', "w") as data_json:
                    json.dump(data, data_json,
                              indent=4,
                              separators=(',', ': '))

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=False)