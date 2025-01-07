from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    name = StringField('Task', validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    completed = SelectField('Completed', choices = [("NO", "NO"), ("YES", "YES")], validators = [DataRequired()])
    submit = SubmitField("Add ToDo")