class Command:
    def __init__(self, id_value: str, name_value: str, type_value: str):
        self.__id = id_value
        self.__name = name_value
        self.__type = type_value
        self.__og_hex_chunk = ""
        self.__curr_hex_chunk = ""
        self.__ap = 0
        self.__job = ""
        self.__mug_flag = False
        self.__repeat_flag = False

    @property
    def id(self):
        return self.__id

    @property
    def repeat_flag(self):
        return self.__repeat_flag

    @repeat_flag.setter
    def repeat_flag(self, value: bool):
        self.__repeat_flag = value

    @property
    def og_hex_chunk(self):
        return self.__og_hex_chunk

    @og_hex_chunk.setter
    def og_hex_chunk(self, value: str):
        self.__og_hex_chunk = value

    @property
    def mug_flag(self):
        return self.__mug_flag

    @mug_flag.setter
    def mug_flag(self, value: bool):
        self.__mug_flag = value

    @property
    def curr_hex_chunk(self):
        return self.__curr_hex_chunk

    @curr_hex_chunk.setter
    def curr_hex_chunk(self, value: str):
        self.__curr_hex_chunk = value

    @property
    def job(self):
        return self.__job

    @job.setter
    def job(self, value: str):
        self.__job = value

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    def search_by_id(self, id_value: str):
        if id_value == str(self.__id):
            return self.__name
        else:
            return "Not found."

    def search_by_name(self, name_value = int):
        if name_value == str(self.__name):
            return self.__id
        else:
            return "Not found."

    def __repr__(self):
        return f'<Ability ID = {self.__id}, Ability Name = {self.__name}, Type = {self.__type}>'

