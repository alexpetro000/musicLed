from __future__ import print_function

import time
from threading import Thread

import requests
import socketio

apiKey = '583bedfd70c2bdf87082bc5e482870a7'
module = 'dirty-leds'

# need something to pick if to use bridge or not here???


actionHandlers = {}
sio = socketio.Client(reconnection=True, reconnection_delay=5)


class ViotSocket:
    wsUrl = ''

    def __init__(self, url):
        self.wsUrl = url

        sio.connect(url)

    @sio.on('connect')
    def on_connect():
        print('viot: Socket established')

    @sio.on('action')
    def on_action(data):
        print('viot: action')
        if not ('request' in data and 'action' in data and 'data' in data):
            print('viot: Received invalid request ID')
            return

        if data['action'] in actionHandlers:
            res = actionHandlers[data['action']](data['data'])
            if isinstance(res, str):
                sio.emit('response', {'request': data['request'], 'status': 'failure', 'message': res})

                return
            sio.emit('response', {'request': data['request'], 'status': 'ok', 'data': res})
        else:
            sio.emit('response',
                     {'request': data['request'], 'status': 'failure', 'message': 'Action handler not found'})

    @sio.on('device-connected')
    def on_device_connected(data):
        if not ('request' in data):
            print('viot: Device connection requested but no device data')
            sio.emit('response', {'request': data['request'], 'status': 'failure', 'message': 'invalid.request'})
            return

        sio.emit('response', {'request': data['request'], 'status': 'ok', 'data': '{}'})

    @sio.on('disconnect')
    def on_disconnect():
        print('viot: Socket disconnected')
        auth = Viot.instance.auth()
        url = auth['socket'] + "?uniq=" + Viot.instance.uniq + "&authkey=" + auth['authkey']
        sio.connection_url = url


def get_auth(apiKey, module, uniq):
    auth_url = 'https://viot.uk/api/bridge/auth?apikey={apikey}&uniq={uniq}&module={module}'.format(apikey=apiKey,
                                                                                                   uniq=uniq,
                                                                                                   module=module)
    try:
        r = requests.get(auth_url)

        if not r:
            print('viot: Could not establish connection with server. Retrying in 5s...')
            return False

        resp = r.json()
        if not resp:
            print('viot: Invalid response from server. Retrying in 5s...')
            return False
        return resp
    except:
        return False


class Viot:
    instance = None

    def __init__(self, uniq):
        print('we are here')
        if not Viot.instance:
            Viot.instance = Viot.__viot(uniq)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __viot:

        uniq = ''
        connected = False

        def __init__(self, uniq):
            self.uniq = uniq
            print('viot: Attempting initial connection to https://viot.uk')

            resp = self.auth()
            if resp:
                self.begin_socket(resp['socket'], resp['authkey'])

        def begin_socket(self, url, authKey):
            socket_thread = Thread(target=ViotSocket, args=[url + "?uniq=" + self.uniq + "&authkey=" + authKey])
            socket_thread.daemon = True
            socket_thread.start()

        def action(self, actionName):
            def wrapper(func):
                actionHandlers[actionName] = func

            return wrapper

        def auth(self):
            self.connected = False
            attempts = 0
            return False
            while not self.connected:
                resp = get_auth(apiKey, module, self.uniq)
                if not resp:
                    time.sleep(2)
                    attempts += 1
                    if attempts >= 1:
                        print('not connected')
                        return False
                    continue

                self.connected = True
                if resp['status'] == 'ok':
                    print('viot: Authorized successfully')
                    return {'socket': resp['data']['socket'], 'authkey': resp['data']['authkey']}
                else:
                    print("viot: " + resp['message'])
                    exit()
                return
