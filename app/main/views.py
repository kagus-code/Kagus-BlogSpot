from flask import render_template, request,redirect, url_for,abort
from .forms import UpdateProfile,SubmitBlog,postComment
from .. import db,photos
from . import main
from flask_login import login_required,current_user
from ..models import User,Blog

@main.route('/')
def index():
    title = 'Kagus-BlogSpot Home Page'
    return render_template('index.html', title = title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form,user=user)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))     


@main.route('/submit_blog',methods = ['GET', 'POST'])
@login_required
def submit_blog():
    form = SubmitBlog()
    if form.validate_on_submit():
        blog_title = form.blog_title.data

        blog_post=form.blog_post.data
        new_blog = Blog(blog_title=blog_title,blog_post=blog_post,user = current_user)

        new_blog.save_blog()

        return redirect(url_for('main.index'))

    return render_template ('submit_blog.html',blog_form=form)