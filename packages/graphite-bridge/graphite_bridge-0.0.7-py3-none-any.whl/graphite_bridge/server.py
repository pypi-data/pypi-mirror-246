import websocket

class GraphiteServerConnector:
    def __init__(self, server_url, email, password, strategy_id):
        self.__server_url = server_url
        self.__email = email
        self.__password = password
        self.__strategy_id = strategy_id

    def connect(self):
        self.__ws = websocket.WebSocket()
        self.__ws.connect(self.__server_url + "/client_ws")
        return True

    def disconnect(self):
        self.__ws.close()

    def get_client_config(self):
        self.__ws.send('config')

    def upload_state(self, state):
        self.__ws.send('state ' + state)
