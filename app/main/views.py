from . import main
from flask import render_template, session, redirect, jsonify, url_for, request, session
from .utils import UsersHandler, update_json, QuestionHandler

users = UsersHandler()


@main.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get('namefield', '')
        if username:
            session['username'] = username
            users.add_user()
            return redirect(url_for('main.questions'))

    username = session.get('username')
    if username:
        return redirect(url_for('main.questions'))
    return render_template('home.html')


@main.route('/quiz', methods=["GET", "POST"])
def questions():
    handler = QuestionHandler()

    if not handler:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        answer = request.form.get('a')
        correct_answer = handler.question_answer()
        print(answer, correct_answer)
        if answer.lower() == correct_answer.lower():
            print('Good')
            # session['scored'] += 1
        else:
            print('bad')
            # handler.failed += 1

        # handler_object = {}
        # handler_object['question'] = handler.previous_question.question
        # handler_object['options'] = handler.previous_question_options
        # handler_object['correct_answer'] = correct_answer
        # handler_object['picked_answer'] = answer

        # handler.answered_questions.append(handler_object)
        # handler.previous_question_answered = True

    question_answer = handler.get_question()
    if not question_answer:
        return redirect(url_for('main.dashboard'))
    question, answer = question_answer
    total_questions, answered_questions_len = handler.progress_()
    return render_template('quiz.html',
                           qs=question, ans=answer,
                           username=handler.username,
                           q_len=total_questions,
                           ansd_len=answered_questions_len)


@main.route('/quiz/submit', methods=["POST"])
def new_question():
    print(request.json)
    handler = QuestionHandler()
    answer = request.json.get('value')
    correct_answer = handler.question_answer()
    print(answer, correct_answer)
    if answer.lower() == correct_answer.lower():
        handler.save_score(True, fail=False)
        # print('good')
        # handler.score += 1
    else:
        handler.save_score(score=False, fail=True)
        # handler.failed += 1

    # handler_object = {}
    # handler_object['question'] = handler.previous_question.question
    # handler_object['options'] = handler.previous_question_options
    # handler_object['correct_answer'] = correct_answer
    # handler_object['picked_answer'] = answer

    # handler.answered_questions.append(handler_object)
    # handler.previous_question_answered = True
    handler.set_question_answered(correct_answer, answer)
    question_answer = handler.get_question()

    if not question_answer:
        return jsonify({"redirect": True})
    question, answer = question_answer
    total_questions, answered_questions_len = handler.progress_()

    return jsonify({"qs": question, "ans": answer, "q_len": total_questions, "ansd_len": answered_questions_len})


@main.route('/dashboard', methods=["GET", "POST"])
def dashboard():

    if request.method == 'POST':
        # del session['username']
        del session['activities']
        del session['prm']
        quest = request.form.get('quit')

        if not quest:
            # users.reset_user()
            return redirect(url_for('main.questions'))
        else:
            # users.discard_user()
            del session['username']
            return redirect(url_for('main.index'))

    # del session['activities']
    username = session.get('username')
    if not username:
        return redirect(url_for('main.index'))

    handler = QuestionHandler()
    score, failed = handler.get_scores()
    answered_questions = handler.get_answered_q()
    # del session['activities']

    # if not username:
    #     return redirect(url_for('main.index'))

    return render_template('dashboard.html', score=score, failed=failed, questions=answered_questions)


@main.route('/contribute', methods=["GET", "POST"])
def contribute():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('a')
        option_letters = ['b', 'c', 'd']
        options = [request.form.get(i, '') for i in option_letters]
        update_json(question, answer, options)
        options.insert(0, answer)
        return render_template('contribute.html', qs=question, ans=options)

    return render_template('contribute.html')
