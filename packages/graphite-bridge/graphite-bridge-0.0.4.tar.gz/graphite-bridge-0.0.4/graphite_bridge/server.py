import requests
import websocket

class GraphiteServerConnector:
    def __init__(self, server_url, email, password, strategy_id, on_message=None):
        self.__server_url = server_url
        self.__email = email
        self.__password = password
        self.__strategy_id = strategy_id
        self.__on_message = on_message

    def connect(self):
        self.__ws = websocket.WebSocketApp(self.__server_url + "/client_ws", on_message=self.on_message)
        self.__ws.run_forever()

    def disconnect(self):
        self.__ws.close()

    def on_message(self, ws, message):
        print(message)
        if self.__on_message != None:
            self.__on_message(message)

    def get_client_config(self):
        self.__ws.send('config')

    def upload_state(self, state):
        self.__ws.send('state ' + state)
