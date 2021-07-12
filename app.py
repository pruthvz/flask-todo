from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    urgent = db.Column(db.Boolean)


@app.route("/")
def index():
    incompleteTodos = Todo.query.filter_by(complete=False, urgent=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    urgent = Todo.query.filter_by(complete=False, urgent=True).all() 
    return render_template('index.html', incompleteTodos=incompleteTodos, complete=complete, urgent=urgent)

@app.route("/add", methods=["POST"])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False, urgent=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/complete/<id>")
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    todo.urgent = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/incomplete/<id>")
def incomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = False
    todo.urgent = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove/<id>')
def remove(id):
    removeTodo = Todo.query.get(id)
    db.session.delete(removeTodo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/urgent/<id>')
def urgent(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.completed = True
    todo.urgent = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)