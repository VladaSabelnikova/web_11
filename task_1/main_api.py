import flask
from flask import jsonify

from task_1.data import db_session
from task_1.data.jobs import Jobs
from task_1.data import __all_models


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
        {'jobs': [item.to_dict(only=all_attributes) for item in jobs]})


@blueprint.route('/api')
def check():
    return 'Обработчик api работает'
