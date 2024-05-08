from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
from day import Day
import json

load_dotenv("C:\\Users\\Oksana\\Desktop\\passwords.env.txt")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBHO6O6doNzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# SHEETY_TOKEN = os.getenv("SHEETY_TOKEN_TODO_L")
# DOC_ID = os.getenv("DOC_ID_TODO_L")
# sheety_endpoint = "https://api.sheety.co/2af8e23237aae490a742fcae381a9e81/todoList/list1"

# sheety_headers = {
#     "Authorization": f"Bearer {SHEETY_TOKEN}",
# }

all_tasks = []
today = Day()


@app.route('/', methods=['GET'])
def homepage():
    all_tasks.clear()
    # sheety_response = requests.get(sheety_endpoint, headers=sheety_headers)
    # data = sheety_response.json()["list1"]
    with open('data.json') as data_json:
        data = json.load(data_json)["list1"]
    return render_template("index.html", tasks=data, day=today.day)


@app.route('/active-tasks', methods=['GET'])
def show_active_tasks():
    # sheety_response = requests.get(sheety_endpoint, headers=sheety_headers)
    # data = sheety_response.json()["list1"]
    with open('data.json') as data_json:
        data = json.load(data_json)["list1"]
    status = request.args.get('status', default='active')
    print(status)
    active_tasks = [task for task in data if task['status'] == status]
    print(active_tasks)
    return render_template("index.html", tasks=active_tasks, day=today.day)


@app.route("/completed_task", methods=['GET'])
def show_completed_tasks():
    with open('data.json') as data_json:
        data = json.load(data_json)
    completed_tasks = [task for task in data["list1"] if task["status"] == "completed"]

    return render_template("index.html", tasks=completed_tasks, day=today.day)


@app.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.form.get('new-task')
    all_tasks.append(new_task)
    with open('data.json') as data_json:
        data = json.load(data_json)["list1"]
    # sheety_data = {
    #     "list1": {
    #         "date": today.day,
    #         "text": new_task,
    #         "status": "active"
    #     }
    # }
    sheety_data = {
            "id": len(data),
            "date": today.day,
            "description": new_task,
            "status": "active"
    }
    print(sheety_data)
    with open('data.json') as data_json:
        data = json.load(data_json)
    data["list1"].append(sheety_data)
    with open('data.json', "w") as data_json:
        json.dump(data, data_json,
                        indent=4,
                        separators=(',', ': '))
    # requests.post(sheety_endpoint, json=sheety_data, headers=sheety_headers)

    return redirect('/')


@app.route("/update_status", methods=['POST'])
def update_status():
    completed_task_id = request.form.get('task_id')

    with open('data.json') as data_json:
        data = json.load(data_json)

    for task in data["list1"]:
        if task["id"] == int(completed_task_id):
            task["status"] = "completed"

    with open('data.json', "w") as data_json:
        json.dump(data, data_json, indent=4, separators=(',', ': '))

    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)