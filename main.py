import os
import numpy as np
import pandas as pd
import sklearn
import tweepy
import csv
import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,RadioField)
from wtforms.validators import InputRequired, Length
import sqlite3
import joblib

from flask import Flask, render_template
import plotly.express as px
import pandas as pd

sentimental_scores = [0.8, 0.6, 0.7, 0.5, 0.9, 0.4, 0.6, 0.8, 0.7, 0.5, 0.8, 0.6, 0.7, 0.5, 0.9, 0.8]


data = {
    'Personality Type': ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP',
                         'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'],
    'Extroverted': [3, 2, 2, 1, 4, 3, 2, 1, 4, 5, 4, 5, 3, 3, 4, 5],
    'Intuitive': [1, 1, 2, 2, 4, 5, 5, 4, 1, 2, 5, 5, 1, 2, 5, 4],
    'Feeling': [1, 2, 4, 1, 1, 2, 4, 2, 1, 4, 5, 3, 1, 4, 5, 3],
    'Judging': [5, 5, 5, 5, 1, 2, 3, 2, 1, 3, 3, 3, 5, 5, 4, 5],
    'Sentimental Score': sentimental_scores
}


df = pd.DataFrame(data)

df_melted = pd.melt(df, id_vars=['Personality Type', 'Sentimental Score'], var_name='Trait', value_name='Strength')

# Create a Bar chart with Sentimental Scores
fig_bar = px.bar(df_melted, x='Personality Type', y='Strength', color='Trait',
                 title='MBTI Personality Traits Strengths with Sentimental Scores (Bar)',
                 height=500, hover_data=['Sentimental Score'])

# Save the interactive chart as an HTML file
fig_bar.write_html("templates/AnalyticsPage_BarChart.html")


def currtime():
    # Get the current date and time
    current_time = datetime.datetime.now()

    # Format the current time as a string
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Print the formatted time
    print("Current Time:", time_string)


currtime()
#-------------------------------------------------model_code------------------------------------------------------------

conn = sqlite3.connect('covid_database')
cur = conn.cursor()
try:
   cur.execute('''CREATE TABLE user (
     name varchar(20) DEFAULT NULL,
      email varchar(50) DEFAULT NULL,
     password varchar(20) DEFAULT NULL,
     gender varchar(10) DEFAULT NULL,
     age int(11) DEFAULT NULL
   )''')

except:
   pass
#!/usr/bin/env python
# coding: utf-8
consumer_key = 'OvyRyCwdl4VMnbfoTGGkMahLI'
consumer_secret = 'pCdde0XPBlJ8oeC9dtuSRoNXD5H6mW45ZzmwXjj1xbXMu6Lcrk'
access_key = '787266131476226048-0h3Gz2GchMSYeQEq2d8F9qgaxBOFXIS'
access_secret = 'YNBqfDodwWlkdRVaR4iaIGAj2arIyAHhLeaLDRgVGPK1B'



currtime()
#reading the dataset
data = pd.read_csv('mbti_1.csv')
X = data.posts
Y = data.type

from sklearn.linear_model import LogisticRegression

from sklearn.feature_extraction.text import CountVectorizer

cv = None
def readycv():
    global cv
    global X
    cv = CountVectorizer()
    X = cv.fit_transform(X)

currtime()

from sklearn.model_selection import train_test_split
# X_train , X_test , Y_train , Y_test = train_test_split(X,Y,test_size=20,random_state=100)

# clf_LR = LogisticRegression(max_iter=100,C=1)
# clf_LR.fit(X_train,Y_train)

# Define the file name for the saved model

# Check if the saved model file exists


model_file = 'logistic_regression_model.pkl'
if os.path.exists(model_file):
    # Load the saved model
    clf_LR = joblib.load(model_file)
    print("Loaded the saved model.")
else:
    # Train a new model
    readycv()
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=20, random_state=100)
    clf_LR = LogisticRegression(max_iter=100, C=1)
    clf_LR.fit(X_train, Y_train)
    print("Trained a new model.")

    # Save the trained model for future use
    joblib.dump(clf_LR, model_file)
    print("Saved the model.")

