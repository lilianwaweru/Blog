from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User
from .forms import UpdateProfile
from .. import db,photos
from flask_login import login_required



@main.route('/')
def index():

    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html",user = user)


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

    return render_template('profile/update.html',form =form)


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

 @main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog(id):
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data

        new_blog = Blog(id=id,title=title,content=content,category=category,posted=posted,,comment=comment)
        new_blog.save_blog()
        return redirect(url_for('index.html'))
    title = 'New Blog'
    return render_template('new_blog.html',title=title,blog_form=form)

 @main.route('/Blog', methods = ['GET', 'POST'])
@login_required
def blogs():
    blog_form = BlogForm()
    
    if blog_form.validate_on_submit():
        blog = blog_form.blog.data
        cat = blog_form.category.data

        new_blog = Blog(content=blog, category = cat)
        new_pitch.save_pitch()

        return redirect(url_for('main.blogs'))

    all_blogs = Blog.get_all_blogs()
    
    return render_template('new_blog.html', blog_form = blog_form, blogs = all_blogs)
   
@main.route('/comments/<int:id>',methods = ['GET','POST'])
def comment(id):
    
    my_blog = Blog.query.get(id)
    comment_form = CommentForm()

    if id is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_data = comment_form.comment.data
        new_comment = Comment(comment = comment_data, blog_id = id)
        new_comment.save_comment()

        return redirect(url_for('main.comment',id=id))

    all_comments = Comment.get_comment(id)


    return render_template('comments.html',blog = my_blog, comment_form = comment_form, comments = all_comments)  