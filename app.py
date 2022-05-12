from flask import Flask, render_template, session, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = 'o9rew908qre3qr3$TEw3qejrewqopreREWQr'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
handler = None

class Question(db.Model):
	__tablename__ = 'questions'
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String, nullable=False)
	answer = db.Column(db.String(20))
	

class Answers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	a = db.Column(db.String(20), nullable=False)
	b = db.Column(db.String(20), nullable=False)
	c = db.Column(db.String(20), nullable=False)
	d = db.Column(db.String(20), nullable=False)
	q_id = db.Column(db.Integer, db.ForeignKey('questions.id'))


class QuestionHandler():
	def __init__(self):
		self.all_questions = Question.query.all()
		self.previous_question = None
		self.score = 0
		self.failed = 0


	def random_question(self):
		question = random.choice(self.all_questions)
		self.all_questions.remove(question)
		return question
	def get_question(self):
		question = self.random_question()
		ans = Answers.query.get(question.id)
		options = (ans.a, ans.b, ans.c, ans.d)

		self.previous_question = question
		return (question.question, options)

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		username = request.form.get('namefield', '')
		if username:
			session['username'] = username
			global handler
			handler = QuestionHandler()
			return redirect(url_for('questions'))

	username = session.get('username')
	if username:
		return redirect(url_for('questions'))
	return render_template('home.html')

@app.route('/quiz', methods=["GET", "POST"])
def questions():
	if request.method == 'POST':
		answer = request.form.get('a')
		if answer == handler.previous_question:
			handler.score += 1
		else:
			handler.failed += 1

	question_answer = handler.get_question()
	question,answer = question_answer

	return render_template('quiz.html', qs=question,ans=answer,username=session.get('username'))

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
	
	if request.method == 'POST':
		quest = request.form.get('quit')
		
		if not quest:
			global handler
			handler = QuestionHandler()
			return redirect(url_for('questions'))
		else:
			return redirect(url_for('index'))

	username = session.get('username')
	if not username:
		return redirect(url_for('index'))

	return render_template('dashboard.html', score=handler.score, failed=handler.failed)