from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    blog = db.relationship('Blog',backref = 'users',lazy ="dynamic")
    comment = db.relationship('Comment',backref='users',lazy='dynamic')


    def __repr__(self):
        return f'User {self.username}'

    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(500))
    title = db.Column(db.String)
    category = db.Column(db.String)
    comment = db.relationship('Comment',backref = 'blogs',lazy ="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blog(id,category): 
        blog = blog.query.filter_by(category = category).all()
        return blog  

    @classmethod
    def get_all_blogs(cls):
       blogs = Blog.query.order_by('id').all()
       return blogs

    @classmethod
    def get_category(cls,cat):
       category = Blog.query.filter_by(blog_category=cat).order_by('id').all()
       return category

    def __repr__(self):
        return f'Blog {self.blog_title}, {self.category}'

 
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(id,blog):
        comment = Comment.query.filter_by(blog_id = blog).all()
        return comment

    def __repr__(self):
        return f'Comment{self.comment}'           