from Server.app import server


def start(e, receiveTasks, sendLofts):
    server.run(host='0.0.0.0', debug=True, threaded=False)
