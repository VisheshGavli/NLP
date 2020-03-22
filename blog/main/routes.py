from flask import render_template, request, Blueprint
from blog.models import Post
from flask_login import current_user
main = Blueprint('main', __name__)

@main.route('/home/')
@main.route('/')
@main.route('/index/')
def home():
    page = request.args.get('page', 1, type=int)
    print(current_user)
    # if current_user.is_authenticated:
    #     posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).paginate(per_page=2)
    # else:
    #     posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=2)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=10)
    return render_template('home.html',posts=posts,title='Home')

@main.route('/about/')
def about():
    return render_template('about.html',title='About')
