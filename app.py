from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_info = None
    questions = None
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            user_info = main.fetch_user_info(username)
        if 'start_date' in request.form and 'end_date' in request.form:
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            questions = main.fetch_daily_questions(start_date, end_date)
        if 'clear_user_info' in request.form:
            user_info = None
        if 'clear_questions' in request.form:
            questions = None
    return render_template('index.html', user_info=user_info, questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
