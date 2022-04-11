from pathlib import Path
import re

class Enemy:
    def __init__(self, enemy_name_def: str, enemy_id: int, enemy_hex_data_def: str, starting_positions=[0,0]):
        stat_names = ["HP", "MP", "LV", "STR", "DEF", "MAG", "MDEF", "AGL", "ACC", "EVA", "LUCK"]
        self.__enemy_name = enemy_name_def
        self.__enemy_id = enemy_id
        self.__enemy_hex_data = enemy_hex_data_def
        self.__curr_edited_hex_data = ""
        self.__stat_bank = {}
        self.__oversoul_stat_bank = {}
        self.__starting_positions = starting_positions
        self.__experience = 0
        self.__oversoul_experience = 0
        self.__dropped_gil = 0
        self.__stolen_gil = 0
        self.__ap = 0
        self.__item_drop_rate = 0
        self.__steal_rate = 0
        self.__item_drop = {"Normal": ["",""], "Rare": ["",""]}
        self.__stolen_item = {"Normal": ["",""], "Rare": ["",""]}
        self.__bribed_item = {"Normal": ["",""], "Rare": ["",""]}
        self.__stat_hex_positions = []
        self.__stat_hex_oversoul_positions = []
        self.__extra_hex_positions = []
        self.__extra_oversoul_positions = []
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
    def ap(self):
        return self.__ap

    @ap.setter
    def ap(self, value: int):
        self.__ap = value

    @property
    def stat_hex_positions(self):
        return self.__stat_hex_positions

    @stat_hex_positions.setter
    def stat_hex_positions(self, value: list):
        self.__stat_hex_positions = value

    @property
    def stat_hex_oversoul_positions(self):
        return self.__stat_hex_oversoul_positions

    @stat_hex_oversoul_positions.setter
    def stat_hex_oversoul_positions(self, value: list):
        self.__stat_hex_oversoul_positions = value

    @property
    def oversoul_experience(self):
        return self.__oversoul_experience

    @oversoul_experience.setter
    def oversoul_experience(self, value: int):
        self.__oversoul_experience = value

    @property
    def curr_edited_hex_data(self):
        return self.__curr_edited_hex_data

    @curr_edited_hex_data.setter
    def curr_edited_hex_data(self, value: str):
        self.__curr_edited_hex_data = value

    @property
    def extra_hex_positions(self):
        return self.__extra_hex_positions

    @extra_hex_positions.setter
    def extra_hex_positions(self, value: list):
        self.__extra_hex_positions = value

    @property
    def extra_oversoul_positions(self):
        return self.__extra_oversoul_positions

    @extra_oversoul_positions.setter
    def extra_oversoul_positions(self, value: list):
        self.__extra_oversoul_positions = value

    @property
    def item_drop_rate(self):
        return self.__item_drop_rate

    @item_drop_rate.setter
    def item_drop_rate(self, value: int):
        self.__item_drop_rate = value

    @property
    def steal_rate(self):
        return self.__steal_rate

    @steal_rate.setter
    def steal_rate(self, value: int):
        self.__steal_rate = value

    @property
    def item_drop(self):
        return self.__item_drop

    @item_drop.setter
    def item_drop(self, value: dict):
        self.__item_drop = value

    @property
    def stolen_item(self):
        return self.__item_drop

    @stolen_item.setter
    def stolen_item(self, value: dict):
        self.__stolen_item = value

    @property
    def bribed_item(self):
        return self.__bribed_item

    @bribed_item.setter
    def bribed_item(self, value: dict):
        self.__bribed_item = value

    @property
    def experience(self):
        return self.__experience

    @experience.setter
    def experience(self, value: int):
        self.__experience = value

    @property
    def dropped_gil(self):
        return self.__dropped_gil

    @dropped_gil.setter
    def dropped_gil(self, value: int):
        self.__dropped_gil = value

    @property
    def stolen_gil(self):
        return self.__stolen_gil

    @stolen_gil.setter
    def stolen_gil(self, value: int):
        self.__stolen_gil = value

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
    def starting_positions(self):
        return self.__starting_positions

    @enemy_name.setter
    def enemy_name(self, value: str):
        self.__enemy_name = value

    @enemy_id.setter
    def enemy_id(self, value: int):
        self.__enemy_id = value

    @enemy_hex_data.setter
    def enemy_hex_data(self, value: str):
        self.__enemy_hex_data = value

    @stat_bank.setter
    def stat_bank(self, value: dict):
        self.__stat_bank = value

    @oversoul_stat_bank.setter
    def oversoul_stat_bank(self, value: dict):
        self.__oversoul_stat_bank = value

    @starting_positions.setter
    def starting_positions(self, value: list):
        self.__starting_positions = value

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
            elif len(str(hex(stat)[2:])) == 6:
                temp = "00" + str(hex(stat)[2:])
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

    def get_original_hex_stat_position(self, oversoul_bool=False):
        if oversoul_bool == True:
            stat_hex = self.output_HP_MP(formatted=False, oversoul=True)
            position = self.enemy_hex_data.find(stat_hex)
            return position
        stat_hex = self.output_HP_MP(formatted=False, oversoul=False)
        position = self.enemy_hex_data.find(stat_hex)
        return position

    def get_original_hex_stat(self, oversoul_bool = False):
        if oversoul_bool == False:
            stat_hex = self.output_HP_MP(formatted=False, oversoul=False)
            position = self.enemy_hex_data.find(stat_hex)
            original_hex = self.enemy_hex_data[position:position+16]
        else:
            stat_hex = self.output_HP_MP(formatted=False, oversoul=True)
            position = self.enemy_hex_data.find(stat_hex)
            original_hex = self.enemy_hex_data[position:position + 16]
        return original_hex


    def __repr__(self):
        return f'<Enemy ID = {self.__enemy_id}, Enemy Name = {self.__enemy_name}>'

