from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, email_validator
from dotenv import load_dotenv
import os

load_dotenv()

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email.")])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    ckeditor.init_app(app, CKEDITOR_SERVE_LOCAL=True)