# y_pred_LR  = clf_LR.predict(X_test)
# from sklearn.metrics import accuracy_score
# print(accuracy_score(y_pred_LR,Y_test))
# score_lr = accuracy_score(y_pred_LR,Y_test)

from flask import Flask,render_template, url_for,request, flash, redirect, session, jsonify
from chat import get_response
app = Flask(__name__)
app.config['SECRET_KEY'] = '881e69e15e7a528830975467b9d87a98'

#-------------------------------------home_page-------------------------------------------------------------------------
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/')
@app.route('/home')
def home():
   if not session.get('logged_in'):
      return render_template('home.html')
   else:
      return redirect(url_for('user_account'))
#-------------------------------------about_page-------------------------------------------------------------------------
@app.route("/about")
def about():
   return render_template('about.html')
#-------------------------------------ratings_page-------------------------------------------------------------------------
@app.route("/ratings")
def ratings():
   return render_template('ratings.html')
#-------------------------------------user_login_page-------------------------------------------------------------------------
@app.route('/user_login',methods = ['POST', 'GET'])
def user_login():
   conn = sqlite3.connect('covid_database')
   cur = conn.cursor()
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['psw']
      print('asd')
      count = cur.execute('SELECT * FROM user WHERE email = "%s" AND password = "%s"' % (email, password))
      print(count)
      #conn.commit()
      #cur.close()
      l = len(cur.fetchall())
      if l > 0:
         flash( f'Successfully Logged in' )
         return render_template('user_account.html')
      else:
         print('hello')
         flash( f'Invalid Email and Password!' )
   return render_template('user_login.html')

# -------------------------------------user_login_page-----------------------------------------------------------------

# -------------------------------------user_register_page-------------------------------------------------------------------------

@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
   conn = sqlite3.connect('covid_database')
   cur = conn.cursor()
   if request.method == 'POST':
      name = request.form['uname']
      email = request.form['email']
      password = request.form['psw']
      gender = request.form['gender']
      age = request.form['age']
      cur.execute("insert into user(name,email,password,gender,age) values ('%s','%s','%s','%s','%s')" % (name, email, password, gender, age))
      conn.commit()
      # cur.close()
      print('data inserted')
      return redirect(url_for('user_login'))

   return render_template('user_register.html')
#-------------------------------------user_register_page-------------------------------------------------------------------------

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    posts = request.form['posts']
    global clf_LR
    global cv
    if request.method == 'POST':
        if (not cv): readycv()
        vect = cv.transform([posts]).toarray()
        my_prediction = clf_LR.predict(vect)
        print('my_prediction', my_prediction[0])
        flash(f'The personality is {my_prediction[0]}')
    return render_template('user_account.html')

@app.route('/get_tweet', methods=['POST', 'GET'])
def get_tweet():
   global INFJ, ENTP, INTP, INTJ, ENTJ, ENFJ, INFP, ENFP, ISFP, ISTP, ISFJ, ISTJ, ESTP, ESFP, ESTJ, ESFJ
   username = request.form['Name']
   # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_key, access_secret)
   api = tweepy.API(auth)
   # set count to however many tweets you want
   number_of_tweets = 100
   # get tweets
   tweets_for_csv = []
   # Open/Create a file to append data
   csvFile = open(username[1:] + '.csv', 'a')
   # Use csv Writer
   csvWriter = csv.writer(csvFile)
   for tweet in tweepy.Cursor(api.search, q=username, count=100, lang="en", since="2017-04-03").items(number_of_tweets):
      print(tweet.created_at, tweet.text)
      csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
   return render_template('enter.html')

@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    if request.method == 'POST':
        f = request.files['file']
        name = f.filename
        #obj = File_Pass(name)
        global cv
        if (not cv): readycv()
        vect = cv.transform([name]).toarray()
        my_prediction = clf_LR.predict(vect)
        print('my_prediction', my_prediction[0])
        flash(f'The personality is {my_prediction[0]}')
        return render_template('user_account.html')

# ------------------------------------predict_page-----------------------------------------------------------------

#---------------------------------- quiz page -----------------------------------------------------------------------




