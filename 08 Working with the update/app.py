from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newtry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__ (self):
        return f'{self.sno} - {self.title}'

with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def static_template():
    if request.method == 'POST':  # Only add a new todo on POST
        title = request.form['title']
        desc = request.form['desc']
        
        # Create a new Todo and add it to the database
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('static_template'))
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/show")
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "Show page"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':  # Only add a new todo on POST
        title = request.form['title']
        desc = request.form['desc']
    
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,port=8000)