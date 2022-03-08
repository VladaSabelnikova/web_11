import flask
from flask import jsonify, make_response

from task_2.data import db_session
from task_2.data.jobs import Jobs
from task_2.data import __all_models


db_session.global_init('db/blogs.db')

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
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
    return jsonify(
        {'jobs': [item.to_dict(only=all_attributes) for item in jobs]}
    )


@blueprint.route('/api/jobs/<job_id>')
def get_job(job_id):

    if not job_id.isdigit():
        return make_response(jsonify({'error': 'id must be an integer'}), 404)

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
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

    if not job:
        return make_response(jsonify({'error': 'job by id not found'}), 404)

    return jsonify(
        {'job': job.to_dict(only=all_attributes)}
    )


@blueprint.route('/api')
def check():
    return 'Обработчик api работает'
