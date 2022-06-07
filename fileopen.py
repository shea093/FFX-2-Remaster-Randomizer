import binascii
import re
import copy
import item
from services import *
from enemy import Enemy
from pathlib import Path
from dressphere_execute import global_monsters

file_iterations = 369
item_list = item.initialize_items()

# Read a binary file and convert it into hex data
def read_hex(path):
    with path.open(mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data


# Get the directories with the monster files
def get_subdirectories(path):
    vbf_str = path
    vbf_dir = Path(vbf_str)  # VBF Directory
    vbf_subdirs = []   # Subdirectory list initialized

    # Iterate through subdirectories and append them to a list
    [vbf_subdirs.append(x) for x in vbf_dir.iterdir() if x.is_dir()]

    return vbf_subdirs


# Possibly useless lol
def mon_binlist_generator():
    mon_nums = list(range(1, file_iterations+1)) #Range of files to traverse
    mon_list = []
    for n in mon_nums:
        if n < 10:
            mon_string = "m" + "00" + str(n) + ".bin"
        elif n < 100:
            mon_string = "m" + "0" + str(n) + ".bin"
        else:
            mon_string = "m" + str(n) + ".bin"
        mon_list.append(mon_string)
    return mon_list


# Get list of hex strings from the files
def traverse_files():
    mon_filenames = mon_binlist_generator()
    mon_directories = get_subdirectories("VBF_X2")
    mon_hex_files = []
    for directory in mon_directories:
        for file in directory.iterdir():
            if file.is_file() and file.name in mon_filenames:
                mon_hex_files.append((read_hex(file)))
    return mon_hex_files


def cut_creature_values():
    creature_names = []
    with open("Obselete/creaturevalues.txt", "r") as f:
        for line in f.readlines():
            match = re.search('"[^"]+"', line)
            match = match.group()
            match = match[1:-1]
            creature_names.append(match)
    with open("Obselete/new_creature_values.txt", "w") as f:
        for line in creature_names:
            f.write(line + "\n")

def cut_creature_english_names():
    creature_names = []
    with open("Obselete/english_creature_names.txt", "r") as f:
        for line in f.readlines():
            pre_slice = line[5:27]
            pre_slice = re.sub(r"\s+", "", pre_slice, flags=re.UNICODE)
            creature_names.append(pre_slice)
    with open("Obselete/new_english_creature_names.txt", "w") as f:
        for line in creature_names:
            f.write(line + "\n")


def search_stats(hexes):
    stat_hex = "237a0800"
    position = str(hexes[0]).find(stat_hex)
    return position


def cut_line_HPMP(line: str):
    value = line
    returnlist = value.split(", ")
    returnlist[-1] = returnlist[-1].strip()
    return returnlist


def test_enemy_maker(hexes, max=369):
    enemies = []
    with open("HPMP.txt", "r") as f:
        id = 0
        for line in f.readlines():
            id = id + 1
            enemy_info = cut_line_HPMP(line)
            enemy = Enemy(enemy_info[0],id,hexes[id-1])
            enemy.og_hex_data = hexes[id-1]
            enemy.mongetchunk = global_monsters[id-1].big_chunk
            enemy.stat_bank["HP"] = int(enemy_info[1])
            enemy.stat_bank["MP"] = int(enemy_info[2])
            enemy.oversoul_stat_bank["HP"] = int(enemy_info[3])
            enemy.oversoul_stat_bank["MP"] = int(enemy_info[4])
            enemies.append(enemy)
            if id == max:
                break
    return enemies


def redo_hex(enemy_object: Enemy, multiplier: float, oversoul_multiplier: float, oversoul_yesno = False):
    #bugged_ids = [82,195,196,197,198,199,200,208,209,252,260,263,264,288]
    # if (enemy_object.stat_bank["HP"] == 0 or enemy_object.stat_bank["HP"] == 1) and (enemy_object.stat_bank["MP"] == 0 or enemy_object.stat_bank["MP"] == 1):
    #     return enemy_object
    # elif enemy_object.enemy_id in bugged_ids:
    #     return enemy_object

    og_hex = enemy_object.get_original_hex_stat()
    og_oversoul_hex = enemy_object.get_original_hex_stat(oversoul_bool=True)
    new_enemy_instance = copy.deepcopy(enemy_object)
    new_enemy_instance.starting_positions = [new_enemy_instance.get_original_hex_stat_position(), new_enemy_instance.get_original_hex_stat_position(oversoul_bool=True)]
    new_enemy_instance.stat_bank["HP"] = round(new_enemy_instance.stat_bank["HP"] * multiplier)
    new_enemy_instance.oversoul_stat_bank["HP"] = round(new_enemy_instance.oversoul_stat_bank["HP"] * oversoul_multiplier)
    new_hex = new_enemy_instance.output_HP_MP(formatted=False)
    new_enemy_instance.curr_edited_hex_data = new_enemy_instance.enemy_hex_data.replace(og_hex, new_hex)
    if oversoul_yesno != False:
        new_oversoul_hex = new_enemy_instance.output_HP_MP(formatted=False, oversoul=True)
        new_enemy_instance.curr_edited_hex_data = new_enemy_instance.curr_edited_hex_data.replace(og_oversoul_hex, new_oversoul_hex)
    if len(enemy_object.enemy_hex_data) != len(new_enemy_instance.curr_edited_hex_data):
        print("***********")
        print("UH OH")
        print(str(enemy_object)," is bugged.")
    return new_enemy_instance



def set_enemy_data(enemy_list: list[Enemy]):
    for enemy in enemy_list:
        if enemy.get_original_hex_stat_position() < 0:
            test = ""
            pass
        else:
            if enemy.enemy_id in normal_error_ids:
                pass
            else:
                start_pos = enemy.get_original_hex_stat_position() + len(enemies[0].output_HP_MP(formatted=False))
                enemy.stat_bank["LV"] = int(enemy.enemy_hex_data[start_pos:start_pos + 2], 16)
                curr_pos = start_pos + 2
                enemy.stat_bank["STR"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["DEF"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["MAG"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["MDEF"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["AGL"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["ACC"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["EVA"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_bank["LUCK"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_hex_positions = [start_pos,start_pos+2,start_pos+2+2,start_pos+2+2+2,start_pos+2+2+2+2,
                                            start_pos+2+2+2+2+2, start_pos+2+2+2+2+2+2, start_pos+2+2+2+2+2+2+2,
                                            start_pos+2+2+2+2+2+2+2+2]

                exp_start_pos = enemy.get_original_hex_stat_position() + 296
                extra_hex_position0 = exp_start_pos
                experience_value = reverse_four_bytes(enemy.enemy_hex_data[exp_start_pos:exp_start_pos + 8])
                curr_exp_pos = exp_start_pos + 8
                dropped_gil_value = reverse_four_bytes(enemy.enemy_hex_data[curr_exp_pos:curr_exp_pos + 8])
                curr_exp_pos = curr_exp_pos + 8
                stolen_gil_value = reverse_four_bytes(enemy.enemy_hex_data[curr_exp_pos:curr_exp_pos + 8])
                enemy.experience = int(experience_value, 16)
                enemy.dropped_gil = int(dropped_gil_value, 16)
                enemy.stolen_gil = int(stolen_gil_value, 16)
                curr_exp_pos = curr_exp_pos + 8
                enemy.ap = int(reverse_two_bytes(enemy.enemy_hex_data[curr_exp_pos:curr_exp_pos + 4]), 16)
                curr_exp_pos = curr_exp_pos + 4
                enemy.item_drop_rate = int(enemy.enemy_hex_data[curr_exp_pos:curr_exp_pos + 2], 16)
                curr_exp_pos = curr_exp_pos + 2
                enemy.steal_rate = int(enemy.enemy_hex_data[curr_exp_pos:curr_exp_pos + 2], 16)
                curr_exp_pos = curr_exp_pos + 2
                normal_item_hex = reverse_two_bytes(enemy.enemy_hex_data[curr_exp_pos:curr_exp_pos + 4])
                normal_drop_item = [search_items_by_id(item_list, normal_item_hex),
                                    int(reverse_two_bytes(enemy.enemy_hex_data[curr_exp_pos + 4:curr_exp_pos + 8]), 16)]
                rare_item_hex = reverse_two_bytes(enemy.enemy_hex_data[curr_exp_pos + 8:curr_exp_pos + 12])
                rare_drop_item = [search_items_by_id(item_list, rare_item_hex),
                                  int(reverse_two_bytes(enemy.enemy_hex_data[curr_exp_pos + 12:curr_exp_pos + 16]), 16)]
                enemy.item_drop["Normal"] = normal_drop_item
                enemy.item_drop["Rare"] = rare_drop_item
                extra_hex_positions = [extra_hex_position0, extra_hex_position0 + 8, extra_hex_position0 + 8 + 8,
                                       extra_hex_position0 + 8 + 8 + 8,
                                       extra_hex_position0 + 8 + 8 + 8 + 4, extra_hex_position0 + 8 + 8 + 8 + 4 + 2,
                                       extra_hex_position0 + 8 + 8 + 8 + 4 + 2 + 2,
                                       extra_hex_position0 + 8 + 8 + 8 + 4 + 2 + 2 + 4,
                                       extra_hex_position0 + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4,
                                       extra_hex_position0 + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4
                                       ]
                enemy.extra_hex_positions = extra_hex_positions

            ...

            if enemy.enemy_id in oversoul_error_ids:
                test = ""
                pass
            else:
                start_oversoul_pos = enemy.get_original_hex_stat_position(oversoul_bool=True) + len(
                    enemies[0].output_HP_MP(formatted=False, oversoul=True))
                enemy.oversoul_stat_bank["LV"] = int(enemy.enemy_hex_data[start_oversoul_pos:start_oversoul_pos + 2], 16)
                curr_pos = start_oversoul_pos + 2
                enemy.oversoul_stat_bank["STR"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["DEF"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["MAG"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["MDEF"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["AGL"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["ACC"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["EVA"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.oversoul_stat_bank["LUCK"] = int(enemy.enemy_hex_data[curr_pos:curr_pos + 2], 16)
                curr_pos = curr_pos + 2
                enemy.stat_hex_oversoul_positions = [start_oversoul_pos, start_oversoul_pos + 2, start_oversoul_pos + 2 + 2, start_oversoul_pos + 2 + 2 + 2,
                                            start_oversoul_pos + 2 + 2 + 2 + 2,
                                            start_oversoul_pos + 2 + 2 + 2 + 2 + 2, start_oversoul_pos + 2 + 2 + 2 + 2 + 2 + 2,
                                            start_oversoul_pos + 2 + 2 + 2 + 2 + 2 + 2 + 2,
                                            start_oversoul_pos + 2 + 2 + 2 + 2 + 2 + 2 + 2]
                exp_start_pos = enemy.get_original_hex_stat_position(oversoul_bool=True) + 296
                oversoul_hex_pos = exp_start_pos
                experience_value = reverse_four_bytes(enemy.enemy_hex_data[exp_start_pos:exp_start_pos + 8])
                enemy.oversoul_experience = int(experience_value, 16)
                extra_oversoul_positions = [oversoul_hex_pos, oversoul_hex_pos + 8, oversoul_hex_pos + 8 + 8,
                                            oversoul_hex_pos + 8 + 8 + 8,
                                            oversoul_hex_pos + 8 + 8 + 8 + 4, oversoul_hex_pos + 8 + 8 + 8 + 4 + 2,
                                            oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2,
                                            oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4,
                                            oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4,
                                            oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4
                                            ]
                enemy.extra_oversoul_positions = extra_oversoul_positions

def batch_strength_defence_overwrite(enemy_list: list[Enemy]):
    for enemy in enemy_list:
        if enemy.enemy_id in normal_error_ids:
            test = ""
            pass
        else:
            new_str = int(enemy.stat_bank["STR"]*1.5)
            if new_str > 255:
                new_str = 255
            new_mag = int(enemy.stat_bank["MAG"]*1.7)
            if new_mag > 255:
                new_mag = 255
            enemy.stat_bank["STR"] = new_str
            enemy.stat_bank["MAG"] = new_mag

            new_def = enemy.stat_bank["DEF"]
            new_mdef = enemy.stat_bank["MDEF"]
            if enemy.stat_bank["DEF"] < 30:
                pass
            else:
                new_def = int(enemy.stat_bank["DEF"]*0.7)

            new_mdef = int(enemy.stat_bank["MDEF"] * 0.7)

            if new_mdef > 50:
                new_mdef = 50

            enemy.stat_bank["DEF"] = new_def
            enemy.stat_bank["MDEF"] = new_mdef

            #Experience multiplier
            enemy.experience = int(enemy.experience * 0.5)

        ...


        #Oversoul
        if enemy.enemy_id in oversoul_error_ids:
            test = ""
            pass
        else:
            new_str = int(enemy.oversoul_stat_bank["STR"] * 1.5)
            if new_str > 255:
                new_str = 255
            new_mag = int(enemy.oversoul_stat_bank["MAG"] * 1.7)
            if new_mag > 255:
                new_mag = 255
            enemy.oversoul_stat_bank["STR"] = new_str
            enemy.oversoul_stat_bank["MAG"] = new_mag

            new_def = enemy.oversoul_stat_bank["DEF"]
            new_mdef = enemy.oversoul_stat_bank["MDEF"]
            if enemy.oversoul_stat_bank["DEF"] < 30:
                pass
            else:
                new_def = int(enemy.oversoul_stat_bank["DEF"] * 0.7)

            if enemy.stat_bank["MDEF"] < 30:
                pass
            else:
                new_mdef = int(enemy.oversoul_stat_bank["MDEF"] * 0.58)

            enemy.oversoul_stat_bank["DEF"] = new_def
            enemy.oversoul_stat_bank["MDEF"] = new_mdef

            # Oversoul Experience multiplier
            enemy.oversoul_experience = int(enemy.oversoul_experience * 0.65)

def overwrite_hex_data_str_def_exp(enemy_list: list[Enemy]):
    return_list = enemy_list
    for enemy in return_list:
        if enemy.enemy_id in normal_error_ids:
            test = ""
            pass
        else:
            if (enemy.starting_positions[0] < 1):
                pass
            elif len(enemy.curr_edited_hex_data) < 1:
                pass
            else:
                compare_og = enemy.curr_edited_hex_data
                first_chunk = enemy.curr_edited_hex_data[0:enemy.stat_hex_positions[1]]     #Index 1 because we don't want to edit LV (yet)
                stat_list = [convert_gamevariable_to_reversed_hex(enemy.stat_bank["STR"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["DEF"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["MAG"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["MDEF"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["AGL"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["ACC"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["EVA"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.stat_bank["LUCK"],bytecount=1)]
                stat_chunk = "".join(stat_list)
                next_index = enemy.stat_hex_positions[1] + len(stat_chunk)
                statend_to_exp_chunk = enemy.curr_edited_hex_data[next_index:enemy.extra_hex_positions[0]]
                exp_chunk = convert_gamevariable_to_reversed_hex(enemy.experience,bytecount=4)
                last_index = enemy.extra_hex_positions[0] + len(exp_chunk)
                last_chunk = enemy.curr_edited_hex_data[last_index:]
                combined = first_chunk + stat_chunk + statend_to_exp_chunk + exp_chunk + last_chunk
                if len(combined) != len(compare_og):
                    print(enemy)
                    print(len(combined))
                    print(len(compare_og))
                    raise ValueError
                else:
                    enemy.curr_edited_hex_data = combined

        ...
        if enemy.enemy_id in oversoul_error_ids:
            pass
        else:
            if (enemy.starting_positions[1] < 1):
                pass
            elif len(enemy.curr_edited_hex_data) < 1:
                pass
            else:
                compare_og = enemy.curr_edited_hex_data
                first_chunk = enemy.curr_edited_hex_data[0:enemy.stat_hex_oversoul_positions[1]]     #Index 1 because we don't want to edit LV (yet)
                stat_list = [convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["STR"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["DEF"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["MAG"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["MDEF"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["AGL"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["ACC"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["EVA"],bytecount=1),
                              convert_gamevariable_to_reversed_hex(enemy.oversoul_stat_bank["LUCK"],bytecount=1)]
                stat_chunk = "".join(stat_list)
                next_index = enemy.stat_hex_oversoul_positions[1] + len(stat_chunk)
                statend_to_exp_chunk = enemy.curr_edited_hex_data[next_index:enemy.extra_oversoul_positions[0]]
                exp_chunk = convert_gamevariable_to_reversed_hex(enemy.experience,bytecount=4)
                last_index = enemy.extra_oversoul_positions[0] + len(exp_chunk)
                last_chunk = enemy.curr_edited_hex_data[last_index:]
                combined = first_chunk + stat_chunk + statend_to_exp_chunk + exp_chunk + last_chunk
                len1 = len(combined)
                len2 = len(compare_og)
                test = ""
                if len(combined) != len(compare_og):
                    print(enemy)
                    print(len(combined))
                    print(len(compare_og))
                    raise ValueError
                else:
                    enemy.curr_edited_hex_data = combined











# Tests
print(cut_line_HPMP("etc"))
cut_creature_english_names()
print(get_subdirectories("VBF_X2"))
print(mon_binlist_generator())
hex_test = traverse_files()
print(type(hex_test[0]))
enemies = test_enemy_maker(hex_test, max=file_iterations)
print(enemies)


print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
errors = 0
normal_errors = 0
oversoul_errors = 0

normal_error_ids = []
oversoul_error_ids = []

for index, enemy in enumerate(enemies):
    hp_mp_hex = enemy.output_HP_MP(formatted=False, oversoul=False)
    position = str(enemy.enemy_hex_data).find(hp_mp_hex)
    # ignore = False
    # if (enemy.stat_bank["HP"] == 0 or enemy.stat_bank["HP"] == 1) and (enemy.stat_bank["MP"] == 0 or enemy.stat_bank["MP"] == 1):
    #     ignore = True
    if position == -1:
        normal_error_ids.append(enemy.enemy_id)
        errors = errors + 1
        normal_errors = normal_errors + 1
        print(enemy)
        print(f"{index + 1:03}" + ".    " + enemy.output_HP_MP(formatted=True, oversoul=False))
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")

for index, enemy in enumerate(enemies):
    hp_mp_hex = enemy.output_HP_MP(formatted=False, oversoul=True)
    position = str(enemy.enemy_hex_data).find(hp_mp_hex)
    if position == -1:
        oversoul_error_ids.append(enemy.enemy_id)
        errors = errors + 1
        oversoul_errors = oversoul_errors + 1
        print(enemy)
        print(f"{index + 1:03}" + ".    " + enemy.output_HP_MP(formatted=True, oversoul=True))


print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("Non-oversoul Errors: ", normal_errors, "/",file_iterations)
print("Oversoul Errors: ", oversoul_errors, "/",file_iterations)


print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")

def overwrite_HP_batch(enemies: list[Enemy]):
    new_enemies = []
    count_of_successful_changes = 0
    for enemy in enemies:
        if enemy.enemy_id not in normal_error_ids and enemy.get_original_hex_stat_position(oversoul_bool=True) > 1:
            new_enemies.append(redo_hex(enemy, 2.45, 2.45, oversoul_yesno=True))
            count_of_successful_changes = count_of_successful_changes + 1
        elif enemy.enemy_id not in normal_error_ids and enemy.get_original_hex_stat_position(oversoul_bool=True) < 1:
                new_enemies.append(redo_hex(enemy, 2.45, 2.45, oversoul_yesno=False))
                count_of_successful_changes = count_of_successful_changes + 1
        else:
            new_enemies.append(enemy)


    return new_enemies

# def test_write_randomizer(new_enemies_list):
#     new_enemies = new_enemies_list
#     for index, directory in enumerate(get_subdirectories("VBF_RANDO_TEST")):
#         bin_name = str(directory.name[1:]) + ".bin"
#         if bin_name not in mon_binlist_generator():
#             pass
#         # elif int(directory.name[2:]) == new_enemies[int(directory.name[2:])].enemy_id:
#         #     print("please")
#         #     print(new_enemies[index])
#         else:
#             id = int(directory.name[2:])
#
#             for enemy in new_enemies:
#                 if enemy.enemy_id == id:
#                     filepath = directory / bin_name
#                     print("Enemy ID: " + str(enemy.enemy_id))
#                     print("Bin name: "+ str(bin_name))
#                     print(enemy.output_HP_MP(formatted=True, oversoul=False))
#                     binary_converted = binascii.unhexlify(enemy.enemy_hex_data)
#                     with filepath.open(mode="wb") as f:
#                         f.write(binary_converted)
#                     print("Done i think????")


# print(Path.cwd())
# print(get_subdirectories("VBF_X2_NEW"))
print(enemies[0])
print(enemies[0].stat_bank)
print(enemies[0].output_HP_MP(formatted=False))
print(enemies[0].get_original_hex_stat_position())







#IMPORTANT: For now please use Set_Enemy_data BEFORE overwrite HP batch!!!
#Need to fix starting positions as currently set_enemy_data is using the get_og_starting_position function instead of the starting_position variable
set_enemy_data(enemies)
test = ""
enemies = overwrite_HP_batch(enemies)
test = ""
print(enemies[294])
batch_strength_defence_overwrite(enemies)
print("----------")
print("----")
overwrite_hex_data_str_def_exp(enemies)


#WRITE ALL THE BIN FILES
def write_bins():
    for index, directory in enumerate(get_subdirectories("VBF_X2_NEW")):
        bin_name = str(directory.name[1:]) + ".bin"
        if bin_name not in mon_binlist_generator():
            pass
        # elif int(directory.name[2:]) == new_enemies[int(directory.name[2:])].enemy_id:
        #     print("please")
        #     print(new_enemies[index])
        else:
            bad_ids = [194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,216,236,240,255,257,259,261,262,264,265,267,272,281,282,283,287,290,
                       296,297,298,299,300,301,305,306,307,310,312,314,316,318,334,335,336,337,338,186,187,174,157,139,140,141,142,143,116,117,
                       118,119,105,86,]
            id = int(directory.name[2:])
            for enemy in enemies:
                if enemy.enemy_id == id:
                    if enemy.enemy_id in bad_ids:
                        filepath = directory / bin_name
                        print("----------------")
                        print("Errored")
                        binary_converted = binascii.unhexlify(enemy.og_hex_data)
                        with filepath.open(mode="wb") as f:
                            f.write(binary_converted)
                        print("----------------")

                    elif enemy.enemy_id not in normal_error_ids:
                        filepath = directory / bin_name
                        print("Enemy ID: " + str(enemy.enemy_id))
                        print("Bin name: "+ str(bin_name))
                        print(enemy.output_HP_MP(formatted=True, oversoul=False))
                        binary_converted = binascii.unhexlify(enemy.curr_edited_hex_data)
                        compare = binascii.unhexlify(enemy.og_hex_data)
                        if len(compare) != len (binary_converted):
                            raise ValueError
                        with filepath.open(mode="wb") as f:
                            f.write(binary_converted)
                        print("Done i think????")
                    else:
                        filepath = directory / bin_name
                        print("----------------")
                        print("Errored")
                        binary_converted = binascii.unhexlify(enemy.og_hex_data)
                        with filepath.open(mode="wb") as f:
                            f.write(binary_converted)
                        print("----------------")

write_bins()

# print(new_enemies[0].output_HP_MP(formatted=False, oversoul=False))
# print(new_enemies[0].enemy_hex_data.find(new_enemies[0].output_HP_MP(formatted=False, oversoul=False)))

# for enemy in new_enemies:
#     print(enemy)

# print(str(new_enemies[333].enemy_id) + ".  " + str(new_enemies[333].stat_bank["HP"]))
# print(new_enemies[333].output_HP_MP())

# object_test = Enemy("Sallet", 1, hex_test[0])
# object_test.stat_bank["HP"] = 60
# object_test.stat_bank["MP"] = 4
# object_test.oversoul_stat_bank["HP"] = 248
# object_test.oversoul_stat_bank["MP"] = 4
# print(test_enemy_maker(hex_test, max=2))
# print(object_test.stat_bank)
# print(object_test.output_HP_MP(formatted=True))
# print(object_test.output_HP_MP(formatted=True, oversoul=True))
# print(search_stats(hex_test))
# print(object_test.search_stats(object_test.output_HP_MP(oversoul=True)))
# cut_creature_values()