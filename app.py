import eventlet
eventlet.monkey_patch()                 # les 2 premières lignes sont à supprimer en cas de problème (Import pour monitor les perfs du pc host)
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import psutil
import time
import threading
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'my_secret_key'
socketio = SocketIO(app)

app.config["MONGO_URI"] = "mongodb+srv://Nicolas:shrek123@cluster0.ywwcgdb.mongodb.net/quizdb"
mongo = PyMongo(app)

@app.route('/')
def menu():
    user_info = {
        'username': session.get('user'),
        'logged_in': 'user' in session
    }
    return render_template('menu.html',user_info=user_info)


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/about')
def aboutus():
    return render_template('aboutus.html')
    

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Extract the form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the user in the database
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash("Logged in successfully.", "success-log")
            return redirect(url_for("menu"))
        else:
            flash("Invalid username or password.", "fail-log")
            return redirect(url_for("login"))
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the username already exists
        if mongo.db.users.find_one({'username': username}):
            flash("Username already exists!", "name-error")
            return redirect(url_for("register"))

        if mongo.db.users.find_one({'email': email}):
            flash("Email address already associated to a user!", "mail-error")
            return redirect(url_for("register"))

        # Securely hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new user document. The 'scores' field will store quiz results.
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'scores': []  # Each score: {'quiz_id': ..., 'score': ..., 'date': ...}
        })
        flash("Registration successful. Please login.", "sucessful-register")
        return redirect(url_for("login"))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('menu'))


@app.route('/profile')
def profile():
    if 'user' not in session:
        flash("Please log in to access your profile.", "no-log")
        return redirect(url_for('login'))

    # Fetch user data
    user = mongo.db.users.find_one({'username': session['user']})
    if not user:
        flash("User not found.", "user-not-found")
        return redirect(url_for('menu'))
    return render_template('profile.html', user=user)


@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        flash("Please log in to update your profile.", "nolog-profile")
        return redirect(url_for('login'))

    # Get form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Prepare update fields
    update_fields = {}
    if username:
        update_fields['username'] = username
    if email:
        update_fields['email'] = email
    if password:  # Hash the new password
        update_fields['password'] = generate_password_hash(password)

    # Update user in database
    mongo.db.users.update_one(
        {'username': session['user']},
        {'$set': update_fields}
    )

    # Update session username if it was changed
    if 'username' in update_fields:
        session['user'] = update_fields['username']

    flash("Your profile has been updated successfully.", "update-profile")
    return redirect(url_for('profile'))


@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    if 'user' not in session:
        flash("Veuillez vous connecter pour soumettre un quiz.", "quiz-no-log")
        return redirect(url_for('login'))

    quiz_id = request.form.get('quiz_id')
    if not quiz_id:
        flash("Quiz non identifié.", "danger")
        return redirect(url_for('quiz'))
    try:
        quiz_id = int(quiz_id)
    except ValueError:
        flash("ID du quiz invalide.", "danger")
        return redirect(url_for('quiz'))

    correct_answers = {
        1: {'q1': 'c', 'q2': 'a', 'q3': 'd', 'q4': 'b'},  # Quiz 1
        2: {'q1': 'b', 'q2': 'd', 'q3': 'a', 'q4': 'c'},  # Quiz 2
        3: {'q1': 'a', 'q2': 'b', 'q3': 'd', 'q4': 'a'},  # Quiz 3
        4: {'q1': 'a', 'q2': 'a', 'q3': 'b', 'q4': 'c'}  # Quiz 4
    }

    score = 0
    quiz_answers = correct_answers.get(quiz_id, {})
    for question, correct_response in quiz_answers.items():
        if request.form.get(question) == correct_response:
            score += 1
    score_record = {
        'quiz_id': quiz_id,
        'score': score,
        'date': datetime.now()
    }
    mongo.db.users.update_one(
        {'username': session['user']},
        {'$push': {'scores': score_record}}
    )
    flash(f"Quiz {quiz_id} soumis. Votre score: {score} / {len(quiz_answers)}", "quiz-submit")
    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    if 'user' not in session:
        flash("Veuillez vous connecter pour accéder aux quiz.", "danger")
        return redirect(url_for('login'))
    user = mongo.db.users.find_one({'username': session['user']})
    return render_template('quiz.html', user=user)

def send_stats():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        socketio.emit('update', {'cpu': cpu, 'memory': memory})
        time.sleep(1)  # Send data every second


@socketio.on('connect')
def connect():
    print('Client connected')
    threading.Thread(target=send_stats, daemon=True).start()


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
