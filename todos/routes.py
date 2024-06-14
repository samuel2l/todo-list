from flask import render_template, redirect, url_for, flash, request
from todos import app
from todos.models import User, Todos
from todos.forms import RegisterForm, LoginForm, NewTodoForm, DelForm, UpdateForm
from todos import db
from flask_login import login_user, logout_user, login_required, current_user
@app.route("/")
def home():
    return "<h1>Homepage</h1>"

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(name=form.name.data, email=form.email.data,
                               password=form.password.data)
        db.session.add(create_user)
        db.session.commit()

        login_user(create_user)
        flash("successful creation", category='success')
        return redirect(url_for('todos_page'))

    if form.errors != {}:
        for err in form.errors.values():
            flash(f'There was an error: {err}')

    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash("successful log in")
            return redirect(url_for('todos_page'))

        else:
            flash('Username and password do not match', category='danger')
            return redirect(url_for('login_page'))

    return render_template('login.html', form=form)


@login_required
@app.route("/todos", methods =["GET", "POST"])
def todos_page():
    user_todos = Todos.query.filter_by(user_id=current_user.id).all()
    form = NewTodoForm()
    del_form = DelForm()
    if form.validate_on_submit():
        add_todo = Todos(title=form.title.data, content=form.content.data, user_id= current_user.id)
        db.session.add(add_todo)
        db.session.commit()
    # if del_form.validate_on_submit():
    #     del_todo = Todos.query.filter_by(id=id).
    #     db.session.delete(del_todo)
    #     db.session.commit()

    return render_template('todos.html',user_todos=user_todos, form=form,del_form=del_form)
@login_required
@app.route("/todos/<int:id>", methods=["GET","POST"])
def delete_todo(id):
    user_todos = Todos.query.filter_by(user_id=current_user.id).all()
    del_form = DelForm()
    if del_form.validate_on_submit():
        del_todo = Todos.query.filter_by(id=id).first()
        db.session.delete(del_todo)
        db.session.commit()
        return redirect(url_for('todos_page'))
    return render_template('todos.html',user_todos=user_todos, form=del_form)


@login_required
@app.route("/todos/<string:index>")
def full_todo_page(index):

    for todo in Todos.query.filter_by(title=index):
        title = todo.title
        content = todo.content
        created = todo.created

    return render_template("full_todo.html", title=title, content=content,created=created)


@login_required
@app.route("/todos/<int:id>/update", methods=["GET", "POST"])
def update_todo(id):
    todo_to_update = Todos.query.filter_by(id=id).first()
    update_form = UpdateForm()
    if update_form.validate_on_submit():
        todo_to_update.title = update_form.title.data
        todo_to_update.description = update_form.content.data
        db.session.commit()
        flash("Todo updated successfully.", "success")
        return redirect(url_for('todos_page'))
    return render_template('update.html', todo=todo_to_update, update_form=update_form)

@app.route('/logout')
def logout_page():
    logout_user()
    # ein that
    flash("Successfully logged out", category='info')
    return redirect('/login')
