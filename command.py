class Command:
    def __init__(self, id_value: str, name_value: str, type_value: str):
        self.__id = id_value
        self.__name = name_value
        self.__type = type_value
        self.__og_hex_chunk = ""
        self.__curr_hex_chunk = ""
        self.__ap = 0
        self.__dmg_info = {}
        self.__job = ""
        self.__name_start_index = 0
        self.__help_start_index = 0
        self.__name_og_length = len(name_value)
        self.__help_og_length = 0
        self.unknown_text_variable = 0
        self.__mug_flag = False
        self.__repeat_flag = False

        dmg_info_names = ["MP Cost","Target HP/MP","Calc PS","Crit","Hit","Power"]
        for name in dmg_info_names:
            self.__dmg_info[name] = 0

    @property
    def id(self):
        return self.__id

    @property
    def name_start_index(self):
        return self.__name_start_index

    @name_start_index.setter
    def name_start_index (self, value: int):
        self.__name_start_index = value

    @property
    def help_start_index(self):
        return self.__help_start_index

    @help_start_index.setter
    def help_start_index(self, value: int):
        self.__help_start_index = value

    @property
    def repeat_flag(self):
        return self.__repeat_flag

    @repeat_flag.setter
    def repeat_flag(self, value: bool):
        self.__repeat_flag = value

    @property
    def dmg_info(self):
        return self.__dmg_info

    @dmg_info.setter
    def dmg_info(self, value: dict):
        self.__dmg_info = value

    @property
    def ap(self):
        return self.__ap

    @ap.setter
    def ap(self, value: int):
        self.__ap = value

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

