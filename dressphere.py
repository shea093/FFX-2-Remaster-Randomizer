from tabulate import tabulate

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Dressphere:
    def __init__(self, dress_name_def: str, dress_id_def: int):
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        self.__dress_name = dress_name_def
        self.__dress_id = dress_id_def
        self.__stat_variables = {}
        self.__stat_hex_og = ""
        self.__ability_table = {}
        self.__hex_chunk = "" #Legacy
        self.__big_chunk = ""
        self.__abilities = []
        self.__ability_hex = ""
        self.__ability_hex_og = ""
        for stat_name in stat_names:
            self.__stat_variables[stat_name] = 0

    @property
    def stat_variables(self):
        return self.__stat_variables

    @stat_variables.setter
    def stat_variables(self, value: dict):
        self.__stat_variables = value

    @property
    def big_chunk(self):
        return self.__big_chunk

    @big_chunk.setter
    def big_chunk(self, value: str):
        self.__big_chunk = value

    @property
    def ability_hex_og(self):
        return self.__ability_hex_og

    @ability_hex_og.setter
    def ability_hex_og(self, value: str):
        self.__ability_hex_og = value

    @property
    def stat_hex_og(self):
        return self.__stat_hex_og

    @stat_hex_og.setter
    def stat_hex_og(self, value: str):
        self.__stat_hex_og = value


    @property
    def hex_chunk(self):
        return self.__hex_chunk

    @hex_chunk.setter
    def hex_chunk(self, value: str):
        self.__hex_chunk = value

    @property
    def dress_name(self):
        return self.__dress_name

    @property
    def abilities(self):
        return self.__abilities

    @abilities.setter
    def abilities(self, value: list):
        self.__abilities = value
        abilityhex = ""
        for ability in self.abilities:
            abilityhex = abilityhex + ability[0]
            abilityhex = abilityhex + ability[1]
        self.__ability_hex = abilityhex

    def separate_stat_string(self, hex: str, hpmp=False, target="Stats"):
        if target == "Stats":
            variables = {}
            if hpmp == True:
                variable_names = ["A","B","C"]
                count = 0
                for index, variable in enumerate(variable_names):
                    count = count + 2
                    variables[variable] = int(hex[count-2:count],16)
            else:
                variable_names = ["A","B","C","D","E"]
                count = 0
                for index, variable in enumerate(variable_names):
                    count = count + 2
                    variables[variable] = int(hex[count-2:count],16)
            return variables
        elif target == "Abilities":
            pass
        else:
            return



    def stat_formula(self, type: str, tableprint=False):
        table = []
        temp_list = []
        raw_objects = []
        columns = 7
        count = 0
        stat_names = ["STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        for level in range(1, 100):
            if level == 99:
                table.append(temp_list)
            if type == "HP":
                variables = self.separate_stat_string(self.__stat_variables[type],hpmp=True)
                part1 = (level * variables["A"])+variables["C"]
                part2 = (level**2) / (variables["B"]/10)
                formula_result = part1 - part2
                formula_result = "{:.2f}".format(formula_result)
                raw_objects.append(formula_result)
                formula_output = color.BOLD + color.CYAN + str(level) + color.END + ". " + str(formula_result)
                if count == columns:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
            if type == "MP":
                variables = self.separate_stat_string(self.__stat_variables[type],hpmp=True)
                part1 = (level * (variables["A"]/10))+variables["C"]
                part2 = (level**2) / (variables["B"])
                formula_result = part1 - part2
                formula_result = "{:.2f}".format(formula_result)
                raw_objects.append(formula_result)
                formula_output = color.BOLD + color.CYAN + str(level) + color.END + ". " + str(formula_result)
                if count == columns:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
            if type in stat_names:
                variables = self.separate_stat_string(self.__stat_variables[type])
                a_frac = variables["A"] / 10
                part1 = level * a_frac
                part2 = (level / variables["B"]) + variables["C"]
                part3 = level ** 2
                formula_result = part1 + part2 - part3 / 16 / variables["D"] / variables["E"]
                formula_result = "{:.2f}".format(formula_result)
                raw_objects.append(formula_result)
                formula_output = color.BOLD + color.CYAN + str(level)+ color.END + ". " + str(formula_result)
                if count == columns:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
        if tableprint == True:
            print("**************************")
            print(type + " growth for " + self.__dress_name)
            print("**************************")
            print(tabulate(table,tablefmt="fancy_grid"))
        else:
            return raw_objects

    def return_as_list(self):
        return [self.__dress_id,self.__dress_name]

    @property
    def ability_hex(self):
        abilityhex = ""
        for ability in self.abilities:
            abilityhex = abilityhex + ability[0]
            abilityhex = abilityhex + ability[1]
        self.__ability_hex = abilityhex
        return self.__ability_hex

    @property
    def stat_hex(self):
        stathex = ""
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        for stat in stat_names:
            stathex = stathex + self.stat_variables[stat]
        self.__stat_hex = stathex
        return self.__stat_hex

    def change_ability(self, ability_index: int, ability: str):
        hex_byte_reverse = ability[2:4] + ability[0:2]
        hex_byte_reverse = hex_byte_reverse.lower()
        new_ability = (self.abilities[ability_index][0],hex_byte_reverse)
        self.abilities[ability_index] = new_ability
        abilityhex = ""
        for ability in self.abilities:
            abilityhex = abilityhex + ability[0]
            abilityhex = abilityhex + ability[1]
        self.__ability_hex = abilityhex

    def change_required_ability(self, ability_index: int, ability: str):
        hex_byte_reverse = ability[2:4] + ability[0:2]
        hex_byte_reverse = hex_byte_reverse.lower()
        new_required_ability = (hex_byte_reverse,self.abilities[ability_index][1])
        self.abilities[ability_index] = new_required_ability
        abilityhex = ""
        for ability in self.abilities:
            abilityhex = abilityhex + ability[0]
            abilityhex = abilityhex + ability[1]
        self.__ability_hex = abilityhex

    # def return_ability_hex(self):
    #     abilityhex = ""
    #     for ability in self.abilities:
    #         abilityhex = abilityhex + ability[0]
    #         abilityhex = abilityhex + ability[1]
    #     return abilityhex


    def __repr__(self):
        return f'<Dressphere ID = {self.__dress_id}, Dressphere Name = {self.__dress_name}>'