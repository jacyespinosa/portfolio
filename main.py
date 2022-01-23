from flask import Flask, render_template, redirect, url_for, request, flash
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import smtplib
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

#SMTP
MY_EMAIL = os.getenv('EMAIL')
MY_PASSWORD = os.getenv('PASSWORD')
TO_ADDRESS = os.getenv('TO_ADDRESS')


@app.route('/', methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        if request.form['name'] == '' or request.form['email'] == '' or request.form['message'] == '':
            flash('Please fill out the fields correctly.')
            return redirect(url_for('home'))

        else:
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs=TO_ADDRESS,
                                    msg=f"Subject: You have a message!\n\n"
                                        f"Name: {name}\n"
                                        f"Email: {email}\n\n"
                                        f"Message: {message}")

            flash('Message successfully sent.')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    ckeditor.init_app(app, CKEDITOR_SERVE_LOCAL=True)