import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')
    identify()


def identify():
    sio.emit('identify', {
        'name': 'Oak',
        'ip': '0.0.0.0'
    })


@sio.event
def sys_info(_):
    return {
        'cpu': '100%'
    }


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:8080')
sio.wait()
