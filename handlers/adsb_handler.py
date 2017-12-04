from haversine import haversine
import struct
import math

class ADSBHandler:

    latitude = None
    longitude = None

    # +--------+--------+-----------+--------------------------+---------+
    # |  DF 5  |  ** 3  |  ICAO 24  |          DATA 56         |  PI 24  |
    # +-----------------+-----------+--------------------------+---------+

    def encode(message):
        value = 17 << 80
        msg = value
        msg = value
        value = int(float(message['latitude'][:5]) * 1000) << 40
        msg = value
        value = int(float(message['longitude'][:5]) * 100 ) << 0
        return ''.join(str(ord(c)) for c in str(message))

    def decode(stream):
        return stream

    def distance(message):
        device = (float(ADSBHandler.latitude), float(ADSBHandler.longitude))
        airplane = (float(message['latitude']), float(message['longitude']))
        projected_distance = haversine(device, airplane)

        return math.sqrt(projected_distance ** 2 + (float(message['altitude'])/1000) ** 2) * 1000

    def floatToRawLongBits(value):
    	return struct.unpack('Q', struct.pack('d', value))[0]

    def longBitsToFloat(bits):
    	return struct.unpack('d', struct.pack('Q', bits))[0]
