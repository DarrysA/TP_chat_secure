from ciphered_gui import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib
import os


ITERATION = 480000
TAILLE_CLE = 32 # taille de la clé en octets
SEL = b"Gloire au Saint-Transistor"


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
        
        # fonction de débuggage
        self._log.info(f"password = {password}")

        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # on définit les paramètres de la fonction qui permettra de dériver la clé
        kdf = hmac.HMAC(algorithm=hashes.SHA256, length = TAILLE_CLE, salt = SEL, iterations = ITERATION)

        #on convertit le mot de passe du format string au format bytes
        b_password = bytes(password, "utf8")

        # génération de la clé
        self._key = Fernet.generate_key()
        f = Fernet(self._key)

        # fonction de débuggage
        self._log.info(f"La clé dérivée est la suivante : {self._key}")
        
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message):
        self._log.info("Chiffrement du message...")
        iv = os.urandom(16)
        self._log.info(f"Affichage du vecteur d'initialisation : {iv}")
        
        self._log.info(f"La clé utilisée pour le chiffrement est la suivante : {self._key}")
        
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend = default_backend())


        #comme le chiffrement se fait par bloc, il faut ajouter un padding, un remplissage afin que la taille du bloc soit un multiple de la longueur du bloc     
        padder = padding.PKCS7(128).padder()

        self._log.info(f"Message avant chiffrement et padding : {message}")

        padded_data = padder.update(message.encode()) + padder.finalize()
        
        self._log.info(f"Données + padding : {padded_data}")

        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
        
        self._log.info(f"Message chiffré : {encrypted_message}")

        return(iv, encrypted_message)
    
    def decrypt(self, data):
        self._log.info("Déchiffrement du message")
        iv, encrypted_message = data
        
        self._log.info(f"Affichage du vecteur d'initialisation : {data[0]}")
        self._log.info(f"Affichage du message à déchiffrer : {data[1]}")

        self._log.info(f"ameno 1") 

        #conversion du vecteur d'initialisation et du message :
        iv = base64.b64decode(data[0]['data'])

        self._log.info(f"ameno 2")

        encrypted_message = base64.b64decode(data[1]['data'])

        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend = default_backend())
        self._log.info(f"hic sunt dracones 1")
        decryptor = cipher.decryptor()
        self._log.info(f"hic sunt dracones 2")
        message = decryptor.update(encrypted_message) + decryptor.finalize()
        self._log.info(f"hic sunt dracones 3")
        message = str(message, "utf-8")
        self._log.info(f"hic sunt dracones 4")
        return(message)
        self._log.info("Message déchiffré")


    
