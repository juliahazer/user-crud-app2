from project import db

class Message(db.Model):
  __tablename__ = "messages"

  id = db.Column(db.Integer, primary_key=True)
  msg_text = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #has to be primary key here

  def __init__(self, msg_text, user_id):
    self.msg_text = msg_text
    self.user_id = user_id

  def __repr__(self):
    return "The message is: {}".format(self.msg_text)