from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['SECRET_KEY'] = 'mosan'
socketio = SocketIO(app, cors_allowed_origins="*")




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
    username = message['username']
    room = message['room']
    join_room(room)
    emit('status', {'msg': username + ' has joined the room.'}, room=room)

@socketio.on('message', namespace='/chat')
def message(message):
    emit('message', {'msg': message['username'] + ': ' + message['msg']}, room=message['room'])

@socketio.on('leave', namespace='/chat')
def leave(message):
    username = message['username']
    room = message['room']
    leave_room(room)
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)