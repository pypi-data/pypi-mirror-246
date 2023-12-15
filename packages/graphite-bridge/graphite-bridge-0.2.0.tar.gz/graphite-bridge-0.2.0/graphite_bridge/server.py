from asyncio import run
from threading import Thread
import time
import requests
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
            websocket_url = self.__server_url.replace("http", "ws") + "/client_ws"
            self.__ws = websocket.WebSocketApp(websocket_url, on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
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
        response = requests.get(self.__server_url + "/api/client/config?strategyId=" + self.__strategy_id)
        if response.status_code != 200:
            return (False, response.reason)
        response_json = response.json()
        return (response_json['success'], response_json['data'])

    def upload_state(self, state):
        data = { 'strategyId': self.__strategy_id, 'state': state }
        response = requests.post(self.__server_url + "/api/client/upload", json=data)
        if response.status_code != 200:
            return (False, response.reason)
        response_json = response.json()
        return (response_json['success'], response_json['data'])
