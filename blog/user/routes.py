from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import bcrypt,db
from blog.models import User,Post
from blog.user.forms import LoginForm,RegistrationForm

users = Blueprint('users',__name__)


@users.route('/login/',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Pls check your crendentials!','danger')
    return render_template('login.html',title='Login', form=form)


@users.route('/register/',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.add(User(username=form.username.data, email=form.email.data, password=hashed_pass))
        db.session.commit()
        flash(f'Account Created for {form.username.data}','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)

@users.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account/')
@login_required
def account():
    return render_template('account.html', title='Account')


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    print('here '+username)
    user=User.query.filter_by(username=username).first_or_404()
    print(user)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=4,page=page)
    return render_template('user_posts.html',posts=posts,title='Home',user=user)


