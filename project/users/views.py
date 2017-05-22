from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User
from project.users.forms import UserForm
from project import db
from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder='templates'
)

@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    form = UserForm(request.form)
    if form.validate():
      try:
        new_user = User(form.username.data, form.email.data, form.first_name.data, form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
        flash("You added the user: " + new_user.username)
        return redirect(url_for('users.index'))

      #if violates unique field for username/email
      except IntegrityError as e:
        if (str(e.orig.pgerror).find('username_key') != -1):
          flash("Please enter a different username. This user already exists.")
        else:
          flash("Please enter a different email. This email already exists.")
    return render_template('users/new.html', form=form)

  users = User.query.all()
  return render_template('users/index.html', users = users)

@users_blueprint.route('/new')
def new():
  form = UserForm()
  return render_template('users/new.html', form=form)

@users_blueprint.route('/<int:user_id>/edit')
def edit(user_id):
  user = User.query.get(user_id)
  form = UserForm(obj=user)
  return render_template('users/edit.html', form=form, user=user)

@users_blueprint.route('/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
def show(user_id):
  found_user = User.query.get_or_404(user_id)
  if request.method == b'PATCH':
    form = UserForm(request.form)
    if form.validate():
      try:
        form.populate_obj(found_user)
        db.session.add(found_user)
        db.session.commit()
        flash("You edited this user.")
        return redirect(url_for('users.show', user_id = found_user.id))

      #if violates unique field for username/email
      except IntegrityError as e:
        if (str(e.orig.pgerror).find('username_key') != -1):
          flash("Please enter a different username. This user already exists.")
        else:
          flash("Please enter a different email. This email already exists.")
        db.session.rollback()
      #if form isn't validating
    return render_template('users/edit.html', user=found_user, form=form)

  if request.method == b'DELETE':
    db.session.delete(found_user)
    db.session.commit()
    flash("You deleted the user: " + found_user.username)
    return redirect(url_for('users.index'))

  return render_template('users/show.html', user=found_user) 
