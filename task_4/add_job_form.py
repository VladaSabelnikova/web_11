from flask_wtf import FlaskForm
from wtforms import SubmitField, \
    IntegerField, StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField('Тимлид', validators=[DataRequired()])
    job = TextAreaField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объём работы', validators=[DataRequired()])
    collaborators = StringField('Список участников', validators=[DataRequired()])
    is_finished = BooleanField('Завершено')
    submit = SubmitField('Сохранить')
