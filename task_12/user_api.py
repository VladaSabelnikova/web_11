import flask
from flask import jsonify, make_response, request

from task_11.data import db_session
from task_11.data.users import User
from task_11.data import __all_models


db_session.global_init('db/blogs.db')

blueprint_user = flask.Blueprint(
    'api_user',
    __name__,
    template_folder='templates'
)


@blueprint_user.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    all_attributes = (
        'id',
        'surname',
        'name',
        'age',
        'position',
        'speciality',
        'address',
        'email',
        'hashed_password',
        'modified_date'
    )
    return jsonify(
        {'users': [item.to_dict(only=all_attributes) for item in users]}
    )


@blueprint_user.route('/api/users', methods=['POST'])
def add_users():
    all_keys = (
        'surname',
        'name',
        'age',
        'position',
        'speciality',
        'address',
        'email',
        'hashed_password'
    )
    in_json = request.json
    new_id = request.json.get('id', False)
    db_sess = db_session.create_session()

    if not in_json:
        return make_response(jsonify({'error': 'No parameters'}), 500)

    elif not all(key in request.json for key in all_keys):
        return make_response(jsonify({'error': 'Bad request'}), 500)

    elif new_id:
        if db_sess.query(User).filter(User.id == new_id).first():
            return make_response(jsonify({'error': ' Id already exists'}), 500)

    user = User()
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()

    return make_response(jsonify({'info': ' successfully'}), 200)


@blueprint_user.route('/api/users/<user_id>')
def get_user(user_id):

    if not user_id.isdigit():
        return make_response(jsonify({'error': 'id must be an integer'}), 404)

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    all_attributes = (
        'surname',
        'name',
        'age',
        'position',
        'speciality',
        'address',
        'email',
        'hashed_password'
    )

    if not user:
        return make_response(jsonify({'error': 'job by id not found'}), 404)

    return make_response(
        jsonify({'user': user.to_dict(only=all_attributes)}), 200
    )


@blueprint_user.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):

    if not user_id.isdigit():
        return make_response(jsonify({'error': 'id must be an integer'}), 500)

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()

    if not user:
        return make_response(jsonify({'error': 'job by id not found'}), 400)

    db_sess.delete(user)
    db_sess.commit()

    return make_response(jsonify({'info': ' successfully'}), 200)


@blueprint_user.route('/api/users/<job_id>', methods=['POST'])
def editing_user(user_id):

    if not user_id.isdigit():
        return make_response(jsonify({'error': 'id must be an integer'}), 500)

    in_json = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()

    if not user:
        return make_response(jsonify({'error': 'job by id not found'}), 400)

    if not in_json:
        return make_response(jsonify({'error': 'No parameters'}), 500)

    user.surname = request.json.get('surname', user.surname)
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.position = request.json.get('position', user.position)
    user.speciality = request.json.get('speciality', user.speciality)
    user.address = request.json.get('address', user.address)
    user.email = request.json.get('email', user.email)
    user.set_password(request.json.get('password', user.password))
    db_sess.add(user)
    db_sess.commit()

    return make_response(jsonify({'info': ' successfully'}), 200)


@blueprint_user.route('/api/user')
def check():
    return 'Обработчик api работает'
