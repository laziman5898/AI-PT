from flask_wtf import Form
from wtforms import StringField, PasswordField, EmailField, SubmitField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email


class Resigter(Form):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Login(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class info_update_form(Form):
    height = FloatField("Height in CM", validators=[DataRequired()])
    weight = FloatField("Weight in KG", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[('Male', 'Male'), ('Female', 'Female'), ('Unspecifed', 'Not Specified')])
    age = IntegerField("Age", validators=[DataRequired()])
    submit = SubmitField()
