import pathlib

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from requests import get

from data import db_session
from data.users import User
from loginform import LoginForm
import os
from data import __all_models
from data.jobs import Jobs
from add_job_form import AddJobForm
from registerform import RegisterForm
import main_api
from task_11 import user_api

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(
            User.email == form.email.data
        ).first()

        if user and user.check_password(form.hashed_password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            'login.html',
            message="Неправильный логин или пароль",
            form=form
        )
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message="Такой пользователь уже есть"
            )
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.hashed_password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template(
        'register.html',
        title='Регистрация',
        form=form
    )


@app.route('/users_show/<int:user_id>')
def users_show(user_id):

    user = get(f'http://localhost:8080/api/users/{user_id}').json()
    address = user['user']['address']
    surname = user['user']['surname']
    name = user['user']['name']

    api_server = "http://static-maps.yandex.ru/1.x/"

    # нужно заменить на address
    lon = "37.530887"
    lat = "55.703118"
    delta = "1.002"

    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "sat,skl"
    }
    response = requests.get(api_server, params=params)

    map_file = pathlib.Path('static/img/map.png')
    map_file.write_bytes(response.content)

    return render_template(
        'users_show.html',
        surname=surname,
        name=name,
        address=address,
        path=url_for('static', filename='/img/map.png')
    )


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template(
        'add_job.html',
        form=form,
        h1_text='Создать работу'
    )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job and current_user.id in (map(int, job.collaborators.split(', '))):
        db_sess.delete(job)
        db_sess.commit()
        return redirect('/')


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def job_edit(id):
    form = AddJobForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()

        if job and current_user.id in (map(int, job.collaborators.split(', '))):
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
            return render_template(
                'add_job.html',
                form=form,
                h1_text='Изменить работу'
            )
    elif request.method == 'POST':
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
            if job and current_user.id in (
                map(int, job.collaborators.split(', '))
            ):
                job.team_leader = form.team_leader.data
                job.job = form.job.data
                job.work_size = form.work_size.data
                job.collaborators = form.collaborators.data
                job.is_finished = form.is_finished.data
                db_sess.commit()
                return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        jobs = []
        for job in db_sess.query(Jobs):
            if current_user.id in (map(int, job.collaborators.split(', '))):
                jobs.append(job)
        return render_template('jobs_list.html', jobs=jobs)
    return render_template('base.html')


def main():
    db_session.global_init('db/blogs.db')
    app.register_blueprint(main_api.blueprint)
    app.register_blueprint(user_api.blueprint_user)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
