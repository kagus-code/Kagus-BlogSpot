from flask import render_template, request,redirect, url_for,abort,flash
from .forms import UpdateProfile,SubmitBlog,postComment
from .. import db,photos
from . import main
from flask_login import login_required,current_user
from ..models import User,Blog,Comment
import markdown2  
from ..request import get_quotes

@main.route('/')
def index():
    all_blogs= Blog.query.all()
    
    all_quotes = get_quotes()
    author = all_quotes.get("author")
    quote = all_quotes.get("quote")
    print(type(all_blogs))


    title = 'Kagus-BlogSpot Home Page'
    return render_template('index.html', title = title, blogs = all_blogs,author=author,quote=quote)


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


@main.route('/post/<int:id>')
def single_post(id):
    post=Blog.query.get(id)
    print (post)
    if post is None:
        abort(404)
    format_post = markdown2.markdown(post.blog_post,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('post.html',post = post,format_post=format_post)


@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
@login_required
def comments(blog_id):
    form = postComment()
    blog = Blog.query.get(blog_id)
    display_blog_comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment,blog_id=blog_id, user_id = user_id)
        new_comment.save_comment()
        return redirect(url_for('main.comments',blog_id=blog_id))

    return render_template('comment.html',comments = display_blog_comments,the_blog=blog,form=form)    


@main.route('/delete_comment/<int:user_id>/<int:blog_id>',methods = ['POST','GET'])
@login_required
def delete_comment(user_id,blog_id):
    blog = Blog.query.get(blog_id)
    user = Blog.query.get(user_id)
    comment = Comment.query.filter_by(blog_id=blog_id).first()
    

    if user_id == current_user.id:

        print(comment)
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('main.comments',blog_id=blog_id))

    else:
        print("you cant delete comment")
        flash('Cannot delete comment,You are not the author of this blog')

    return redirect(url_for('main.comments',blog_id=blog_id))

