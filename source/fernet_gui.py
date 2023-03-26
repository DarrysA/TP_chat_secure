from ciphered_gui import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
import base64
import hashlib
import os


TAILLE_CLEF_BLOC = 32 #taille de la clé en octets
SEL = b"Gloire au Saint-Transistor" # création d'un sel fixe
NB_ITERATIONS = 480000


class FernetGUI(CipheredGUI):
    """
    GUI for a fernet chat secured client. Way way more secured.
    """
    def __init__(self)->None:
        # constructor
        self._client = None
        self._callback = None
        self._log = logging.getLogger(self.__class__.__name__)
        # ajout du champ pour la clé de chiffrement
        self._key = None


    def run_chat(self, sender, app_data)->None:

        # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")

        # on récupère le mot de passe
        password = dpg.get_value("connection_password")

        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # génération de la clé à l'aide de SHA256 à partir du mot de passe
        self._key = hashlib.sha256()
        self._key.update(password.encode("utf-8"))

        # on convertit la clé en base 64
        self._key = base64.b64encode(self._key.digest())

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")


    # cette fonction sert à chiffrer les messages
    def encrypt(self, message):
        
        #chiffrement du message
        f = Fernet(self._key)
        encrypted_message = f.encrypt(bytes(message, "utf-8"))

        return(encrypted_message)


    def decrypt(self, encrypted_message):

        #conversion du vecteur d'initialisation et du message :
        #iv = base64.b64decode(data[0]["data"])
        encrypted_message = base64.b64decode(encrypted_message['data'])        

        #déchiffrement du message
        f = Fernet(self._key)
        message = f.decrypt(encrypted_message)
        message = str(message, "utf-8")
        return(message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()
