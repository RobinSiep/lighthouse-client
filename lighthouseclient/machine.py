from subprocess import Popen, PIPE

from lighthouseclient import sio


@sio.event
def shutdown():
    p = Popen(('shutdown', '-h', 'now'), stdout=PIPE, stderr=PIPE)
    _, error = p.communicate()
    if p.returncode != 0:
        error = error.decode('utf-8')
        if "NOT super-user" in error:
            error = "Insufficient permissions to perform shutdown"

        return False, error
    else:
        return True, None
