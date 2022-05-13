from flask import Flask, render_template, session, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = 'o9rew908qre3qr3$TEw3qejrewqopreREWQr'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
users = {}


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
		self.previous_question_options = None
		self.previous_question_answered = False
		self.score = 0
		self.failed = 0
		self.answered_questions = []


	def random_question(self):
		if not self.all_questions:
			return
		question = random.choice(self.all_questions)
		self.all_questions.remove(question)
		return question
	

	def get_question(self):
		#return new questions
		#if the previous question is not answered return it
		#if there is not previos qeustion create a new one

		pr = self.previous_question_answered
		
		if self.previous_question:
			question = self.random_question() if pr else self.previous_question
		else:
			question = self.random_question()


		if not question:
			return
		ans = Answers.query.get(question.id)
		options = (ans.a, ans.b, ans.c, ans.d)

		self.previous_question = question
		self.previous_question_answered = False
		self.previous_question_options = options
		return (question.question, options)


@app.route('/', methods=["GET", "POST"])
def index():

	if request.method == "POST":
		username = request.form.get('namefield', '')
		if username:
			session['username'] = username
			global users
			users[username] = QuestionHandler()
			
			return redirect(url_for('questions'))

	username = session.get('username')
	if username:
		return redirect(url_for('questions'))
	return render_template('home.html')

@app.route('/quiz', methods=["GET", "POST"])
def questions():
	username = session.get('username')
	if not username:
		return redirect(url_for('index'))
	handler = users[username]

	if request.method == 'POST':
		answer = request.form.get('a')
		correct_answer = handler.previous_question.answer
		print(answer, correct_answer)
		if answer == handler.previous_question.answer:
			handler.score += 1
		else:
			handler.failed += 1

		handler_object = {}
		handler_object['question'] = handler.previous_question.question
		handler_object['options'] = handler.previous_question_options
		handler_object['correct_answer'] = handler.previous_question.answer
		handler_object['picked_answer'] = answer

		handler.answered_questions.append(handler_object)
		handler.previous_question_answered = True


	question_answer = handler.get_question()
	if not question_answer:
		return redirect(url_for('dashboard'))
	question,answer = question_answer

	return render_template('quiz.html', qs=question,ans=answer,username=session.get('username'))

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
	username = session.get('username')
	handler = users[username]
	if request.method == 'POST':
		quest = request.form.get('quit')
		
		if not quest:	
			users[username] = QuestionHandler()
			return redirect(url_for('questions'))
		else:
			session.pop('username')
			del users[username]
			return redirect(url_for('index'))

	
	if not username:
		return redirect(url_for('index'))

	return render_template('dashboard.html', score=handler.score, failed=handler.failed, questions=handler.answered_questions)