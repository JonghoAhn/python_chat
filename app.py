from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key ='mosan'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("event")
def event_handler(json):
    if "data" in json:
        if json["data"] == "Connect":
            socketio.emit("response", {"nickname": "", "message": "새로운 유저 입장"})
    else:
        nickname = json["nickname"].encode("utf-8").decode("utf-8")
        message = json["message"].encode("utf-8").decode("utf-8")
        socketio.emit("response", {"nickname": nickname, "message": message})

if __name__ == '__main__':
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
