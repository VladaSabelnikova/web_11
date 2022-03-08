from requests import get

from task_3.data import db_session
from task_3.data.jobs import Jobs
from task_3.data import __all_models


db_session.global_init('db/blogs.db')


def test_all_jobs():
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    all_attributes = (
        'id',
        'job',
        'work_size',
        'collaborators',
        'start_date',
        'end_date',
        'is_finished',
        'user.name',
        'user.surname',
    )

    correct = {'jobs': [item.to_dict(only=all_attributes) for item in jobs]}

    assert get('http://127.0.0.1:8080/api/jobs').json() == correct


def test_one_job():
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == 1).first()
    all_attributes = (
        'id',
        'job',
        'work_size',
        'collaborators',
        'start_date',
        'end_date',
        'is_finished',
        'user.name',
        'user.surname',
    )

    correct = {'job': job.to_dict(only=all_attributes)}

    assert get('http://127.0.0.1:8080/api/jobs/1').json() == correct


def test_one_job_error_id():
    correct = {'error': 'job by id not found'}

    assert get('http://127.0.0.1:8080/api/jobs/123456789').json() == correct


def test_one_job_invalid_id():
    correct = {'error': 'id must be an integer'}

    assert get('http://127.0.0.1:8080/api/jobs/id').json() == correct
