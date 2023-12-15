from asyncio import run
from threading import Thread
import time
import websocket

class GraphiteServerConnector:
    def __init__(self, server_url, email, password, strategy_id, on_message=None):
        self.__server_url = server_url
        self.__email = email
        self.__password = password
        self.__strategy_id = strategy_id
        self.__connected = False
        if on_message is not None:
            self.__on_message = on_message

    def connect(self):
        def run(*args):
            self.__ws = websocket.WebSocketApp(self.__server_url + "/client_ws", on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
            self.__ws.run_forever()
        Thread(target=run).start()
        wait_count = 0
        while not self.__connected:
            wait_count += 1
            if wait_count > 10:
                return False
            time.sleep(1)
        return True

    def disconnect(self):
        self.__ws.close()

    def on_message(self, ws, message):
        print(message)
        if self.__on_message is not None:
            self.__on_message(message)
    
    def on_open(self, ws):
        self.__connected = True
    
    def on_close(self, ws):
        self.__connected = False

    def get_client_config(self):
        self.__ws.send('config')

    def upload_state(self, state):
        self.__ws.send('state ' + state)
