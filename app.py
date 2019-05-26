from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

players = []
number = 0


@socketio.on('join', namespace='/test')
def on_join(data):
    #app.logger.info('someone joined')
    #app.logger.info(data['data']['form_data'])
    username = data['data']['username']
    room = data['data']['room']
    imageData = data['data']['imageData']
    global players
    global number
    emit('number', {"number":number})
    number = number + 1
    players.append({"username": username, "room": room, "imageData": imageData, "number": number})
    join_room(room)
    emit('entered', {"players": list(filter(lambda d: d['room'] == room, players))}, room=room, broadcast=True)
    connected = True
array = []
clickDrag = []

@socketio.on('addClick', namespace='/test')
def addClick(message):
    global array
    global clickDrag
    array.append(message['data']['coordinates'])
    clickDrag.append(message['data']['clickDrag'])
    emit('serverResponseAddClick', {'data': {"array": array, "clickDrag": clickDrag}}, broadcast=True, room=message["data"]["room"])
    if len(array) > 1 and len(clickDrag) > 1:
        array = array[-2:]
        clickDrag = clickDrag[-2:]

@socketio.on('chat', namespace='/test')
def chat(info):
    emit('serverResponseChat', {"message":info['message']}, room=info['room'], broadcast=True)
    app.logger.info(info['room'])
    #app.logger.info('choice: '+choice)
    #app.logger.info('message: '+ info['message'])
    if choice is not None:
        if str(info['message']).strip() == str(choice).strip() and info['countAsGuess']:
            emit('guessed', {"username": info['username']}, broadcast=True, room=info['room'])
            emit('serverResponseChat', {"message": info['username']+" guessed the word!"}, broadcast=True, room=info['room'])

choice = ''
@socketio.on('choice', namespace='/test')
def choiceFunction(info):
    global choice
    choice = info['choice']


@app.route('/uploadajax', methods=['POST', 'GET'])
def uploadajax():
    #app.logger.info(request.files['file'].read())
    return 'returned'


if __name__ == '__main__':
    socketio.run(app, debug=True)
