from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    media = StringField('media', validators=[DataRequired()])
    title = StringField('Item title', validators=[DataRequired()])
    author = StringField('Author')
    year = StringField('Year')
