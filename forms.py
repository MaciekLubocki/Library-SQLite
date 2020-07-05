from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    media = SelectField(
        'Media', choices=[('Book', 'Book'), ('Audio CD', 'Audio CD'), ('DVD', 'DVD')]) # noqa
    title = StringField('Item title', validators=[DataRequired()])
    author = StringField('Author')
    year = StringField('Year')
