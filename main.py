import psutil
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
    cores = psutil.cpu_count()
    load_avg = [f"{x / psutil.cpu_count() * 100}%" for x in
                psutil.getloadavg()]
    memory = psutil.virtual_memory()
    return {
        'cpu': f'{psutil.cpu_percent()}%',
        'load_average': load_avg,
        'cores': cores,
        'memory': memory.total,
        'memory_used': memory.used
    }


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:8080')
sio.wait()
