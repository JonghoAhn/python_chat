from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

socketio = SocketIO(app, manage_session=False)
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['room'] = 'default_room'
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', username=session['username'], room=session['room'])

@socketio.on('join', namespace='/chat')
def join(message):
    username = session.get('username', '')
    room = session.get('room', '')
    join_room(room)
    emit('status', {'msg': f"{username} has joined the room."}, room=room)

@socketio.on('message', namespace='/chat')
def message(message):
    room = session.get('room', '')
    emit('message', {'msg': f"{session['username']}: {message['msg']}"}, room=room)

@socketio.on('leave', namespace='/chat')
def leave(message):
    username = session.get('username', '')
    room = session.get('room', '')
    leave_room(room)
    emit('status', {'msg': f"{username} has left the room."}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
