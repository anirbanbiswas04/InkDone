from flask_login import login_user, current_user, logout_user, login_required
from inkdone.users.forms import LoginForm, SignUpForm, ProfileEditForm
from flask import render_template, redirect, url_for, flash, Blueprint, current_app
from inkdone.users.models import User, Accomplishment
from inkdone import db
import os

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
            ).first()
        if user and user.check_password(form_password=form.password.data):
            login_user(user)
            flash(f'You are logged in as: {user.username}', category='✅')
            return redirect(url_for('users.profile', username=user.username))
        else:
            flash('Username or password do not match! Please try again.', category='❌')
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out.', category='✅')
    return redirect(url_for('users.login'))


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('core.home'))
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=form.password1.data
            )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created as: {user.username}, Please login.', category='✅')
        return redirect(url_for('users.login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}.', category='❌')
    return render_template('signup.html', form=form)


@users.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(
        username=username
        ).first_or_404()
    image = ''

    if user.image:    
        image = url_for('static', filename='images/' + user.image)
    return render_template('profile.html', user=user, image=image)


@login_required
@users.route('/profile-edit', methods=['GET', 'POST'])
def profile_edit():
    form = ProfileEditForm()
    if form.validate_on_submit():
        if not form.clear_image.data:
            if form.image.data:
                if current_user.image:
                    current_img = os.path.join(current_app.root_path, 'static/images', current_user.image)
                    if os.path.exists(current_img):
                        os.remove(current_img)
                _, ext = os.path.splitext(form.image.data.filename)
                image_name = current_user.username + ext
                image_path =  os.path.join(current_app.root_path, 'static/images', image_name)
                form.image.data.save(image_path)
                current_user.image = image_name
        else:
            current_img = os.path.join(current_app.root_path, 'static/images', current_user.image)
            if os.path.exists(current_img):
                os.remove(current_img)
            current_user.image = None            
        current_user.bio=form.bio.data
        current_user.email=form.email.data
        current_user.academics=form.academics.data

        try:
            current_user.accomplishment[0].name= form.accomplishment_name.data
            current_user.accomplishment[0].description= form.accomplishment_description.data
        except:
            accomplishment = Accomplishment(
                name= form.accomplishment_name.data, 
                description= form.accomplishment_description.data,
                created_by= current_user.id
                )
            db.session.add(accomplishment)

        db.session.commit()

        flash(f'{current_user.username}, Your profile is updated.', category='✅')
        return redirect(url_for('users.profile', username=current_user.username))
    
    if form.errors != {}:
        for field, err_msg in form.errors.items():
            flash(f"{field.replace('_', ' ').title()} {err_msg[0]}", category='❌')

    form.email.data = current_user.email
    form.bio.data = current_user.bio
    form.academics.data = current_user.academics

    try:
        form.accomplishment_name.data = current_user.accomplishment[0].name
    except:
        pass

    try:
        form.accomplishment_description.data = current_user.accomplishment[0].description
    except:
        pass

    return render_template('profile_edit.html', form=form)

@login_required
@users.route('/delete')
def delete_account():
    if current_user.image:
        current_img = os.path.join(current_app.root_path, 'static/images', current_user.image)
        if os.path.exists(current_img):
            os.remove(current_img)
    user = User.query.filter_by(id=current_user.id)[0]
    db.session.delete(user)
    db.session.commit()
    flash(f'Your profile is deleted.', category='✅')
    return redirect(url_for('users.logout'))