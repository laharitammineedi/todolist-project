from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
TASKS_FILE = "tasks.json"

# Load tasks from JSON file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task")
    if task_text:
        tasks = load_tasks()
        tasks.append({"task": task_text, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/toggle/<int:index>")
def toggle_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
