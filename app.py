from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, leave_room,join_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mosan')  # 환경변수에서 비밀키를 가져오거나 기본값 사용
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('chat.html', username=username)

@socketio.on('message', namespace='/chat')
def message(message):
    emit('message', {'msg': f"{message['username']}: {message['msg']}"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

