from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddCafe(FlaskForm):
    name = StringField(label ='Cafe Name', validators=[DataRequired()])
    location = StringField(label='Location', validators=[DataRequired()])
    wifi = SelectField(label='Wifi Connection', choices=['', 'Strong', 'Moderate', 'Weak', 'None'], validators=[DataRequired()])
    coffee_price = StringField(label= 'Coffee Price Range', validators=[DataRequired()])
    environment = StringField(label='Short Review', validators=[DataRequired()])
    overall_rating = StringField(label='Rating (only whole number ratings)', validators=[DataRequired()])
    submit = SubmitField('Submit')