questions = [
    ("How do you typically react when faced with a challenge or problem?", [
        ('I stay calm and analyze the situation.', 'a'),
        ('I feel anxious and seek advice from others.', 'b'),
        ('I assess the situation and consult with a mentor or experienced individual.', 'c'),
        ('I immediately take action, trusting my instincts to guide me.', 'a'),
    ]),
    ("In a group setting, are you more likely to:", [
        ('Take charge and make decisions.', 'a'),
        ('Listen and follow the group\'s lead.', 'b'),
        ('Contribute ideas and suggestions.', 'c'),
        ('Facilitate and ensure everyone\'s opinion is heard.', 'd'),
        ('Adapt and go with the flow of the group.', 'e'),
        ('Analyze the situation and provide a thoughtful response.', 'f'),
        ('Encourage collaboration and teamwork.', 'g'),
        ('Challenge ideas and stimulate debate.', 'h'),
    ]),
    ("When making a major life decision, what's more important to you?", [
        ('Logic and practicality.', 'a'),
        ('Emotions and personal values.', 'b'),
        ('Consulting with trusted friends or family.', 'c'),
        ('Considering long-term consequences.', 'd'),
        ('Seeking advice from experts or professionals.', 'e'),
        ('Weighing pros and cons thoroughly.', 'f'),
        ('Trusting your intuition or gut feeling.', 'g'),
        ('Exploring creative and innovative solutions.', 'h'),
    ]),
    ("How do you prefer to spend your free time?", [
        ('Engaging in structured activities or hobbies.', 'a'),
        ('Exploring new ideas and possibilities.', 'b'),
        ('Connecting with friends and socializing.', 'c'),
        ('Immersing yourself in artistic or creative pursuits.', 'd'),
        ('Reading and gaining knowledge.', 'e'),
        ('Participating in physical activities or sports.', 'f'),
    ]),
    ("When working on a project, do you tend to:", [
        ('Create detailed plans and stick to them.', 'a'),
        ('Adapt and change course as needed.', 'b'),
    ]),
    ("How do you handle criticism or negative feedback?", [
        ('Analyze it objectively and look for improvement.', 'a'),
        ('Take it personally and feel hurt.', 'b'),
    ]),
    ("When meeting new people, are you more likely to:", [
        ('Start conversations and initiate interactions.', 'a'),
        ('Wait for others to approach you.', 'b'),
    ]),
    ("What describes your communication style best?", [
        ('I\'m straightforward and to the point.', 'a'),
        ('I\'m more indirect and considerate of others\' feelings.', 'b'),
    ]),
    ("How do you approach time management?", [
        ('I like to plan my schedule and adhere to it.', 'a'),
        ('I prefer flexibility and adaptability in my schedule.', 'b'),
    ]),
    ("When it comes to decision-making, do you rely more on:", [
        ('Facts and data.', 'a'),
        ('Intuition and gut feeling.', 'b'),
    ]),
    ("How do you recharge or relax after a busy day?", [
        ('Spend time with friends or in a social setting.', 'a'),
        ('Have some alone time or engage in solitary activities.', 'b'),
    ]),
    ("How do you deal with a messy or disorganized environment?", [
        ('It bothers me, and I like to tidy up.', 'a'),
        ('I\'m comfortable with some level of chaos.', 'b'),
    ]),
]


# Create a form using Flask-WTF
class QuizForm(FlaskForm):
   pass

for i, (question, choices) in enumerate(questions, start=1):
    setattr(QuizForm, f'question_{i}', RadioField(question, choices=[(choice[0], choice[0]) for choice in choices], validators=[InputRequired()]))

@app.route('/quiz')
def quiz():
    form = QuizForm()
    print(form._fields.items())
    return render_template('quiz.html', form=form, questions=questions)

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/analytics')
def index():
    return render_template('AnalyticsPage_BarChart.html')

@app.get('/predict1')
def index_get():
   return render_template("chat.html")
@app.post('/predict1')
def predict1():
   text = request.get_json().get("message")
   response = get_response(text)
   #    print(response,response.replace('\n','<br\>'))
   message = {"answer" : response.replace('\n','<br>')}
   return jsonify(message)


