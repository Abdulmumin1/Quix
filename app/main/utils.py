
import random
import os
import json


class QuestionHandler():
    def __init__(self):
        from ..models import Question
        self.all_questions = Question.query.all()
        self.no_of_questions = len(self.all_questions)
        self.previous_question = None
        self.previous_question_options = None
        self.previous_question_answered = False
        self.score = 0
        self.failed = 0
        self.answered_questions = []

    def random_question(self):
        if len(self.answered_questions) >= 10:
            return
        if not self.all_questions:
            return
        question = random.choice(self.all_questions)
        self.all_questions.remove(question)
        return question

    def get_question(self):
        # return new questions
        # if the previous question is not answered return it
        # if there is not previos qeustion create a new one
        from ..models import Answers
        pr = self.previous_question_answered

        if self.previous_question:
            question = self.random_question() if pr else self.previous_question
        else:
            question = self.random_question()

        if not question:
            return
        ans = Answers.query.get(question.id)
        options = [ans.a, ans.b, ans.c, ans.d]
        options = list(map(lambda x: x.title(), options))
        options = list(map(lambda x: x.strip(), options))
        random.shuffle(options)
        options = tuple(options)

        self.previous_question = question
        self.previous_question_answered = False
        self.previous_question_options = options

        return (question.question.strip(), options)

    def question_answer(self):
        correct_answer = self.previous_question.answer
        correct_answer = correct_answer.strip()
        correct_anwer = correct_answer.title()
        return correct_answer

    def progress_(self):
        total_question_n = 10
        total_question_answered = len(self.answered_questions)
        total_question_n = total_question_n if total_question_n > 10 else f"{total_question_n} "
        total_question_answered = total_question_answered if total_question_answered > 10 else f" {total_question_answered}"

        return total_question_n, total_question_answered


class UsersHandler:
    def __init__(self, session):
        self.session = session
        self.users = {}

    def get_user(self):
        username = self.session.get('username')
        if not self.users and username:
            self.session.pop('username')
            return
        return self.users[username]

    def add_user(self):
        id_ = self.session.get('username')
        self.users[id_] = UserObject(id_)

    def reset_user(self):
        id_ = self.session.get('username')
        self.users[id_] = UserObject(id_)

    def discard_user(self):
        del self.users[self.session.get('username')]
        self.session.pop('username')


class UserObject(QuestionHandler):
    def __init__(self, username):
        super().__init__()
        self._username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, name):
        return "username cannot be set"


def update_json(question, answer, options):

    # if not os.path.exists('questions_under_review.json'):
    #     jo = {"1": {"question": "who is the author?", "answer": "abdulmumin",
    #                 "options": ["abdulmumin", "ismail", "misbahu", "rahma", "kabir"]}}
    #     jf = json.dump(jo, open('questions.json', 'w'))

    json_file = json.load(open("questions.json", "r"))
    last_number = list(json_file.keys())[-1]

    options = list(map(lambda x: x.title(), options))
    options.append(answer)
    print(json_file)
    new = int(last_number)+1
    json_object = {}
    json_object["question"] = question.capitalize()
    json_object["answer"] = answer.title()
    json_object["options"] = options
    json_file[new] = json_object

    json.dump(json_file, open('questions_under_review.json', 'w'))
