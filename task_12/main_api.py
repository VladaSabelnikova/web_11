import flask
from flask import jsonify, make_response, request

from task_4.data import db_session
from task_4.data.jobs import Jobs
from task_4.data import __all_models


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


@blueprint.route('/api/jobs', methods=['POST'])
def add_jobs():
    all_keys = (
        'job',
        'work_size',
        'collaborators',
        'is_finished',
        'team_leader'
    )
    in_json = request.json
    new_id = request.json.get('id', False)
    db_sess = db_session.create_session()

    if not in_json:
        return make_response(jsonify({'error': 'No parameters'}), 500)

    elif not all(key in request.json for key in all_keys):
        return make_response(jsonify({'error': 'Bad request'}), 500)

    elif new_id:
        if db_sess.query(Jobs).filter(Jobs.id == new_id).first():
            return make_response(jsonify({'error': ' Id already exists'}), 500)

    job = Jobs()
    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    db_sess.add(job)
    db_sess.commit()

    return make_response(jsonify({'info': ' successfully'}), 200)


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


@blueprint.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):

    if not job_id.isdigit():
        return make_response(jsonify({'error': 'id must be an integer'}), 500)

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return make_response(jsonify({'error': 'job by id not found'}), 400)

    db_sess.delete(job)
    db_sess.commit()

    return make_response(jsonify({'info': ' successfully'}), 200)


@blueprint.route('/api/jobs/<job_id>', methods=['POST'])
def editing_job(job_id):

    if not job_id.isdigit():
        return make_response(jsonify({'error': 'id must be an integer'}), 500)

    in_json = request.json
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return make_response(jsonify({'error': 'job by id not found'}), 400)

    if not in_json:
        return make_response(jsonify({'error': 'No parameters'}), 500)

    job.team_leader = request.json.get('team_leader', job.team_leader)
    job.job = request.json.get('job', job.job)
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.is_finished = request.json.get('is_finished', job.is_finished)
    db_sess.add(job)
    db_sess.commit()

    return make_response(jsonify({'info': ' successfully'}), 200)


@blueprint.route('/api')
def check():
    return 'Обработчик api работает'
