from . import db

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
