from ciphered_gui import *
from fernet_gui import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
import base64
import hashlib
import os
import time


TTL = 30 #time to live en secondes


class TimeFernetGUI(FernetGUI):
    """
    GUI for a fernet chat secured client. Way way more secured.
    """

    # cette fonction sert à chiffrer les messages
    def encrypt(self, message):

        #chiffrement du message
        self._log.info("Chiffrement du message...")
        f = Fernet(self._key)
        temps = int(time.time()) - 45
        encrypted_message = f.encrypt_at_time(bytes(message, "utf-8"), temps)
        self._log.info("Message chiffré !")
        self._log.info(f"[temporaire] Affichage du message chiffré : {encrypted_message}")

        return(encrypted_message)


    def decrypt(self, encrypted_message):
        self._log.info("Déchiffrement du message...")

        #conversion du vecteur d'initialisation et du message :
        encrypted_message = base64.b64decode(encrypted_message['data'])        

        time.sleep(45)

        #déchiffrement du message
        f = Fernet(self._key)
        temps = int(time.time())
        message = f.decrypt_at_time(encrypted_message, TTL, temps)
        message = str(message, "utf-8")
        return(message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()
