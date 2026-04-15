# Imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import date, datetime

# App Setup
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Data Class ~ Row of data
class AllTasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return f"Task {self.id}"
    
with app.app_context():
    db.create_all()

# routes to webpages
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        task_due_date = request.form['due_date']

        if task_due_date == "":
            task_due_date = date.today()
        else:
            task_due_date = datetime.strptime(task_due_date, "%Y-%m-%d").date()
        # Convert the due date string to a date object
        

        new_task = AllTasks(content=task_content, due_date=task_due_date)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        tasks = AllTasks.query.order_by(AllTasks.due_date).all()
        return render_template('index.html', tasks=tasks)

# Delete route
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = AllTasks.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

#Edit route
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id): 
    task = AllTasks.query.get_or_404(id)   
    if request.method == "POST":
        task.content = request.form['content']
        task_due_date = request.form['due_date']
        task.due_date = datetime.strptime(task_due_date, "%Y-%m-%d").date()
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', task=task)

# Runs and Debugs
if __name__ == "__main__":
    app.run(debug=True)