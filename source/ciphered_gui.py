import logging

import dearpygui.dearpygui as dpg
import cryptography

from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import BasicGUI

# default values used to populate connection window
DEFAULT_VALUES = {
    "host" : "127.0.0.1",
    "port" : "6666",
    "name" : "foo"
}

class CipheredGUI:
    """
    GUI for a chat secured client. Way more secured.
    """
    def __init__(self)->None:
        # constructor
        self._client = None
        self._callback = None
        self._log = logging.getLogger(self.__class__.__name__)


    # surcharge pour inclure le champ de la clef de chiffrement
    def _key(self)->None:
        return 0

    # surcharge de la fonction _create_connection_window() pour y inclure un champ password
    def _create_connection_window():

        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
        
        with dpg.window(label = "Password", pos = (400, 150), width=400, height = 300, show = False, tag = "connection_windows"):
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal = True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()