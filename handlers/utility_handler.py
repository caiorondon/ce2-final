import sys
import time
from serial import Serial
from serial.tools import list_ports

from .config_handler import ConfigHandler

class UtilityHandler:

    arduino = None

    def write(message):
        UtilityHandler.arduino.write(message.encode())

    def init():
        print("""
        > Simulador ADS-B
        >> Autor: Caio Rondon Botelho de Carvalho
        >> Versao: 1.0v
        """)

        #
        # LISTA DIPOSITIVOS
        #

        # capturando dispositivos
        devices = list(list_ports.comports())
        # termina programa se nao encontra dispositivo para comunicacao
        if not devices:
            print("Nenhum dispositivo encontrado! Favor verificar.")
            sys.exit(0)

        print("Listando dispositivos conectados:\n[Numero] - 'Descricao'")
        for i, device in enumerate(devices):
            print ("["+ str(i) + "] - '" + str(device) + "'")

        #
        # ESCOLHER DISPOSITIVOS
        #
        opc = input("\nEscolha o numero que representa o Arduino. Qualquer letra para sair.\n> ")

        try:
            d = int(opc)
            # captura dispositivo escolhido
            arduino_info = devices[d]
            UtilityHandler.arduino = Serial(arduino_info.device, ConfigHandler.baudrate)
            time.sleep(2) # tempo para conexao ser estabelecida
            print("Conectado!")
        except ValueError:
            sys.exit(0)
        except Exception as e:
            print(str(e))
            print("Nao foi possivel se conectar ao dispositivo selecionado")
            sys.exit(1)

        return
