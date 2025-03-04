from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import main
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_info = None
    questions = None

    try:
        if request.method == 'POST':
            if 'username' in request.form:
                username = request.form['username']
                user_info = main.fetch_user_info(username)
            if 'start_date' in request.form and 'end_date' in request.form:
                start_date = request.form.get('start_date', '2020-04-01')
                end_date = request.form.get('end_date', datetime.now().strftime('%Y-%m-%d'))
                per_page = int(request.form.get('per_page', 10))
                questions = main.fetch_daily_questions(start_date, end_date)
    except Exception as e:
        logging.error(f"Error in index route: {e}")

    return render_template('index.html', 
                         user_info=user_info, 
                         questions=questions)

if __name__ == '__main__':
    app.run(debug=True)