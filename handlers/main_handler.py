import tornado.web
from tornado import gen

from .adsb_handler import ADSBHandler
from .utility_handler import UtilityHandler

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("../static/index.html")
        return

    @gen.coroutine
    def post(self):
        tipo = self.get_argument('type')

        # informacoes sobre a posicao do dispositivo
        if tipo == 'meta':
            ADSBHandler.latitude = self.get_argument('latitude')
            ADSBHandler.longitude = self.get_argument('longitude')
            self.set_status(200)
            return

        args = {
            'altitude': self.get_argument("altitude"),
            'latitude': self.get_argument("latitude"),
            'longitude': self.get_argument("longitude"),
            'airplane_id': self.get_argument('airplane_id')
        }

        print("Received data! Encoding information...")
        encoded_msg = ADSBHandler.encode(args)
        print(encoded_msg)

        print("Decoding message...")
        decoded_msg = ADSBHandler.decode(encoded_msg)
        print(args)

        print("Calculating distance...")
        distance = ADSBHandler.distance(args)
        print("Distance is " + str(distance) + " meters from device.")

        print("Sending distance to Arduino...")
        UtilityHandler.write(str(int(distance)) + "\n")
        print("Sent!")

        return
