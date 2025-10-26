from flask import Blueprint, render_template, request, redirect, url_for, g

from todor.auth import login_required
from .models import Todo, User
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods = ('GET','POST'))
@login_required
def crear_tarea():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # creamos el objeto todo
        todo = Todo(g.user.id, title, desc)
        # guardamos el objeto todo  a la base de datos
        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods = ('GET','POST'))
@login_required
def update(id):
    todo = get_todo(id)
    if request.method == 'POST':
        # modificamos los datos
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False
    
        # guardamos las modificaciones en la base de datos
        db.session.commit()

        return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo = todo)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))