@app.route('/process', methods=['POST'])
def process():
   data = request.form.get('data')
   return f'You submitted: {data}' 


@app.route('/runfile', methods=['POST'])
def runfile():
    # Check if a file was included in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    # If a file is provided, process it
    if file:
        # Read the content of the file as a string
        file_contents = file.read().decode('utf-8')

        # Get the file name and size
        filename = file.filename
        file_size = len(file_contents)

        global cv
        if (not cv): readycv()
        vect = cv.transform([file_contents]).toarray()
        my_prediction = clf_LR.predict(vect)
        print('my_prediction', my_prediction[0])
        link = '\\result\\'+my_prediction[0]

        # Create a JSON response with filename, file size, and the file content
        data_rs = {
            "filename": filename,
            "file_size": file_size,
            # "file_content": file_contents,
            "result":"Personality prediction is " + str(my_prediction[0])+'<br> For Further information checkout '+f'<a href="{link}">click here </a\>'
        }
        return jsonify(data_rs)


@app.route('/textprocess', methods=['POST'])
def textprocess():
    data = request.get_json()

    if 'message' not in data:
        return jsonify({"error": "No 'message' field in the request"})

    user_text = data['message']

    if not user_text:
        return jsonify({"error": "Empty message"})

    global cv  # You should have the cv (CountVectorizer) and clf_LR (Logistic Regression) models defined
    if not cv:
        readycv()

    vect = cv.transform([user_text]).toarray()
    my_prediction = clf_LR.predict(vect)
    print('my_prediction', my_prediction[0])
    link = '\\result\\'+my_prediction[0]

    data_rs = {
        "user_text": user_text,
        "result": "Personality prediction is " + str(my_prediction[0])+'<br> For Further information checkout '+f'<a href="{link}">click here </a>'
    }
    
    return jsonify(data_rs)

@app.route('/questions5', methods=['GET'])
def get_random_questions():
    # Shuffle the questions to get random order
    import random
    random.shuffle(questions)

    # Select the first 5 questions from the shuffled list
    selected_questions = questions[:5]

    # Structure the questions in a response JSON format
    response_data = {
        "questions": [
            {"question": question[0], "options": question[1]} for question in selected_questions
        ]
    }
    return jsonify(response_data)


@app.route('/processanswers', methods=['POST'])
def process_answers():
    # try:
    # Receive answers from the user as JSON data
    user_answers = request.get_json()

    # Process the user's answers (you can customize this part)
    # For example, you can calculate a result based on the answers received
    result = process_answers_logic(user_answers)

    # Create a response JSON with the result
    link = '\\result\\'+result
    response_data = {
        "result": "Personality prediction is " + str(result)+'<br> For Further information checkout '+f'<a href="{link}">click here </a>'
    }

    return jsonify(response_data)

    # except Exception as e:
    #     # Handle any exceptions or errors here
    #     return jsonify({"error": str(e)})

def process_answers_logic(user_answers):
    # Customize this function to process the user's answers and calculate the result.
    # For example, you can calculate a score based on the selected options in the answers.
    # This function should return a result based on your specific logic.
    # Here's a simple example:

    score = 0

    print(user_answers)
    text = ""
    for answer in user_answers["answers"]:
        # In this example, we assume 'a' answers are worth 1 point and 'b' answers are worth 2 points.
        text+=answer["answer"]+". ||"
        print(answer)
    
    global cv
    if(not cv): readycv()
    print(text)
    vect = cv.transform([text]).toarray()
    my_prediction = clf_LR.predict(vect)
    return my_prediction[0]



imagesDict = {}


@app.route('/result/<string:personality>')
def personality(personality):
    content=open(f"{personality}.txt").read()
    imgurl = imagesDict.get(
        personality,"https://www.16personalities.com/static/images/personality-types/headers/diplomats_Protagonist_ENFJ_personality_header.svg"
    )
    return render_template('Results.html',content = content,image = imgurl,personality=personality)



if __name__ == '__main__':
   app.secret_key = os.urandom(12)
   app.run(debug=True)