import os
import sys
import tornado.ioloop
import tornado.web
import webbrowser

from handlers.config_handler import ConfigHandler
from handlers.utility_handler import UtilityHandler
from handlers.main_handler import MainHandler

def create_web_server():
    handlers = [
        (r"/", MainHandler),
    ]
    settings = {
        "debug": True,
        "template_path": "templates",
        "static_path": "static"
    }

    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    # Le a porta a ser usada a partir da configuracao lida
    http_listen_port = sys.argv[1]
    # cria web server
    web_app = create_web_server()
    ioloop = tornado.ioloop.IOLoop.instance()
    UtilityHandler.init()
    print("Servidor iniciado. Abrindo http://localhost:" + http_listen_port)
    # abre pagina web
    webbrowser.open('http://localhost:' + http_listen_port, new = 2)
    # liga led de debug no arduiono
    # UtilityHandler.write('6')
    web_app.listen(http_listen_port)
    ioloop.start()
