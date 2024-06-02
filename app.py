from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, leave_room, emit, join_room
from flask_cors import CORS
import eventlet
import eventlet.wsgi

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'  # 보안을 위해 환경 변수에서 불러오도록 설정
app.config['CORS_HEADERS'] = 'Content-Type'

# CORS 정책 설정
CORS(app, resources={r"/*": {"origins": "*"}})

# SocketIO 초기화
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
    username = session['username']
    room = session['room']
    return render_template('chat.html', username=username, room=room)

@socketio.on('join', namespace='/chat')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    emit('status', {'msg': f'{username} has joined the room.'}, room=room)

@socketio.on('message', namespace='/chat')
def message(message):
    emit('message', {'msg': f"{message['username']}: {message['msg']}"}, room=message['room'])

@socketio.on('leave', namespace='/chat')
def leave(message):
    username = message['username']
    room = message['room']
    leave_room(room)
    emit('status', {'msg': f'{username} has left the room.'}, room=room)

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Prevent caching
    return response

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
