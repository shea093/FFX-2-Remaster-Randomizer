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
        self.__help_text = ""
        self.__name_start_index = 0
        self.__help_start_index = 0
        self.name_og_length = len(name_value)
        self.name_new_length = 0
        self.__help_og_length = 0
        self.help_new_length = 0
        self.__new_help_text = ""
        self.__new_name_text = ""
        self.unknown_text_variable = 0
        self.__mug_flag = False
        self.__repeat_flag = False
        self.repeated_jobs = []

        dmg_info_names = ["MP Cost","Target HP/MP","Calc PS","Crit","Hit","Power"]
        for name in dmg_info_names:
            self.__dmg_info[name] = 0

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def new_name_text(self):
        return self.__new_name_text

    @property
    def new_help_text(self):
        return self.__new_help_text

    @new_help_text.setter
    def new_help_text(self, value: str):
        self.__new_help_text = value
        self.help_new_length = len(value)

    @new_name_text.setter
    def new_name_text(self, value: str):
        self.__new_name_text = value
        self.name_new_length = len(value)

    @property
    def help_text(self):
        return self.__help_text

    @help_text.setter
    def help_text(self, value: str):
        self.__help_text = value
        self.__help_new_length = len(value)

    @property
    def help_og_length(self):
        return self.__help_og_length

    @help_og_length.setter
    def help_og_length(self, value: int):
        self.__help_og_length = value

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

    @name.setter
    def name(self, value: str):
        self.__name = value
        self.__name_new_length = len(value)

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
        if self.__type == "Mon-Magic":
            return f'<{self.__name}>'
        else:
            return f'<Ability ID = {self.__id}, Ability Name = {self.__name}, Type = {self.__type}>'

