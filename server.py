import re
import smtplib
import pandas as pd
import csv
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect
# from flask_mail import Mail, Message


app = Flask(__name__)


@app.route('/index.html')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def page_name(page_name):
    return render_template(page_name)

# @app.route('/work_exp_IT.html')
# def work_exp_IT():
#     return render_template('work_exp_IT.html')

# def send_email(data):
#     mail= Mail(app)
#     app.config['MAIL_SERVER']='smtp.gmail.com'
#     app.config['MAIL_PORT'] = 465
#     app.config['MAIL_USERNAME'] = 'dbshoy@gmail.com'
#     app.config['MAIL_PASSWORD'] = 'XXXXX'
#     app.config['MAIL_USE_TLS'] = False
#     app.config['MAIL_USE_SSL'] = True
#     mail = Mail(app)
#     msg = Message('From your website', sender = data['email'], recipients = ['dbshoy@gmail.com'])
#     msg.body = data['message']
#     mail.send(msg)

def is_valid_email(email):
    """Validate email using regular expressions."""
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Use the match() function to check if the email matches the pattern
    match = re.match(pattern, email)
    return match is not None

def write_to_txt(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        name = data['name']
        message = data['message']
        database.write(f'\n{name},{email},{message}')

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        email = data['email']
        name = data['name']
        message = data['message']
        csv_file = csv.writer(database, delimiter=',')
        csv_file.writerow([name, email, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        email = data['email']
        if is_valid_email(email):
            write_to_csv(data)
            # TODO https://www.letscodemore.com/blog/smtplib-smtpauthenticationerror-username-and-password-not-accepted/
            # send_email(data)
            return render_template('/thank_you.html', name=data['name'])
        else:
            return render_template('/email_invalid.html', email=email)
        # return redirect('/thankyou.html')
    else:
        return data
