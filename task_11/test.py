from requests import get, post, delete

from task_4.data import db_session
from task_4.data.jobs import Jobs
from task_4.data import __all_models


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
    job = db_sess.query(Jobs).filter(Jobs.id == 4).first()
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

    assert get('http://127.0.0.1:8080/api/jobs/4').json() == correct


def test_one_job_error_id():
    correct = {'error': 'job by id not found'}

    assert get('http://127.0.0.1:8080/api/jobs/123456789').json() == correct


def test_one_job_invalid_id():
    correct = {'error': 'id must be an integer'}

    assert get('http://127.0.0.1:8080/api/jobs/id').json() == correct


def test_add_jobs_correct():
    """
    Тест корректного добавления.
    """
    correct = {'info': ' successfully'}

    variant = post(
        'http://localhost:8080/api/jobs',
        json={
            'job': 'lalalal',
            'work_size': 1,
            'collaborators': '1, 2, 5',
            'is_finished': False,
            'team_leader': 5
        }
    ).json()

    assert variant == correct


def test_add_jobs_invalid_not_args():
    """
    Тест не корректного добавления.
    Отсутствуют параметры.
    """

    correct = {'error': 'No parameters'}

    variant = post('http://localhost:8080/api/jobs', json={}).json()

    assert variant == correct


def test_add_jobs_invalid_id():
    """
    Тест не корректного добавления.
    Добавление существующего id.
    """

    correct = {'error': ' Id already exists'}

    variant = post('http://localhost:8080/api/jobs',
        json={
            'id': 4,
            'job': 'lalalal',
            'work_size': 1,
            'collaborators': '1, 2, 5',
            'is_finished': False,
            'team_leader': 5
        }
    ).json()

    assert variant == correct


def test_delete_jobs_correct():
    """
    Тест корректного удаления.
    """
    correct = {'info': ' successfully'}
    variant = delete('http://localhost:8080/api/jobs/4').json()

    assert variant == correct


def test_delete_jobs_invalid_id():
    """
    Тест некорректного удаления.
    Не существующий id
    """
    correct = {'error': 'job by id not found'}
    variant = delete('http://localhost:8080/api/jobs/1234567').json()

    assert variant == correct


def test_delete_jobs_error_id():
    """
    Тест некорректного удаления.
    Тип id не число.
    """
    correct = {'error': 'id must be an integer'}
    variant = delete('http://localhost:8080/api/jobs/id').json()

    assert variant == correct


def test_editing_jobs_correct():
    """
    Тест корректного редактирования.
    """
    correct = {'info': ' successfully'}
    variant = post(
        'http://localhost:8080/api/jobs/2',
        json={'job': 'ura!!!!'}
    ).json()

    assert variant == correct


def test_editing_jobs_error_id():
    """
    Тест некорректного редактирования.
    id не число.
    """
    correct = {'error': 'id must be an integer'}
    variant = post(
        'http://localhost:8080/api/jobs/id',
        json={'job': 'ura!!!!'}
    ).json()

    assert variant == correct


def test_editing_jobs_no_arguments():
    """
    Тест некорректного редактирования.
    Не переданы аргументы.
    """
    correct = {'error': 'No parameters'}
    variant = post(
        'http://localhost:8080/api/jobs/2',
        json={}
    ).json()

    assert variant == correct
