import pygame
from WebSocket.WebSocketListener import WebSocketListener
from multiprocessing import Queue
from WebSocket.Window import Window
from project.Server import BroadcasterWebsocketServer
from project.analysis import Analysis


class MainApplication:

    def __init__(self):
        self.queue = Queue(maxsize=1)
        self.state = Queue(maxsize=1)
        self.listener = WebSocketListener(self.queue)
        self.listener.daemon = True
        self.server = BroadcasterWebsocketServer('', 8000, True)
        self.window = Window(self.queue)
        self.window.daemon = True
        self.a = Analysis(self.queue, self.server.serverMessage, self.server.getMessage)
        self.a.daemon = True

    def mainloop(self):
        self.listener.start()
        self.a.start()
        self.server.start()
        self.window.start()
        self.window.join()
        self.a.join()
        self.listener.join()


if __name__ == "__main__":
    application = MainApplication()
    application.mainloop()
