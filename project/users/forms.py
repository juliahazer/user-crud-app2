from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, Email

class UserForm(FlaskForm): #this is inheriting from FlaskForm class
  username = StringField('Username', validators=[Length(min=1)]) #Unique(User, User.username, message="there is already an account with that username")])
  email = StringField('Email', validators = [Length(min=5, max=35), Email()])
  first_name = StringField('First Name', validators = [Length(min=1)])
  last_name = StringField('Last Name', validators =[Length(min=1)])