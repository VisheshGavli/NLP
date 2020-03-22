from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.post.forms import PostForm

posts = Blueprint('posts',__name__)


@posts.route('/post/new/', methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Content has been Posted','success')

        return redirect(url_for('main.home'))
    else:
        pass
    return render_template('create_post.html', title='New Post', legend='Create Post',form=form)



@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)


@posts.route('/post/<int:post_id>/update/', methods=['POST','GET'])
@login_required
def update_post(post_id):

    print(current_user)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your Post has been updated.','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',title='Update Post', legend='Update Post', form=form)


@posts.route('/post/<int:post_id>/delete/', methods=['POST'])
@login_required
def delete_post(post_id):

    print('go')
    print(current_user)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted.','success')
    return redirect(url_for('main.home'))



