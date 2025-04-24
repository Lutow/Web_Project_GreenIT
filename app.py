from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def signup():
    return render_template('register.html')


@app.route('/about')
def aboutus():
    return render_template('aboutus.html')


def send_stats():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        socketio.emit('update', {'cpu': cpu, 'memory': memory})
        time.sleep(1) 


@socketio.on('connect')
def connect():
    print('Client connected')
    threading.Thread(target=send_stats, daemon=True).start()


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
