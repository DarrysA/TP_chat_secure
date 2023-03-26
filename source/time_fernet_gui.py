from ciphered_gui import *
from fernet_gui import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
import base64
import hashlib
import os


TAILLE_CLEF_BLOC = 32 #taille de la clé en octets
SEL = b"Gloire au Saint-Transistor" # création d'un sel fixe
NB_ITERATIONS = 480000


class TimeFernetGUI(FernetGUI):
    """
    GUI for a fernet chat secured client. Way way more secured.
    """
    
    def encrypt_at_time(self, message):
        
        return 

    def decrypt_at_time(self, message):

        return

    # cette fonction sert à chiffrer les messages
    def encrypt(self, message):
        self._log.info("Début de chiffrement du message...")
        
        #chiffrement du message
        self._log.info("Chiffrement du message...")
        f = Fernet(self._key)
        encrypted_message = f.encrypt(bytes(message, "utf-8"))
        self._log.info("Message chiffré !")

        self._log.info(f"[temporaire] Affichage du message chiffré : {encrypted_message}")

        return(encrypted_message)


    def decrypt(self, encrypted_message):
        self._log.info("Déchiffrement du message...")

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
