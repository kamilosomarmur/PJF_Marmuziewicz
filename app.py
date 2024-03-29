from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)
app.app_context().push()
class Kanban(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    column = db.Column(db.String(20), default="todo")

    def __repr__(self):
        return '<Task %r>'%self.id


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        task_content = request.form['content']
        existing_task = Kanban.query.filter_by(content=task_content).first()
        if existing_task:
            return 'Task with the same content already exists'
        else:
            new_task = Kanban(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Wystąpił błąd przy dodawaniu zadania'
    else:
        tasks = Kanban.query.order_by(Kanban.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Kanban.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Wystąpił błąd przy usuwaniu zadania'
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Kanban.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Wystąpił błąd przy edycji zadania'
    else:
        return render_template('edit.html',task=task)
@app.route('/update_column/<int:id>/<column>', methods=['POST'])
def update_column(id, column):
    task = Kanban.query.get_or_404(id)
    task.column = column

    try:
        db.session.commit()
    except:
        return 'Wystąpił błąd przy przenoszeniu zadania'

if __name__ == '__main__':
    app.run(debug=True)
