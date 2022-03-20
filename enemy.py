from pathlib import Path
import re

class Enemy:
    def __init__(self, enemy_name_def: str, enemy_id: int, enemy_hex_data_def: str, starting_position=0):
        stat_names = ["HP", "MP", "LV", "STR", "DEF", "MAG", "MDEF", "AGL", "ACC", "EVA", "LUCK"]
        self.__enemy_name = enemy_name_def
        self.__enemy_id = enemy_id
        self.__enemy_hex_data = enemy_hex_data_def
        self.__stat_bank = {}
        self.__oversoul_stat_bank = {}
        self.__starting_position = starting_position
        for stat_name in stat_names:
            self.__stat_bank[stat_name] = 0
            self.__oversoul_stat_bank[stat_name] = 0

    @property
    def enemy_name(self):
        return self.__enemy_name

    @property
    def enemy_id(self):
        return self.__enemy_id

    @property
    def enemy_hex_data(self):
        return self.__enemy_hex_data

    @property
    def stat_bank(self):
        return self.__stat_bank

    @property
    def oversoul_stat_bank(self):
        return self.__oversoul_stat_bank

    @property
    def starting_position(self):
        return self.__starting_position

    @enemy_name.setter
    def enemy_name(self, value: str):
        self.__enemy_name = value

    @enemy_id.setter
    def enemy_id(self, value: int):
        self.__enemy_name = value

    @enemy_hex_data.setter
    def enemy_hex_data(self, value: str):
        self.__enemy_name = value

    @stat_bank.setter
    def stat_bank(self, value: dict):
        self.__stat_bank = value

    @oversoul_stat_bank.setter
    def oversoul_stat_bank(self, value: dict):
        self.__oversoul_stat_bank = value

    @starting_position.setter
    def starting_position(self, value: dict):
        self.__starting_position = value

    def output_HP_MP(self, formatted = False, oversoul = False):
        if oversoul == True:
            stat_list = [self.__oversoul_stat_bank["HP"],self.__oversoul_stat_bank["MP"]]
        else:
            stat_list = [self.__stat_bank["HP"], self.__stat_bank["MP"]]
        hex_stat_str = ""
        hex_array_test = []
        count = 0
        for stat in stat_list:
            count = count + 1
            num = ""
            if len(str(hex(stat)[2:])) == 1:
                #print(str(hex(stat)[2:]))
                num = "0" + str(hex(stat)[2:])
            elif len(str(hex(stat)[2:])) == 3:
                temp = "00000" + str(hex(stat)[2:])
                num = temp[6:8] + "0" + temp[5] + "0000"
            elif len(str(hex(stat)[2:])) == 4:
                temp = "0000" + str(hex(stat)[2:])
                num = temp[6:8] + temp[4:6] + "0000"
            elif len(str(hex(stat)[2:])) == 5:
                temp = "000" + str(hex(stat)[2:])
                #print(temp)
                num = temp[6:8] + temp[4:6] + temp[2:4] + temp[0:2]
            else:
                num = str(hex(stat)[2:])
            if count == 1 or count == 2:
                if len(num) == 2:
                    num = num + "000000"
                if len(num) == 4:
                    num = num + "0000"
            hex_array_test.append(num)
            hex_stat_str = hex_stat_str + num  # Append
        if formatted == False:
            return hex_stat_str
        else:
            message = hex_stat_str.upper()
            new_message = ""
            for i in range(1, len(message)):
                if i % 2 == 0:
                    new_message = new_message + " " + message[i - 2:i]
            new_message = new_message + " " + message[-2:len(message)]
            new_message = new_message[1:]
            return new_message

    def search_stats(self, value: str):
        stat_hex = value
        position = self.enemy_hex_data.find(stat_hex)
        return position

    def __repr__(self):
        return f'<Enemy ID = {self.__enemy_id}, Enemy Name = {self.__enemy_name}>'

