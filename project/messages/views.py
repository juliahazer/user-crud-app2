from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.messages.models import Message
from project.users.models import User
from project.messages.forms import MessageForm
from project import db
from sqlalchemy.exc import IntegrityError

messages_blueprint = Blueprint(
  'messages',
  __name__,
  template_folder='templates'
)

@messages_blueprint.route('/', methods=['GET', 'POST'])
def index(user_id):
  user = User.query.get(user_id)
  messages = user.messages
  if request.method == 'POST':
    form = MessageForm(request.form)
    if form.validate():
      try:
        new_msg = Message(form.msg_text.data, user_id)
        db.session.add(new_msg)
        db.session.commit()
        flash('You added the message: "' + form.msg_text.data + '"')
        return redirect(url_for('messages.index', user_id=user_id))

      #if violates unique field for username/email
      except IntegrityError as e:
        if (str(e.orig.pgerror).find('username_key') != -1):
          flash("Please enter a different username. This user already exists.")
        else:
          flash("Please enter a different email. This email already exists.")
    return render_template('messages/new.html', user=user, form=form)

  return render_template('messages/index.html', messages=messages, user=user)

@messages_blueprint.route('/new')
def new(user_id):
  user = User.query.get(user_id)
  form = MessageForm()
  return render_template('messages/new.html', user=user, form=form)

@messages_blueprint.route('/<int:msg_id>/edit')
def edit(user_id, msg_id):
  found_user = User.query.get(user_id)
  selected_message = Message.query.get_or_404(msg_id)
  form = MessageForm(obj=selected_message)
  return render_template('messages/edit.html', user=found_user, message=selected_message, form=form)

@messages_blueprint.route('/<int:msg_id>', methods=['GET', 'PATCH', 'DELETE'])
def show(user_id,msg_id):
  found_user = User.query.get_or_404(user_id)
  selected_message = Message.query.get_or_404(msg_id)
  if request.method == b'PATCH':
    form = MessageForm(request.form, obj=selected_message)
    if form.validate():
      form.populate_obj(selected_message)
      db.session.add(selected_message)
      db.session.commit()
      flash('You edited the message. "' + selected_message.msg_text + '"')
      return redirect(url_for('messages.index', user_id=found_user.id))
    return render_template('messages/edit.html', user=found_user, message=selected_message, form=form)

  if request.method == b'DELETE':
    db.session.delete(selected_message)
    db.session.commit()
    flash('You deleted the message: "' + selected_message.msg_text + '"')
    return redirect(url_for('messages.index', user_id=found_user.id))

  #NO GET HERE FOR SHOW