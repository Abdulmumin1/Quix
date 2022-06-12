from . import main
from flask import render_template, session, redirect, url_for, request, session
from .utils import UsersHandler, update_json

users = UsersHandler(session)


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
    handler = users.get_user()

    if not handler:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        answer = request.form.get('a')
        correct_answer = handler.question_answer()
        print(answer, correct_answer)
        if answer.lower() == correct_answer.lower():
            handler.score += 1
        else:
            handler.failed += 1

        handler_object = {}
        handler_object['question'] = handler.previous_question.question
        handler_object['options'] = handler.previous_question_options
        handler_object['correct_answer'] = correct_answer
        handler_object['picked_answer'] = answer

        handler.answered_questions.append(handler_object)
        handler.previous_question_answered = True

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


@main.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    username = session.get('username')
    handler = users.get_user()
    if request.method == 'POST':
        quest = request.form.get('quit')

        if not quest:
            users.reset_user()
            return redirect(url_for('main.questions'))
        else:
            users.discard_user()
            return redirect(url_for('main.index'))

    if not username:
        return redirect(url_for('main.index'))

    return render_template('dashboard.html', score=handler.score, failed=handler.failed, questions=handler.answered_questions)


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
