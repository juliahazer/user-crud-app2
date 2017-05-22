from project import db

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True, nullable=False)
  email = db.Column(db.Text, unique=True, nullable=False)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)
  # messages = db.relationship('Message', backref='user', lazy='dynamic')

  def __init__(self, username, email, first_name, last_name):
    self.username = username
    self.email = email
    self.first_name = first_name
    self.last_name = last_name

  def __repr__(self):
    return "This user's username is {}, email is {}, first name is {}, and last name is {}".format(self.username, self.email, self.first_name, self.last_name)