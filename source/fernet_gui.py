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
        self._log.info("Chat running...")
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
        #self._key.digest()

        self._log.info(f"Affichage de la clé : {self._key}")

        # on convertit la clé en base 64
        self._key = base64.b64encode(self._key.digest())

        self._log.info(f"Affichage de la clé en base64 : {self._key}")

        f = Fernet(self._key)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")


    # cette fonction sert à chiffrer les messages
    def encrypt(self, message):
        self._log.info("Début de chiffrement du message...")
        iv = os.urandom(16)
        
        # comme le chiffrement se fait par bloc, il faut ajouter un padding 
        # il s'agit d'un remplissage afin que la taille du bloc soit un multiple de la longueur du bloc     
        self._log.info("Création du padding")
        padder = padding.PKCS7(TAILLE_CLEF_BLOC).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        
        #chiffrement du message
        self._log.info("Chiffrement du message")
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend = default_backend())
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
        
        return(iv, encrypted_message)


    def decrypt(self, data):
        self._log.info("Déchiffrement du message...")

        #conversion du vecteur d'initialisation et du message :
        iv = base64.b64decode(data[0]["data"])
        encrypted_message = base64.b64decode(data[1]["data"])        

        #déchiffrement du message
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend = default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

        #unpadding du message
        unpadder = padding.PKCS7(TAILLE_CLEF_BLOC).unpadder()
        unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
        message = str(unpadded_message, "utf-8")

        return(message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()
