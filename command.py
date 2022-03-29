class Command:
    def __init__(self, id_value: str, name_value: str, type_value: str):
        self.__id = id_value
        self.__name = name_value
        self.__type = type_value
        self.__ap = 0

    @property
    def id(self):
        return self.__id

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

    def __repr__(self):
        return f'<Ability ID = {self.__id}, Ability Name = {self.__name}, Type = {self.__type}>'

