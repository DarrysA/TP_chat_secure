from ciphered_gui import *
from fernet_gui import *
from cryptography.fernet import Fernet, InvalidToken
import base64
import time


TTL = 30 #time to live en secondes


class TimeFernetGUI(FernetGUI):
    """
    GUI for a fernet chat secured client. Way way more secured.
    """

    # cette fonction sert à chiffrer les messages
    def encrypt(self, message):

        #chiffrement du message
        f = Fernet(self._key)
        temps = int(time.time())
        encrypted_message = f.encrypt_at_time(bytes(message, "utf-8"), temps)

        return(encrypted_message)


    def decrypt(self, encrypted_message):

        try:

            #conversion du message au format base64 :
            encrypted_message = base64.b64decode(encrypted_message['data'])        

            #déchiffrement du message
            f = Fernet(self._key)
            temps = int(time.time())

            message = f.decrypt_at_time(encrypted_message, TTL, temps)
        
        except InvalidToken as e:
            self._log.info("Erreur : token invalide")

        message = str(message, "utf-8")
        return(message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()
