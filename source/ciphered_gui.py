import logging

import dearpygui.dearpygui as dpg
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from chat_client import *
from generic_callback import GenericCallback
from basic_gui import *

# default values used to populate connection window
DEFAULT_VALUES = {
    "host" : "127.0.0.1",
    "port" : "6666",
    "name" : "foo"
}

class CipheredGUI(BasicGUI):
    """
    GUI for a chat secured client. Way more secured.
    """
    def __init__(self)->None:
        # constructor
        self._client = None
        self._callback = None
        self._log = logging.getLogger(self.__class__.__name__)
        # ajout du champ pour la clé de chiffrement
        self._key = None
        #on ajoute cette donnée membre qui est nécessaire pour la fonction envoi
        

    def _create_chat_window(self)->None:
        # chat windows
        # known bug : the add_input_text do not display message in a user friendly way
        with dpg.window(label="Chat", pos=(0, 0), width=800, height=600, show=False, tag="chat_windows", on_close=self.on_close):
            dpg.add_input_text(default_value="Readonly\n\n\n\n\n\n\n\nfff", multiline=True, readonly=True, tag="screen", width=790, height=525)
            dpg.add_input_text(default_value="some text", tag="input", on_enter=True, callback=self.text_callback, width=790)

    
    # surcharge de la fonction _create_connection_window() pour y inclure un champ password
    def _create_connection_window(self)->None:

        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
                    
            #ajout d'un champ pour le mot de passe
            dpg.add_text("password")
            dpg.add_input_text(password = True, id = "connection_password")
            dpg.add_button(label="Connect", callback=self.run_chat)


    def run_chat(self, sender, app_data)->None:
        # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")

        # on récupère le mot de passe
        password = dpg.get_value("connection_password")
        
        # fonction de débuggage
        print(f"password = {password}")
        
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # on définit les paramètres de la fonction qui permettra de dériver la clé
        salt = b"Gloire au Saint-Transistor" #on définit un sel constant
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256, length = 256, salt = salt, iterations = 48000)

        #on convertit le mot de passe du format string au format bytes
        b_password = bytes(password, "UTF-8")

        # on dérive ensuite le mot de passe :
        self._key = kdf.derive(b_password)
        
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    # cette fonction sert à chiffrer les messages
    def encrypt(message, self)->None:
        print("Chiffrement du message...")
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(bytes(message, "UTF-8")) + encryptor.finalize()
        return(iv, encrypted_message)
        print("Message chiffré")

    def decrypt(data, self)->None:
        iv, encrypted_message = data
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        message = decryptor.update(encrypted_message) + decryptor.finalize()
        message = str(message, encoding = "utf-8", errors = "strict")
        return(message)

    def send_message(self, message:str)->None:
        print("envoi du message")
        with Proxy(self._uri) as server:
            encrypted_message = self.encrypt(message)
            server.send_message(self._name, encrypted_message)

            print(f"Message chiffré : {encrypted_message}")
    
    def recv(self, data)->None:
        # function called to get incoming messages and display them
        if self._callback is not None:
            for user, message in self._callback.get():
                self.update_text_screen(f"{user} : {self.decrypt(data, self)}")
            self._callback.clear()

    def send(self, text)->None:
        # function called to send a message to all (broadcasting)
        self._client.send_message(text)

    def loop(self, data):
        # main loop
        while dpg.is_dearpygui_running():
            self.recv(data)
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()