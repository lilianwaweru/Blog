from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators=[Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    blog = TextAreaField('pitch',validators=[Required()])
    category = SelectField('Category',choices=[('Personal','Personal'),('Corporate','Corporate'),('Artist','Artist'),('Guest','Guest')],validators=[Required()]) 
    submit = SubmitField('submit') 

class CommentForm(FlaskForm):
    comment = TextAreaField('write your comment',validators=[Required()])
    submit = SubmitField('submit')       