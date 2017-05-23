from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import Length

class MessageForm(FlaskForm):
  msg_text = TextAreaField('Message', validators = [Length(min=1, max=100)], render_kw={"rows": 5, "cols": 40})