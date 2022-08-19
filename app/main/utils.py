from flask import session
import random
import os
import json
import secrets
from ..models import Question, Answers


class QuestionHandler():
    def __init__(self):
        # from ..models import Question
        self.username = session.get('username')

    def load_json(self):
        # self.all_questions = Question.query.all()
        # self.no_of_questions = len(self.all_questions)
        data = session.get('activities')
        data = json.loads(data)
        self.previous_question = self.return_question(data["q_id"])
        self.previous_question_options = data["options"]
        self.previous_question_answered = data["question_answered"]
        self.score = data["score"]
        self.failed = data["failed"]
        self.answered_questions = data['all_attended_question']
        self.attended_index = data["attended_index"]

    def random_question(self):
        data = session.get('prm', None)
        if not data:
            value = random.randint(1, 42)
            self.create_a_index()
            # self.load_json()
            self.add_q(value)
            return self.return_question(value), value
        # random.shuffle(self.all_questions)
        # if len(self.answered_questions) >= 10:
        #     return
        # if not self.all_questions:
        #     return
        # question = secrets.choice(self.all_questions)
        # self.all_questions.remove(question)
        data = json.loads(data)
        if len(data['attended_index']) >= 10:
            return None, None

        value = random.randint(1, 42)

        if value in data["attended_index"]:
            return self.random_question()
        else:
            self.add_q(value)
            return self.return_question(value), value
            # return question

    def return_question(self, ind):
        return Question.query.get(ind)

    def get_question(self):
        # return new questions
        # if the previous question is not answered return it
        # if there is not previos qeustion create a new one
        # from ..models import Answers

        data = session.get('activities', None)
        # data = json.loads(data)
        question, q_id = None, None
        if not data:
            print('\n no data \n')
            question, q_id = self.random_question()
            self.previous_question = self.return_question(q_id)
            # self.create_a_index()
        else:
            data = json.loads(data)
            # self.load_json()
            if not data['question_answered']:
                # q_id = data['q_id']
                question = self.return_question(data["q_id"])
            else:
                question, q_id = self.random_question()

        if not question:
            return

        print(data)
        ans = Answers.query.get(question.id)
        options = [ans.a, ans.b, ans.c, ans.d]
        options = list(map(lambda x: x.title(), options))
        options = list(map(lambda x: x.strip(), options))
        random.shuffle(options)
        options = tuple(options)

        # self.previous_question = question
        # self.previous_question_answered = False
        # self.previous_question_options = options

        current_question = question.question.strip()
        self.save_activities(q_id, current_question, options)

        return (current_question, options)

    def question_answer(self):
        data = session.get('activities', None)
        data = json.loads(data)
        # self.load_json()
        correct_answer = self.return_question(data['q_id']).answer
        correct_answer = correct_answer.strip()
        correct_anwer = correct_answer.title()
        return correct_answer

    def progress_(self):
        data = session['prm']
        data = json.loads(data)
        total_question_n = 10
        # data = session.get('')
        # total_question_answered = len(self.answered_questions)
        # total_question_n = total_question_n if total_question_n > 10 else f"{total_question_n} "
        total_question_answered = len(data['attended_index'])

        return total_question_n, total_question_answered

    def save_activities(self, q_id, current_question, options, start=True):
        data = {}
        # data['s']
        data["q_id"] = q_id
        data['score'] = 0
        data['failed'] = 0
        data["question"] = current_question
        data["options"] = options
        data["question_answered"] = False

        session["activities"] = json.dumps(data)

    def create_a_index(self):
        data = {}
        data['all_attended_question'] = []
        data['attended_index'] = []
        data['score'] = 0
        data['failed'] = 0
        session['prm'] = json.dumps(data)

    def set_question_answered(self, correct_answer, answer):
        data = session.get('activities')
        data = json.loads(data)

        data['question_answered'] = True
        # all_attended_question = data["all_attended_question"]

        handler_object = {}
        handler_object['question'] = data['question']
        handler_object['options'] = data['options']
        handler_object['correct_answer'] = correct_answer
        handler_object['picked_answer'] = answer

        # all_attended_question.append(handler_object)
        self.add_all_q(handler_object)

        session['activities'] = json.dumps(data)

    def save_score(self, score, fail):
        data = session['prm']
        data = json.loads(data)
        print(data)
        if score:
            data['score'] += 1
        else:
            data['failed'] += 1

        session['prm'] = json.dumps(data)

    # def add_config(key, value):
    #     data = session.get(key, None)
    #     data[]

    def add_q(self, q):
        data = session['prm']
        data = json.loads(data)

        if q in data['attended_index']:
            # print('\n\n\n aller \n\n')
            return
        else:
            # print('\n\n\n aller \n\n')
            data["attended_index"].append(q)
            session['prm'] = json.dumps(data)

    def add_all_q(self, q):
        data = session['prm']
        data = json.loads(data)
        data["all_attended_question"].append(q)
        session['prm'] = json.dumps(data)

    def get_scores(self):
        data = session['prm']
        data = json.loads(data)
        return data['score'], data['failed']

    def get_answered_q(self):
        data = session['prm']
        data = json.loads(data)
        return data['all_attended_question']


class UsersHandler:
    def __init__(self):
        self.session = session
        self.users = {}
        self.used_keys = set()

    def get_user(self):
        id_ = self.session.get('key')
        if not id_:
            return
        if not self.users and id_:
            self.session.pop('username')
            # self.session.pop('key')
            return
        return self.users[id_]

    def add_user(self):
        username = self.session.get('username')
        id_ = self.shorten()
        self.session['key'] = id_
        self.users[id_] = UserObject(username)

    def reset_user(self):
        username = self.session.get('username')
        id_ = self.session.get('key')
        self.users[id_] = UserObject(username)

    def discard_user(self):
        id_ = self.session.get('key')
        del self.users[id_]
        self.session.pop('username')
        self.used_keys.remove(id_)

    def shorten(self, nbytes: int = 5) -> str:
        ext = secrets.token_urlsafe(nbytes=nbytes)
        if ext in self.used_keys:
            return self.shorten(nbytes=nbytes)
        else:
            self.used_keys.add(ext)
            return ext

    # def save_session(self):


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
    "add questions to json file|"
    # if not os.path.exists('questions_under_review.json'):
    #     jo = {"1": {"question": "who is the author?", "answer": "abdulmumin",
    #                 "options": ["abdulmumin", "ismail", "misbahu", "rahma", "kabir"]}}
    #     jf = json.dump(jo, open('questions.json', 'w'))

    json_file = json.load(open("questions_under_review.json", "r"))
    last_number = list(json_file.keys())[-1]

    options = list(map(lambda x: x.title(), options))
    options.append(answer)
    print(question, answer, options)
    # print(json_file)
    new = int(last_number)+1
    json_object = {}
    json_object["question"] = question.capitalize()
    json_object["answer"] = answer.title()
    json_object["options"] = options
    json_file[new] = json_object

    json.dump(json_file, open('questions_under_review.json', 'w'))
