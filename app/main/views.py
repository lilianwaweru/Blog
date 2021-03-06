from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Blog,Comment
from .forms import UpdateProfile,BlogForm,CommentForm,DeleteForm
from .. import db,photos
from flask_login import login_required
import requests
import json
from ..email import mail_message


@main.route('/')
def index():
    

    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return render_template('index.html', random=random)

@main.route('/blogs/corporate')
def corporate():
    blogs = Blog.get_blog('Corporate')
    return render_template('corporate.html',blogs = blogs)  

@main.route('/blogs/personal')
def personal():
    blogs = Blog.get_blog('Personal')

    return render_template('personal.html',blogs = blogs)  

@main.route('/blogs/artist')
def artist():
    blogs = Blog.get_blog('Artist')

    return render_template('artist.html',blogs = blogs)  


@main.route('/blogs/guest')
def guest():
    blogs = Blog.get_blog('Guest')

    return render_template('guest.html',blogs = blogs)  


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
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        category = form.category.data

        new_blog = Blog()
        new_blog.save_blog()

        db.session.add(blog)
        db.session.commit()

        subscribers = Subscriber.query.all()
        for subscriber in subscribers:
            mail_message("New Blog Post", "email/new_blog", subscriber.email, subscriber = subscriber)

        return redirect(url_for('index.html'))
    title = 'New Blog'
    return render_template('new_blog.html',title=title,blog_form=form)

# @main.route('/Blogs', methods = ['GET', 'POST'])
# @login_required
# def blogs():
#     blog_form = BlogForm()
    
#     if blog_form.validate_on_submit():
#         blog = blog_form.blog.data
#         cat = blog_form.category.data

#         new_blog = Blog(content=blog, category = cat)
#         new_blog.save_blog()

#         return redirect(url_for('main.blogs'))

#     all_blogs = Blog.get_all_blogs()
    
#     return render_template('new_blog.html', blog_form = blog_form, blogs = all_blogs)
   
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

@main.route('/delete/<int:id>',methods = ['GET','POST'])
def delete(id):
    
    my_blog = Blog.query.get(id)
    delete_form = DeleteForm()
    if id is None:
        abort(404)

    if delete_form.validate_on_submit():
        delete = Comment.query.filter_by(comment = blog_id).all() 
        db.session.delete(delete)
        db.session.commit()
        

        return redirect(url_for('main.delete',id=id))

    return render_template("comments.html",delete_form = delete_form)


@main.route('/blog/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_blog(id):
    blog = Blog.get_blog(id)
    db.session.delete(blog)
    db.session.commit()

    return render_template('main.blog.html', id=id, blog = blog)  

