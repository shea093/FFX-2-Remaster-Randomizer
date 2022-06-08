import os
import sys
import pathlib

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        test = ""

    return os.path.join(base_path, relative_path)

item_txt_path = resource_path(pathlib.PureWindowsPath("Test Files/items.txt"))
acc_txt_path = resource_path(pathlib.PureWindowsPath("Test Files/accessories.txt"))


class Item:
    def __init__(self, id_value: str, name_value: str, type_value: str):
        self.__id = id_value
        self.__name = name_value
        self.__type = type_value
        self.__og_hex_chunk = ""
        self.__curr_hex_chunk = ""

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def og_hex_chunk(self):
        return self.__og_hex_chunk

    @og_hex_chunk.setter
    def og_hex_chunk(self, value: str):
        self.__og_hex_chunk = value

    @property
    def curr_hex_chunk(self):
        return self.__curr_hex_chunk

    @curr_hex_chunk.setter
    def curr_hex_chunk(self, value: str):
        self.__curr_hex_chunk = value

    def __repr__(self):
        return f'<Item ID = {self.__id}, Item Name = {self.__name}>'

def initialize_items():
    items = []
    with open(item_txt_path,"r") as f:
        id_hex_count = 8192
        for n, line in enumerate(f.readlines()):
            id_hex = hex(id_hex_count)
            new_item = Item(id_value=id_hex[2:],name_value=line.replace('\n',""),type_value="Item")
            items.append(new_item)
            id_hex_count = id_hex_count + 1
    with open(acc_txt_path,"r") as f:
        for n, line in enumerate(f.readlines()):
            id_cut = line[0:4]
            name_cut = line[5:]
            new_item = Item(id_value=id_cut,name_value=name_cut.replace('\n',""),type_value="Accessory")
            items.append(new_item)
    return items


