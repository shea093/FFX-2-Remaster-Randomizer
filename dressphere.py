class Dressphere:
    def __init__(self, dress_name_def: str, dress_id_def: int):
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "ACC", "EVA", "LUCK"]
        self.__dress_name = dress_name_def
        self.__dress_id = dress_id_def
        self.__stat_variables = {}
        self.__ability_table = {}
        self.__hex_chunk = ""
        for stat_name in stat_names:
            self.__stats[stat_name] = 0

    @property
    def stat_variables(self):
        return self.__stat_variables

    @stat_variables.setter
    def stats(self, value: dict):
        self.__stat_variables = value

    @property
    def hex_chunk(self):
        return self.__hex_chunk

    @hex_chunk.setter
    def hex_chunk(self, value: str):
        self.__hex_chunk = value