from tabulate import tabulate

class Dressphere:
    def __init__(self, dress_name_def: str, dress_id_def: int):
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        self.__dress_name = dress_name_def
        self.__dress_id = dress_id_def
        self.__stat_variables = {}
        self.__ability_table = {}
        self.__hex_chunk = ""
        for stat_name in stat_names:
            self.__stat_variables[stat_name] = 0

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

    @property
    def dress_name(self):
        return self.__dress_name

    def separate_stat_string(self, hex: str):
        variables = {}
        variable_names = ["A","B","C","D","E"]
        count = 0
        for index, variable in enumerate(variable_names):
            count = count + 2
            variables[variable] = int(hex[count-2:count],16)
        return variables


    def stat_formula(self, type: str):
        table = []
        temp_list = []
        count = 0
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        for level in range(1, 100):
            if level == 99:
                table.append(temp_list)
            if type in stat_names:
                variables = self.separate_stat_string(self.stat_variables[type])
                a_frac = variables["A"] / 10
                part1 = level * a_frac
                part2 = (level / variables["B"]) + variables["C"]
                part3 = level ** 2
                formula_result = part1 + part2 - part3 / 16 / variables["D"] / variables["E"]
                formula_result = "{:.2f}".format(formula_result)
                formula_output = str(level) + ". " + str(formula_result)
                if count == 4:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
        print("**************************")
        print(type)
        print("**************************")
        print(tabulate(table))


    def __repr__(self):
        return f'<Dressphere ID = {self.__dress_id}, Dressphere Name = {self.__dress_name}>'