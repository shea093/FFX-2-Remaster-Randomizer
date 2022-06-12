import pathlib
import random
import binascii
from command import Command
from services import *
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        test = ""

    return os.path.join(base_path, relative_path)

# from abilty_tiers import tier1_abilities
# INPUT VARIABLES
job_bin_path = resource_path(pathlib.PureWindowsPath("Test Files\job.bin"))
cmd_bin_path = resource_path(pathlib.PureWindowsPath("Test Files\command.bin"))
auto_bin_path = resource_path(pathlib.PureWindowsPath("Test Files/a_ability.bin"))
seed_path = resource_path(pathlib.PureWindowsPath("Test Files/seed.txt"))
monmagic_bin_path = resource_path(pathlib.PureWindowsPath("Test Files/monmagic.bin"))
monget_bin_path = resource_path(pathlib.PureWindowsPath("Test Files/mon_get.bin"))


def read_seed():
    this_seed = 0
    with open(seed_path, 'r') as seed_file:
        try:
            this_seed = int(seed_file.read())
        except:
            print("Error reading seed.txt file, please make sure it contains a valid integer.")
            exit()
    return this_seed


seed = read_seed()

# from abilty_tiers import tier2_abilities
# from abilty_tiers import tier3_abilities


jobs_names = [
    "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku2", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02",
    "trainer03", "mascot02",
    "mascot03", "psychic", "festivalist01", "festivalist02", "festilvalist03"
]


# previous seed: 111876967976853241
# 659
# MAIN SEED 790723



def job_bin_to_hex():
    job_bin = pathlib.Path(job_bin_path)
    hex_data = read_hex(job_bin)
    return hex_data


def cmd_bin_to_hex():
    cmd_bin = pathlib.Path(cmd_bin_path)
    hex_data = read_hex(cmd_bin)
    return hex_data


def auto_bin_to_hex():
    auto_bin = pathlib.Path(auto_bin_path)
    hex_data = read_hex(auto_bin)
    return hex_data

def monmagic_bin_to_hex():
    monmagic_bin = pathlib.Path(monmagic_bin_path)
    hex_data = read_hex(monmagic_bin)
    return hex_data

def monget_bin_to_hex():
    monget_bin = pathlib.Path(monget_bin_path)
    hex_data = read_hex(monget_bin)
    return hex_data

def get_big_chunks(get_all_segments=False, segment_type="job"):
    chunks = []
    hex_file = ""
    initial_position = 0
    next_position = 0
    if segment_type == "job":
        hex_file = job_bin_to_hex()
        initial_position = 520
        next_position = 976
    elif segment_type == "command":
        hex_file = cmd_bin_to_hex()
        initial_position = 64
        next_position = 64 + 280
    elif segment_type == "auto-ability":
        hex_file = auto_bin_to_hex()
        initial_position = 64
        next_position = 64 + 352
    elif segment_type == "mon-magic":
        hex_file = monmagic_bin_to_hex()
        initial_position = 64
        next_position = 64 + 272
    elif segment_type == "mon-get":
        hex_file = monget_bin_to_hex()
        initial_position = 64
        next_position = 64 + 280
    start_chunk = hex_file[initial_position:next_position]
    chunks.append(start_chunk)
    ending_chunk = ""
    if segment_type == "command":
        for i in range(0, 553):
            initial_position = next_position
            next_position = next_position + 280
            chunks.append(hex_file[initial_position:next_position])
            if i == 552 and get_all_segments is True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segment_type == "job":
        for i in range(0, 30):
            initial_position = next_position
            next_position = next_position + 456
            chunks.append(hex_file[initial_position:next_position])
            if i == 29 and get_all_segments is True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segment_type == "auto-ability":
        for i in range(0, 161):
            initial_position = next_position
            next_position = next_position + 352
            chunks.append(hex_file[initial_position:next_position])
            if i == 160 and get_all_segments is True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segment_type == "mon-magic":
        for i in range(0, 567):
            initial_position = next_position
            next_position = next_position + 272
            chunks.append(hex_file[initial_position:next_position])
            if i == 566 and get_all_segments is True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segment_type == "mon-get":
        for i in range(0, 369):
            initial_position = next_position
            next_position = next_position + 280
            chunks.append(hex_file[initial_position:next_position])
            # if i == 369 and get_all_segments is True:
            #     ending_chunk = hex_file[next_position:len(hex_file)]
    if get_all_segments is True:
        beginning_chunk = hex_file[0:520]
        if segment_type == "command":
            beginning_chunk = hex_file[0:64]
            return [beginning_chunk, chunks, ending_chunk]
        if segment_type == "auto-ability":
            beginning_chunk = hex_file[0:64]
            return [beginning_chunk, chunks, ending_chunk]
        if segment_type == "mon-magic":
            beginning_chunk = hex_file[0:64]
            return [beginning_chunk, chunks, ending_chunk]
        if segment_type == "mon-get":
            beginning_chunk = hex_file[0:344]
            return [beginning_chunk, chunks]
        return [beginning_chunk, chunks, ending_chunk]
    else:
        return chunks


def test_randomize_big_chunks(seed_value: int):
    chunks = get_big_chunks(get_all_segments=True)
    random.Random(seed_value).shuffle(chunks[1])
    return chunks


def cut_command_names(valid_abilities=False):
    command_ids = []
    filename = resource_path("Test Files/commands.txt")
    if valid_abilities is True:
        filename = resource_path("Test Files/valid_commands.txt")
    with open(filename, "r") as f:
        for line in f.readlines():
            this_id = line[32:36]
            name = line[46:len(line)]
            name = name[:name.find("\"")]
            tupl = (this_id, name)
            command_ids.append(tupl)
    return command_ids


def cut_monmagic_names(valid_abilities=False):
    monmagic_ids = []
    filename = resource_path("Test Files/monmagic.txt")
    if valid_abilities is True:
        pass
    with open(filename, "r") as f:
        for line in f.readlines():
            this_id = line[32:36]
            name = line[46:len(line)]
            name = name[:name.find("\"")]
            tupl = (this_id, name)
            monmagic_ids.append(tupl)
    return monmagic_ids


def cut_autoability_names():
    autoability_ids = []
    with open(resource_path("Test Files/auto_abilities.txt"), "r") as f:
        for line in f.readlines():
            this_id = line[36:40]
            name = line[50:len(line)]
            name = name[:name.find("\"")]
            tupl = (this_id, name)
            autoability_ids.append(tupl)
    return autoability_ids


command_global_chunks = get_big_chunks(segment_type="command")
auto_global_chunks = get_big_chunks(segment_type="auto-ability")
monmagic_global_chunks = get_big_chunks(segment_type="mon-magic")


# Initiates the list of abilities
# valid_ability_pooling is an argument for shuffle_abilities()
# that returns only abilities that are intended to be shuffled

def initiate_abilities(valid_ability_pooling=False, monster_magic=False) -> list[Command]:
    abilities = []
    if monster_magic is True:
        monmagic_tuples = cut_monmagic_names()
        for chunkindex, command in enumerate(monmagic_tuples):
            cmd = Command(id_value=command[0], name_value=command[1], type_value="Mon-Magic")
            cmd.og_hex_chunk = monmagic_global_chunks[chunkindex]
            abilities.append(cmd)
        if valid_ability_pooling is False:
            return abilities
    if valid_ability_pooling is True:
        valid_ability_tuples = cut_command_names(valid_abilities=True)
        for ability in valid_ability_tuples:
            if int(ability[0], 16) <= 12841:
                cmd = Command(id_value=ability[0], name_value=ability[1], type_value="Command")
                # print(cmd)
                abilities.append(cmd)
            else:
                auto = Command(id_value=ability[0].upper(), name_value=ability[1], type_value="Auto-Ability")
                abilities.append(auto)
    else:
        command_tuples = cut_command_names()
        autoability_tuples = cut_autoability_names()
        for chunkindex, command in enumerate(command_tuples):
            cmd = Command(id_value=command[0], name_value=command[1], type_value="Command")
            cmd.og_hex_chunk = command_global_chunks[chunkindex]
            abilities.append(cmd)
        for autochunkindex, autoability in enumerate(autoability_tuples):
            auto = Command(id_value=autoability[0].upper(), name_value=autoability[1], type_value="Auto-Ability")
            auto.og_hex_chunk = auto_global_chunks[autochunkindex]
            abilities.append(auto)
    return abilities

heading_chunk = get_big_chunks(get_all_segments=True,segment_type="command")[0]
global_number_of_abilities = int(reverse_four_bytes(heading_chunk[32:40]),16)
global_number_of_bytes_after_header = int(reverse_four_bytes(heading_chunk[48:56]),16)
global_abilities = initiate_abilities()
mon_magic_abilities = initiate_abilities(monster_magic=True)

cmd_name_help_list = []
with open(resource_path("Test Files/commandtext"), 'r', encoding = "utf_8") as cmdtext:
    cmdtext_str = cmdtext.readline()
    cmd_name_help_list = cmdtext_str.split("◘")
    cmd_name_help_list = cmd_name_help_list[0:-1]

cmd_names = cmd_name_help_list[::2]
cmd_helps = cmd_name_help_list[1::2]
test = ""

for index, abi in enumerate(global_abilities):
    if abi.type == "Command":
        abi.name = cmd_names[index]
        abi.name_og_length = len(cmd_names[index])
        abi.help_og_length = len(cmd_helps[index])
        abi.help_text = cmd_helps[index]
        name_start_index_hex = reverse_two_bytes(abi.og_hex_chunk[0:4])
        help_start_index_hex = reverse_two_bytes(abi.og_hex_chunk[8:12])
        abi.name_start_index = int(name_start_index_hex, 16)
        abi.help_start_index = int(help_start_index_hex, 16)
        abi.new_help_text = cmd_helps[index]
        abi.new_name_text = cmd_names[index]




def set_ability_ap_batch():
    for ability in global_abilities:
        if ability.type == "Command":
            hex_cut = ability.og_hex_chunk[268:268 + 4]
            hex_input = reverse_two_bytes(hex_cut)
            if len(hex_input) != 4:
                pass
            else:
                ability.ap = int(hex_input, 16)
        elif ability.type == "Auto-Ability":
            hex_cut = ability.og_hex_chunk[348:348 + 4]
            hex_input = reverse_two_bytes(hex_cut)
            if len(hex_input) != 4:
                pass
            else:
                ability.ap = int(hex_input, 16)


#Updated to also add the Name/Help index positions
def set_dmg_info_batch():
    for ability in global_abilities:
        if ability.type == "Command":
            hex_cut = ability.og_hex_chunk[76:76 + 14]
            nth = 2
            hex_list = [hex_cut[i:i + nth] for i in range(0, len(hex_cut), nth)]
            # dmg_info_names = ["MP Cost", "Target", "Calc PS", "Crit", "Hit", "Power"]
            ability.dmg_info["MP Cost"] = int(hex_list[0], 16)
            ability.dmg_info["Target HP/MP"] = int(hex_list[1], 16)
            ability.dmg_info["Calc PS"] = int(hex_list[2], 16)
            ability.dmg_info["Crit"] = int(hex_list[3], 16)
            ability.dmg_info["Hit"] = int(hex_list[4], 16)
            ability.dmg_info["Power"] = int(hex_list[5], 16)
            ability.dmg_info["Number of Attacks"] = int(hex_list[6], 16)
            cast_cut = ability.og_hex_chunk[68:76]
            cast_time = reverse_two_bytes(cast_cut[4:8])
            wait_time = reverse_two_bytes(cast_cut[0:4])
            test = ""
            ability.dmg_info["Cast Time"] = int(cast_time, 16)
            ability.dmg_info["Wait Time"] = int(wait_time, 16)

            #DEBUG, DELETE LATER
            ability.dmg_info["Start Motion"] = ability.og_hex_chunk[24:26]
        #Start indexes for name / help text
        ability.name_start_index = int(reverse_two_bytes(ability.og_hex_chunk[0:4]),16)
        ability.unknown_text_variable = int(reverse_two_bytes(ability.og_hex_chunk[4:8]),16)
        ability.help_start_index = int(reverse_two_bytes(ability.og_hex_chunk[8:12]),16)
    for monmagic in mon_magic_abilities:
            hex_cut = monmagic.og_hex_chunk[76:76 + 14]
            nth = 2
            hex_list = [hex_cut[i:i + nth] for i in range(0, len(hex_cut), nth)]
            # dmg_info_names = ["MP Cost", "Target", "Calc PS", "Crit", "Hit", "Power"]
            monmagic.dmg_info["MP Cost"] = int(hex_list[0], 16)
            monmagic.dmg_info["Target HP/MP"] = int(hex_list[1], 16)
            monmagic.dmg_info["Calc PS"] = int(hex_list[2], 16)
            monmagic.dmg_info["Crit"] = int(hex_list[3], 16)
            monmagic.dmg_info["Hit"] = int(hex_list[4], 16)
            monmagic.dmg_info["Power"] = int(hex_list[5], 16)
            monmagic.dmg_info["Number of Attacks"] = int(hex_list[6], 16)


def print_dmg_info():
    for ability in global_abilities:
        if ability.type == "Command":
            print(str(ability.id) + "; " + ability.name + "\t " + "TARGET: " + str(
                ability.dmg_info["Target HP/MP"]) + "\t   " +
                  "CALC_PS: " + str(ability.dmg_info["Calc PS"]) + "\t   " + "POWER: " +
                  str(ability.dmg_info["Power"]) + "\t    " + "CRIT: " + str(ability.dmg_info["Crit"]))


set_ability_ap_batch()
set_dmg_info_batch()
test = ""

delete_autoability_indexes = []
change_ap_indexes = []


def replace_ap_with_file_changes():
    with open(resource_path("Test Files/ap_changes.txt"), mode="r") as f:
        for line in f.readlines():
            line_edited = line.strip()
            if len(line_edited) <= 4:
                pass
            else:
                ap_check = line_edited.split(",")
                if ap_check[1] == "DELETE":
                    delete_autoability_indexes.append(ap_check[0])
                else:
                    change_ap_indexes.append(int(ap_check[0]))
                    global_abilities[int(ap_check[0])].ap = int(ap_check[1])


def batch_AP_multiply():
    for ability in global_abilities:
        if isinstance(ability.ap, int) and ability.ap > 0:
            ability.ap = round(ability.ap * 1.75)


replace_ap_with_file_changes()
batch_AP_multiply()


def translate_ability(hex_byte: str):
    hex_byte_reverse = hex_byte[2:4] + hex_byte[0:2]
    hex_byte_reverse = hex_byte_reverse.upper()
    for ability in global_abilities:
        if ability.search_by_id(hex_byte_reverse) != "Not found.":
            return ability.search_by_id(hex_byte_reverse)
        else:
            pass
    return "N/A"


def initiate_dresspheres_new():
    # Initiate dresspheres
    this_dressphere_list = []
    hex_chunks = get_big_chunks()

    for index, job in enumerate(jobs_names):
        new_dressphere = Dressphere(job, index + 1)
        new_dressphere.hex_chunk = hex_chunks[index][16:16 + 232]
        new_dressphere.big_chunk = hex_chunks[index]
        this_dressphere_list.append(new_dressphere)

    for dressphere in this_dressphere_list:
        formulae = parse_chunk(dressphere.hex_chunk)
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        ability_initial_position = 0
        stat_hex_og_string = ""
        for index, stat in enumerate(stat_names):
            stat_hex_og_string = stat_hex_og_string + formulae[index + 1]
            dressphere.stat_variables[stat] = formulae[index + 1]
            ability_initial_position = index + 1
        dressphere.stat_hex_og = stat_hex_og_string
        ability_initial_position = ability_initial_position + 1
        ability_list = formulae[ability_initial_position:len(formulae)]
        ability_hex_og_string = ""
        for i in range(1, len(ability_list)):
            if (i % 2) == 0 or (i == 0):
                pass
            else:
                # ORDER = (Required Ability, Actual Ability)
                ability_hex_og_string = ability_hex_og_string + ability_list[i - 1]
                ability_hex_og_string = ability_hex_og_string + ability_list[i]
                ability_tuple = (ability_list[i - 1], ability_list[i])
                dressphere.abilities.append(ability_tuple)
        dressphere.ability_hex_og = ability_hex_og_string

    return this_dressphere_list


#   RANDOMIZATION OF ABILITIES IN EVERY DRESSPHERE EXCEPT SPECIAL DRESSPHERES
#   "Mask" abilities have problematic hex so those will not be in the ability pool
def shuffle_abilities(dresspheres_list: list[Dressphere], percent_chance_of_branch=50):
    special_jobs = ["super_yuna1", "super-yuna2", "super-yuna3",
                    "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3"]
    dresspheres_edited = dresspheres_list

    valid_abilities = initiate_abilities(valid_ability_pooling=True)
    commands_to_shuffle = valid_abilities[0:250]
    auto_abilities_to_shuffle = valid_abilities[250:len(valid_abilities)]
    random.Random(seed).shuffle(commands_to_shuffle)
    random.Random(seed).shuffle(auto_abilities_to_shuffle)
    seed_increment = 1
    # print("size before: ", len(commands_to_shuffle))
    commands_to_shuffle_repeat = commands_to_shuffle.copy()
    random.Random(seed + 500).shuffle(commands_to_shuffle_repeat)
    delete_autoabilities = []
    for abilityindex in delete_autoability_indexes:
        delete_autoabilities.append(global_abilities[int(abilityindex)].name)

    # Ability tiers
    # tier1_ability_repeats = tier1_abilities.copy()
    # tier2_ability_repeats = tier1_abilities.copy()
    # tier3_ability_repeats = tier1_abilities.copy()

    convert_to_mug = ["Pilfer Gil", "Borrowed Time", "Pilfer HP", "Pilfer MP", "Sticky Fingers", "Master Thief",
                      "Soul Swipe", "Steal Will", "Bribe", "Tantalize", "Bribe", "Silence Mask", "Darkness Mask",
                      "Poison Mask", "Sleep Mask", "Stop Mask", "Petrify Mask"]
    # ignored_abilities = []
    abilities_to_edit = []

    for this_dress in dresspheres_edited:
        if this_dress.dress_name in special_jobs:
            pass
        else:
            this_dress_abilities = []
            activated_abilities = []  # To make sure the ability branching always goes to the root
            output_abilities = [this_dress.abilities[0]]
            if this_dress.dress_name == "whitemage" or this_dress.dress_name == "blackmage":
                output_abilities = [dresspheres_edited[1].abilities[0]]
            # Attempt to make gunner Physical
            # if this_dress.dress_name == "gunner":
            #     output_abilities = [dresspheres_edited[3].abilities[0]]

            root_abilities = []
            mug_flaggu = False
            repeat_flaggu = False
            for i in range(1, 12):
                try:
                    new_command = commands_to_shuffle.pop()
                except IndexError:
                    new_command = commands_to_shuffle_repeat.pop()
                    repeat_flaggu = True
                if new_command.name in convert_to_mug:
                    mug_flaggu = True
                new_command.job = this_dress.dress_name
                this_dress_abilities.append(new_command)
                abilities_to_edit.append(new_command)  # Might be useless

                # Edit global ability flags
                for f_index, flag_search in enumerate(global_abilities):
                    if flag_search.id == new_command.id:
                        global_abilities[f_index].mug_flag = mug_flaggu
                        if repeat_flaggu is True:
                            global_abilities[f_index].repeat_flag = True
                        else:
                            global_abilities[f_index].job = this_dress.dress_name
                mug_flaggu = False

            for i in range(1, 5):
                new_auto_ability = auto_abilities_to_shuffle.pop()
                while new_auto_ability.name in delete_autoabilities:
                    new_auto_ability = auto_abilities_to_shuffle.pop()
                this_dress_abilities.append(new_auto_ability)
            for i, ability in enumerate(this_dress.abilities[1:len(this_dress.abilities)]):
                ability_to_add = ""
                ability_required = "0001"
                if i <= 1:
                    if this_dress_abilities[i].id not in root_abilities:
                        root_abilities.append(this_dress_abilities[i].id)
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                    ability_required = "0000"
                elif i == 2:
                    activated_abilities.append(this_dress_abilities[i].id)
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                    ability_required = "0001"
                elif random.Random(seed + seed_increment).randint(1, 100) > percent_chance_of_branch:
                    if this_dress_abilities[i].id not in activated_abilities:
                        activated_abilities.append(this_dress_abilities[i].id)
                    ability_required = "0001"
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                else:
                    found = False
                    while found is False:
                        index_check = random.Random(seed + seed_increment).randint(0, len(this_dress_abilities) - 1)
                        if (this_dress_abilities[index_check].id in activated_abilities) and (
                                this_dress_abilities[index_check].id not in root_abilities):
                            ability_to_add = this_dress_abilities[i].id
                            ability_required = this_dress_abilities[index_check].id
                            activated_abilities.append(this_dress_abilities[i].id)
                            seed_increment = seed_increment + 1
                            found = True
                        else:
                            seed_increment = seed_increment + 1
                ability_required_reverse = ability_required.lower()[2:4] + ability_required.lower()[0:2]
                ability_to_add_reverse = ability_to_add.lower()[2:4] + ability_to_add.lower()[0:2]
                ability_tuple = (ability_required_reverse, ability_to_add_reverse)
                output_abilities.append(ability_tuple)
                seed_increment = seed_increment + 1
            this_dress.abilities = output_abilities
    # print("CHECKU CHECKU")
    # print("CHECKU CHECKU")

    # for i in dresspheres_edited:
    #     print(i)

    # print("CHECKU CHECKU")
    # print("CHECKU CHECKU")
    # print("size after: " , len(commands_to_shuffle))
    # print(len(auto_abilities_to_shuffle))
    return dresspheres_edited


def randomize_stat_pool(stat_pool_values=list):
    stat_pool = stat_pool_values.copy()
    seed_increment = 1
    for stat_list in stat_pool:
        seed_increment = seed_increment + 1
        random.Random(seed + 55000 + seed_increment).shuffle(stat_list)
    for index, stat_pool_sublist in enumerate(stat_pool):
        seed_increment = seed_increment + 1
        random.Random(seed + seed_increment).shuffle(stat_pool_sublist)
        if index == 0 or index == 1:  # HP / MP
            for jndex, stat_hex in enumerate(stat_pool_sublist):
                var_A = int(stat_hex[0:2], 16) + (random.Random(seed + seed_increment).randint(-5, 5))
                seed_increment = seed_increment + 1
                if var_A > 81:
                    var_A = 81
                if var_A <= 4:
                    var_A = 5

                var_B = int(stat_hex[2:4], 16) + (random.Random(seed + seed_increment).randint(-5, 5))
                seed_increment = seed_increment + 1
                if var_B < 67:
                    var_B = 67
                if var_B > 200:
                    var_B = 200

                var_C = int(stat_hex[4:6], 16) + (random.Random(seed + seed_increment).randint(-50, 50))
                seed_increment = seed_increment + 1
                if var_C > 200:
                    var_C = 200
                if var_C < 50:
                    var_C = 50

                concat_vars = [hex(var_A)[2:4], hex(var_B)[2:4], hex(var_C)[2:4]]
                for ccindex, hex_st in enumerate(concat_vars):
                    if len(hex_st) == 1:
                        concat_vars[ccindex] = "0" + hex_st
                hex_output = concat_vars[0] + concat_vars[1] + concat_vars[2]
                stat_pool[index][jndex] = hex_output
        else:  # All other stats
            for jndex, stat_hex in enumerate(stat_pool_sublist):
                var_A = int(stat_hex[0:2], 16)
                # if var_A < 4:
                #     pass
                # else:
                #     var_A = var_A + (random.Random(seed+seed_increment).randint(-1, 1))
                #     seed_increment = seed_increment + 1
                #     if var_A <= 0:
                #         var_A = 1
                #     if var_A > 24:
                #         var_A = 24
                var_A = round(var_A)

                var_B = int(stat_hex[2:4], 16)
                # var_B = round(var_B)

                var_C = int(stat_hex[4:6], 16) + (random.Random(seed + seed_increment).randint(-30, 30))
                # + (random.Random(seed+seed_increment).randint(-2, 2))
                seed_increment = seed_increment + 1
                if var_C < 1:
                    var_C = 1
                if index == 6:
                    if var_C < 25:
                        var_C = 25
                    if var_C > 61:
                        var_C = 61
                if var_C > 129:
                    var_C = 129
                # if var_C > 30 and (index != 5 or index != 6):
                #      var_C = 55
                # var_C = round(var_C)

                var_D = int(stat_hex[6:8], 16)
                # var_D = round(var_D)

                var_E = int(stat_hex[8:10], 16) + (random.Random(seed + seed_increment).randint(-20, 255))
                seed_increment = seed_increment + 15
                if var_E <= 1:
                    var_E = 1
                if var_E > 254:
                    var_E = 254
                var_E = round(var_E)

                concat_vars = [hex(var_A)[2:4], hex(var_B)[2:4], hex(var_C)[2:4], hex(var_D)[2:4], hex(var_E)[2:4]]
                pass
                for ccindex, hex_st in enumerate(concat_vars):
                    if len(hex_st) == 1:
                        concat_vars[ccindex] = "0" + hex_st
                hex_output = concat_vars[0] + concat_vars[1] + concat_vars[2] + concat_vars[3] + concat_vars[4]
                stat_pool[index][jndex] = hex_output

    return stat_pool


def change_ability_jobs_to_shuffled(dresspheres_list: list[Dressphere], ability_list: list) -> list[Command]:
    effect_animation_start_index = 16
    effect_animation_stop_index = 16 + 8
    attack_motion_start_index = 24
    attack_motion_stop_index = 24 + 2

    sub_menu_action_start_index = 26  # 01 for submenu
    sub_menu_action_stop_index = 26 + 2
    sub_menu_start_index = 28
    sub_menu_stop_index = 28 + 4

    sub_shared_start_index = sub_menu_start_index - 2
    sub_shared_stop_index = sub_menu_stop_index

    belongs_to_job_start_index = 272
    belongs_to_job_stop_index = 272 + 4

    the_0b0b_jobs = ["gunner", "alchemist", "darkknight", "thief", "trainer01", "gambler", "mascot01", "psychic",
                     "festivalist01",
                     "warrior", "samurai", "darkknight", "berserker", "blackmage", "whitemage"]
    the_0c0c_jobs = ["trainer02", "mascot02", "festivalist02", "gunmage", "songstress"]
    the_0d0d_jobs = ["trainer03", "mascot03", "festilvalist03"]
    shared_menu_abilities = ["Swordplay", "Bushido", "Arcana", "Instinct", "Black Magic", "White Magic", "Festivities",
                             "Gunplay", "Fiend Hunter", "Blue Bullet", "Dance",
                             "Sing", "Kupo!", "Wildcat", "Cutlery", "Flimflam", "Gamble", "Kogoro", "Ghiki", "Flurry",
                             "Psionics"]
    dance_abilities = ["Darkness Dance", "Samba of Silence", "MP Mambo", "Magical Masque", "Sleepy Shuffle",
                       "Carnival Cancan",
                       "Slowdance", "Brakedance", "Jitterbug", "Dirty Dancing"]
    edited_abilities = []

    for ability_index, ability in enumerate(ability_list):

        # hex_cut = ability.og_hex_chunk[268:268 + 4]
        # hex_cut = ability.og_hex_chunk[348:348 + 4]

        change_flag = False
        if ability_index in change_ap_indexes:
            change_flag = True
            if ability.type == "Command":
                edited_chunk = ability.og_hex_chunk[0:268] + str(
                    convert_gamevariable_to_reversed_hex(ability.ap, bytecount=2)) + ability.og_hex_chunk[
                                                                                     268 + 4:len(ability.og_hex_chunk)]
                if len(edited_chunk) != len(ability.og_hex_chunk):
                    raise ValueError
                ability.curr_hex_chunk = edited_chunk
            elif ability.type == "Auto-Ability":
                edited_chunk = ability.og_hex_chunk[0:348] + str(
                    convert_gamevariable_to_reversed_hex(ability.ap, bytecount=2)) + ability.og_hex_chunk[
                                                                                     348 + 4:len(ability.og_hex_chunk)]
                ability.curr_hex_chunk = edited_chunk

        if ability.job not in jobs_names or ability.job == "" \
                or ability.type == "Auto-Ability" or ability.name in shared_menu_abilities:
            # 3 swordplay; 4 blm; 5 whm; 6 bushido; 7 arcana, 545 instinct
            if ability_index == 3:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "1b4b3300" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0450" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 4:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "ce467100" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0950" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 5:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "63374f00" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0a50" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 6:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "48474c00" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0550" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 7:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "313f2b00" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0650" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 545:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "50412900" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0750" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            edited_abilities.append(ability)

        else:
            if change_flag == False:
                chunk_edited = ability.og_hex_chunk
            else:
                chunk_edited = ability.curr_hex_chunk
            chunk_length = len(chunk_edited)
            job_hex = ""
            for dress_search in dresspheres_list:
                a = ability.job
                b = dress_search.dress_name
                if a == b:
                    poppy = "yes"
                made_it = "no"
                if dress_search.dress_name == ability.job:
                    job_hex = hex(dress_search.dress_id)
                    made_it = "yas"
                    break
            job_hex_sliced = str(job_hex[2:len(job_hex)])
            useless = "breakpoint"
            if len(job_hex_sliced) == 1:
                job_hex_sliced = "0" + job_hex_sliced
                pass
            checku = ability.job
            if ability.mug_flag == True:
                chunk_edited = chunk_edited[0:attack_motion_start_index] + "03" + chunk_edited[
                                                                                  attack_motion_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:effect_animation_start_index] + "3903390322" + chunk_edited[effect_animation_stop_index + 2:chunk_length]

            if ability.name == "Ultima" or ability.name == "Holy":
                chunk_edited = chunk_edited[0:40] + "56000120" + chunk_edited[40 + 8:chunk_length]
            if ability.name in dance_abilities:
                chunk_edited = chunk_edited[0:attack_motion_start_index] + "03" + chunk_edited[
                                                                                  attack_motion_stop_index:chunk_length]

            if ability.job in the_0b0b_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0b0b" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job in the_0c0c_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0c0c" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job in the_0d0d_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0d0d" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            # if ability.job == "blackmage":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000101" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # if ability.job == "whitemage":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000202" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # # if ability.job == "warrior":
            # #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000606" + chunk_edited[
            # #                                                                    sub_menu_stop_index:chunk_length]
            # #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            # #                                                                                         belongs_to_job_stop_index:chunk_length]
            #
            #
            # if ability.job == "warrior":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000B0B" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            #
            #
            #
            # if ability.job == "samurai":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000808" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # if ability.job == "darkknight":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000909" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # if ability.job == "berserker":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000A0A" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            if ability.name == "Mix":
                chunk_edited = chunk_edited[0:16] + "0000000000090505" + chunk_edited[16 + 16:chunk_length]

            # Swordplay
            if 101 <= ability_index < 113:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000606" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # Black Magic
            if (165 <= ability_index < 177) or ability_index == 369 or ability_index == 368:
                test = ""
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000101" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # White Magic
            if (179 <= ability_index < 191) or ability_index == 370 or ability_index == 371:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000202" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # Instinct
            if 138 < ability_index <= 147:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000A0A" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # Bushido
            if 113 <= ability_index < 125:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000808" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # Arcana
            if (129 <= ability_index < 137) or (376 <= ability_index <= 378):
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000909" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            shared_abi_indexes = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                                  111, 112, 165, 166, 167, 168, 169, 170, 171, 172, 173,
                                  174, 175, 176, 369, 368, 179, 180, 181, 182, 183, 184, 185,
                                  186, 187, 188, 189, 190, 370, 371, 139, 140, 141, 142, 143, 144,
                                  145, 146, 147, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
                                  123, 124, 129, 130, 131, 132, 133, 134, 135, 136, 376, 377, 378]

            if ability.name == "Spare Change":
                chunk_edited = ability.og_hex_chunk
            if ability_index in changed_hit_ids:
                chunk_edited = chunk_edited[0:40] + "4e002060" + chunk_edited[48:chunk_length]
            if (ability.repeat_flag is True) and (ability_index not in shared_abi_indexes):
                chunk_edited = chunk_edited[0:sub_menu_action_start_index] + "010000" + chunk_edited[
                                                                                        sub_menu_action_stop_index + 4:chunk_length]

            if len(chunk_edited) != len(ability.og_hex_chunk):
                raise ValueError
            ability.curr_hex_chunk = chunk_edited
            edited_abilities.append(ability)
    return edited_abilities


def initiate_monsters() -> list[Dressphere]:
    mon_names = []
    these_monsters = []
    with open(resource_path("HPMP.txt"),'r') as HP_MP_File:
        for line in HP_MP_File.readlines():
            split_line = line.split(sep=",")
            mon_names.append(split_line[0])
    chunks = get_big_chunks(segment_type="mon-get")[1:]
    test = ""
    for index, chunk in enumerate(chunks):
        new_monster = Dressphere(mon_names[index],index+6001)
        new_monster.big_chunk = chunk
        new_monster.og_big_chunk = chunk
        formulae = parse_chunk(chunk,mon=True)
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        #ability_initial_position = 0
        stat_hex_og_string = ""
        for jndex, stat in enumerate(stat_names):
            stat_hex_og_string = stat_hex_og_string + formulae[jndex + 1]
            new_monster.stat_variables[stat] = formulae[jndex + 1]
            #ability_initial_position = index + 1
        new_monster.stat_hex_og = stat_hex_og_string
        these_monsters.append(new_monster)
        test =""
    return these_monsters


global_monsters = initiate_monsters()
test =""

# # LV * A/10 + (LV / B) + C - (LV^2) / 16 / D / E
# global_monsters[0].stat_formula(type="STR",tableprint=True)
# global_monsters[0].stat_variables["STR"] = '09050d0C01'
# global_monsters[0].stat_formula(type="STR",tableprint=True)
# # global_monsters[0 ].stat_formula(type="AGL",tableprint=True)
# # global_monsters[15].stat_formula(type="AGL",tableprint=True)
# # global_monsters[21].stat_formula(type="AGL",tableprint=True)
# # global_monsters[21].stat_formula(type="EVA",tableprint=True)
# #'2ba65a' HP
# #'15900a' MP
# #'02160cc804' EVA
# #'021030c804' AGL
# # global_monsters[8].stat_formula(type="EVA",tableprint=True)
# # global_monsters[8].stat_variables["EVA"] = "011601c804"
# # global_monsters[8].stat_formula(type="EVA",tableprint=True)
# #'2ba65a' coyote
# #'bed2b5' omega
# #LV * A + C - (LV^2 / (b/10))
# # (LV * (A/10)) + C - (LV^2 / B) MP
# global_monsters[8].stat_formula(type="MP",tableprint=True)
# global_monsters[8].stat_variables["MP"] = "259032"
# global_monsters[8].stat_formula(type="MP",tableprint=True)


def randomize_monsters():
    start_monster_seed_feed = (seed * seed) + 2056
    start_monster_main_seed = random.Random(start_monster_seed_feed).randint(1,9999999)
    start_monster_increment = random.Random(start_monster_seed_feed).randint(5,20)

    for monster in global_monsters:
        main_stat_names = ["STR", "DEF", "MAG", "MDEF"]
        for stat_name in main_stat_names:
            all_main_stat = "09050F0C01"
            main_var_B = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(1,5))
            start_monster_main_seed += start_monster_increment
            main_var_C = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(1,16))
            start_monster_main_seed += start_monster_increment
            randomized_main_stat = all_main_stat[0:2] + main_var_B + main_var_C + all_main_stat[6:]
            monster.stat_variables[stat_name] = randomized_main_stat
        #Evasion randomization
        evasion_stat = "011601c804"
        eva_var_c = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(1,15))
        start_monster_main_seed += start_monster_increment
        randomized_eva_stat = evasion_stat[0:4] + eva_var_c + evasion_stat[6:]
        monster.stat_variables["EVA"] = randomized_eva_stat
        #Agility randomization
        agility_stat = "000c35c804"
        agi_var_c = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(40, 50))
        start_monster_main_seed += start_monster_increment
        randomized_agi_stat = agility_stat[0:4] + agi_var_c + agility_stat[6:]
        monster.stat_variables["AGL"] = randomized_agi_stat
        #HP randomization
        hp_stat = "2ba65a"
        hp_var_a = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(18, 40))
        start_monster_main_seed += start_monster_increment
        randomized_HP_stat = hp_var_a + hp_stat[2:]
        monster.stat_variables["HP"] = randomized_HP_stat
        #ACC randomization
        acc_stat = "001476c804"
        acc_var_c = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(80, 118))
        start_monster_main_seed += start_monster_increment
        randomized_acc_stat = acc_stat[0:4] + acc_var_c + acc_stat[6:]
        monster.stat_variables["ACC"] = randomized_acc_stat
        #MP randomization
        mp_stat = "2ba65a"
        mp_var_a = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(21, 37))
        start_monster_main_seed += start_monster_increment
        mp_var_c = convert_gamevariable_to_reversed_hex(random.Random(start_monster_main_seed).randint(1, 32))
        start_monster_main_seed += start_monster_increment
        randomized_MP_stat = mp_var_a + mp_stat[2:4] + mp_var_c
        monster.stat_variables["MP"] = randomized_MP_stat

        #Change big chunk
        monster.big_chunk = monster.big_chunk.replace(monster.stat_hex_og, monster.stat_hex)
        monster.big_chunk = "01" + monster.big_chunk[2:]
        if len(monster.big_chunk) != 280:
            raise ValueError

test = ""
randomize_monsters()
test = ""








#0 Sallet
#15 Flan Azul
#42 Zu
#150 Omega
#328 Shinra
#68 Black Elemental
#21 Gecko

# Initialization
dresspheres = initiate_dresspheres_new()
# print(dresspheres[8])
# print(dresspheres[8].hex_chunk)
# print(dresspheres[9])
# print(dresspheres[9].hex_chunk)
# print(dresspheres[7])
# print(dresspheres[7].hex_chunk)
# print(dresspheres[1])
# print(dresspheres[1].hex_chunk)
# print(dresspheres[5])
# print(dresspheres[5].hex_chunk)
global_abilities[3].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[4].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[5].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[6].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[7].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[545].og_hex_chunk = global_abilities[31].og_hex_chunk

# print("_---------------------------")
# print(global_abilities[239].og_hex_chunk)
# print("_---------------------------")
# print("_---------------------------")
# #
# print(dresspheres[7])
# print(dresspheres[7].stat_variables["MAG"])
# #0e 0a 11 12 01
# variable_str = "0e 0a 11 12 01"
# variable_str = variable_str.replace(" ", "")
# dresspheres[7].stat_variables["MAG"] = variable_str
# stat_names = ["STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
# print(dresspheres[0].hex_chunk)
# print(dresspheres[7].abilities)
# print(dresspheres[7].ability_hex)
# #Test change ability
# print(global_abilities[0].id)
# print(dresspheres[7].abilities)
# print(dresspheres[7].ability_hex)
# print(dresspheres[7].ability_hex_og)
# for ability_tuple in dresspheres[7].abilities:
#     print (translate_ability(ability_tuple[1]) + " requires " + translate_ability(ability_tuple[0]))
# print(dresspheres[7].ability_hex)
# print(dresspheres[7].ability_hex_og)
# print(dresspheres[7].stat_variables)

# print(global_abilities[107])
# print(global_abilities[107].og_hex_chunk)

valid_abilities_test = initiate_abilities(valid_ability_pooling=True)

# print(valid_abilities_test)
random_dresspheres_test = initiate_abilities(valid_ability_pooling=True)
# print(dresspheres[7].abilities)
#
# print("$$$$")
# print(randomize_stat_pool(pool_stats(dresspheres)))
#
# print("$$$$")

dresspheres = shuffle_abilities(dresspheres, percent_chance_of_branch=70)
# print("$$$$")
# print("$$$$")
# print("$$$$")
# for dress in dresspheres:
#     print(dress.dress_name)
# print("$$$$")
# print("$$$$")
# print("$$$$")

chunks_output = get_big_chunks(get_all_segments=True)
dress_chunks = []
county = 0
dresspheres = replace_stats(dresspheres, randomize_stat_pool(pool_stats(dresspheres)))

for dress in dresspheres:
    dress.big_chunk = dress.big_chunk.replace(dress.ability_hex_og, dress.ability_hex)
    dress.big_chunk = dress.big_chunk.replace(dress.stat_hex_og, dress.stat_hex)
    dress_chunks.append(dress.big_chunk)

dress_number = len(dress_chunks)

job_bin_string = chunks_output[0]
for chunk in dress_chunks:
    job_bin_string = job_bin_string + chunk
job_bin_string = job_bin_string + chunks_output[2]

#                     with filepath.open(mode="wb") as f:
#                         f.write(binary_converted)
# TEST JOBBIN REPLACE

#
#
changed_ids = []
changed_hit_ids = []
phys_change = []


def change_potencies(ability_list: list[Command]):
    # Change Attack potency from 16 to 10
    for i in range(44, 50):
        ability_list[i].dmg_info["Power"] = 10
        changed_ids.append(i)
    # Make sure thief attacks are less
    ability_list[46].dmg_info["Power"] = 5
    # Trigger Happy Nerf
    ability_list[50].dmg_info["Power"] = 1
    changed_ids.append(50)
    # Nerfs to Cait abilities
    for i in range(251, 255):
        ability_list[i].dmg_info["Hit"] = 45
        ability_list[i].dmg_info["Power"] = 15
        ability_list[i].dmg_info["Crit"] = 25
        changed_ids.append(i)
        changed_hit_ids.append(i)
    # Nerfs to knife abilities
    for i in range(267, 269):
        ability_list[i].dmg_info["Hit"] = 45
        ability_list[i].dmg_info["Cast Time"] = 0
        ability_list[i].dmg_info["Wait Time"] = 83
        phys_change.append(i)
        changed_ids.append(i)
        changed_hit_ids.append(i)
    for i in range(261, 266):
        ability_list[i].dmg_info["Cast Time"] = 0
        ability_list[i].dmg_info["Wait Time"] = 83
        changed_ids.append(i)
        phys_change.append(i)
    # Nerf to Stop Knife
    ability_list[266].dmg_info["Hit"] = 65
    ability_list[266].dmg_info["Cast Time"] = 0
    ability_list[266].dmg_info["Wait Time"] = 80
    phys_change.append(266)
    changed_ids.append(266)
    changed_hit_ids.append(266)
    # Nerf to Quartet Knife
    ability_list[269].dmg_info["MP Cost"] = 35
    ability_list[269].dmg_info["Cast Time"] = 0
    ability_list[269].dmg_info["Wait Time"] = 80
    changed_ids.append(269)
    # Multiple Hit Cactling Gun
    ability_list[270].dmg_info["Power"] = 23
    ability_list[270].dmg_info["Number of Attacks"] = 4
    changed_ids.append(270)
    # Increase to MP cost of Yuna Mascot skills
    for i in range(241, 249):
        if ability_list[270].dmg_info["MP Cost"] > 0:
            ability_list[i].dmg_info["MP Cost"] = ability_list[i].dmg_info["MP Cost"] * 2
            changed_ids.append(i)




    # Nerf magic attack potency. This would be good if not using randomizer
    # ability_list[44].dmg_info["MP Cost"] = 1
    # ability_list[44].dmg_info["Power"] = 5

    # Mug and Nab gil
    for i in range(372, 374):
        ability_list[i].dmg_info["MP Cost"] = 10
        ability_list[i].dmg_info["Power"] = 10
        changed_ids.append(i)
    # Burst Shot
    ability_list[57].dmg_info["Power"] = 12
    changed_ids.append(57)
    # Scattershot/Burst
    ability_list[59].dmg_info["Power"] = 11
    changed_ids.append(59)
    ability_list[60].dmg_info["Power"] = 11
    changed_ids.append(60)
    # Cheapshot
    ability_list[52].dmg_info["Power"] = 8
    changed_ids.append(52)
    # Sparkler
    ability_list[117].dmg_info["Power"] = 12
    changed_ids.append(117)
    # Fireworks
    ability_list[118].dmg_info["Power"] = 12
    changed_ids.append(118)

    # Change ranged attack to Magic-Based
    # ability_list[44].dmg_info["Calc PS"] = 9

    # Attempt to make Bio do damage
    ability_list[133].dmg_info["Calc PS"] = 9
    ability_list[133].dmg_info["Power"] = 11
    ability_list[133].dmg_info["Target HP/MP"] = 1
    changed_ids.append(133)
    # Blind/Silence/Sleep Do Damage
    for i in range(376, 379):
        ability_list[i].dmg_info["Power"] = 12
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Target HP/MP"] = 1
        changed_ids.append(i)
    # Darkness nerf
    ability_list[127].dmg_info["Power"] = 15
    changed_ids.append(127)

    tier1magic_ids = [165, 166, 167, 168]
    tier2magic_ids = [169, 170, 171, 172]
    tier3magic_ids = [173, 174, 175, 176]
    # Change Black Magic Potencies AND to "Special Magic" (based on Physical formula but affected by Magic Defence)
    for i in tier1magic_ids:
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Power"] = 15
        ability_list[i].dmg_info["Cast Time"] = 20
        ability_list[i].dmg_info["Wait Time"] = 55
        phys_change.append(i)
        changed_ids.append(i)
    for i in tier2magic_ids:
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Power"] = 24
        ability_list[i].dmg_info["Wait Time"] = 80
        changed_ids.append(i)
    for i in tier3magic_ids:
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Power"] = 32
        ability_list[i].dmg_info["Cast Time"] = 105
        changed_ids.append(i)
    # Flare
    ability_list[368].dmg_info["Calc PS"] = 9
    ability_list[368].dmg_info["Power"] = 50
    ability_list[368].dmg_info["Cast Time"] = 125
    changed_ids.append(368)
    # Ultima
    ability_list[369].dmg_info["Calc PS"] = 9
    ability_list[369].dmg_info["Power"] = 75
    ability_list[369].dmg_info["Cast Time"] = 100
    ability_list[369].dmg_info["Wait Time"] = 75
    changed_ids.append(369)
    # Holy
    ability_list[370].dmg_info["Calc PS"] = 3
    ability_list[370].dmg_info["Power"] = 3
    ability_list[370].dmg_info["Cast Time"] = 115
    changed_ids.append(370)
    # Excalibur buff
    ability_list[110].dmg_info["Power"] = 50
    ability_list[110].dmg_info["MP Cost"] = 40
    ability_list[110].dmg_info["Cast Time"] = 0
    ability_list[110].dmg_info["Wait Time"] = 80
    phys_change.append(110)
    changed_ids.append(110)
    # Phys attack cast-time changes
    normal_phys_attacks = [81,101,102,103,104,105,106,107,108,109,111,112,113,114,115,116,119,139,140,141,142,143,144,145,146,
        201,202,203,204,205,206,209,211,212,213,214,215,219,221,222,223]
    for i in normal_phys_attacks:
        ability_list[i].dmg_info["Cast Time"] = 0
        ability_list[i].dmg_info["Wait Time"] = 73
        changed_ids.append(i)
        phys_change.append(i)
    # Nerfs to Fiend hunter skills
    for i in range (62,72):
        ability_list[i].dmg_info["Power"] = 10
        ability_list[i].dmg_info["Cast Time"] = 0
        ability_list[i].dmg_info["Wait Time"] = 70
        changed_ids.append(i)
        phys_change.append(i)
    # Psychic bomb
    ability_list[486].dmg_info["Power"] = 8
    ability_list[486].dmg_info["MP Cost"] = 20
    changed_ids.append(486)
    # Excellence
    ability_list[495].dmg_info["MP Cost"] = 40
    changed_ids.append(495)





change_potencies(global_abilities)

# for i in range (0,9):
#     if i % 2 != 0:
#         pass
#     else:
#         num = (dresspheres[0].stat_variables["STR"][i] + dresspheres[0].stat_variables["STR"][i+1]).replace(" ","")
#         num = int(num, 16)
#         print(num)

# print(pool_stats(dresspheres))
# print(len(pool_stats(dresspheres)))
# for pool in pool_stats(dresspheres):
#     print(len(pool))


# for dress in replace_stats(dresspheres,randomize_stat_pool(pool_stats(dresspheres))):
#     dress.stat_formula("MAG", tableprint=True)


# for command in global_abilities:
#     print("************************")
#     print("ability id: " + command.id)
#     print("ability name: " + command.name)
#     print("************************")
#     print("------------------------")


# print(job_bin_string)

# print_jobs_edit = [8,9,11,12,13,14,15,16,17,18,19,20,21,496,497,498,499]
# print("****")
# for i in print_jobs_edit:
#     print(get_big_chunks(segmentType="command")[i])
# print("****")
# print("****")

# for dress in dresspheres:
#     print(dress.dress_name)
#     print(dress.abilities)

# for cmd_search in global_abilities:
#     print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
# print("****")
# print("****")
# print(get_big_chunks(segmentType="command")[235])
# print("****")
# print("****")
# print("Length of og abilities: "+str(len(global_abilities)))


global_abilities = change_ability_jobs_to_shuffled(dresspheres, global_abilities)


decode_dict = {
        '0': '◘', '30': '0', '31': '1', '32': '2', '33': '3', '34': '4', '35': '5', '36': '6', '37': '7', '38': '8',
        '39': '9', '3a': ' ', '3b': '!', '3c': '”', '3d': '#', '3e': '$', '3f': '%', '40': '&', '41': '’', '42': '(',
        '43': ')', '44': '*', '45': '+', '46': ',', '47': '-', '48': '.', '49': '/', '4a': ':', '4b': ';', '4c': '<',
        '4d': '=', '4e': '>', '4f': '?', '50': 'A', '51': 'B', '52': 'C', '53': 'D', '54': 'E', '55': 'F', '56': 'G',
        '57': 'H', '58': 'I', '59': 'J', '5a': 'K', '5b': 'L', '5c': 'M', '5d': 'N', '5e': 'O', '5f': 'P', '60': 'Q',
        '61': 'R', '62': 'S', '63': 'T', '64': 'U', '65': 'V', '66': 'W', '67': 'X', '68': 'Y', '69': 'Z', '6a': '[',
        '6b': '/', '6c': ']', '6d': '^', '6e': '_', '6f': '‘', '70': 'a', '71': 'b', '72': 'c', '73': 'd', '74': 'e',
        '75': 'f', '76': 'g', '77': 'h', '78': 'i', '79': 'j', '7a': 'k', '7b': 'l', '7c': 'm', '7d': 'n', '7e': 'o',
        '7f': 'p', '80': 'q', '81': 'r', '82': 's', '83': 't', '84': 'u', '85': 'v', '86': 'w', '87': 'x', '88': 'y',
        '89': 'z', '8a': '{', '8b': '|', '8c': '}', '8d': '~', '8e': '·', '8f': '【', '90': '】', '91': '♪', '92': '♥',
        '13': '@', 'a': '€','96': '©','b': '®'
    }

encode_dict = {'◘': '00', '0': '30', '1': '31', '2': '32', '3': '33', '4': '34', '5': '35',
               '6': '36', '7': '37', '8': '38', '9': '39', ' ': '3a', '!': '3b', '”': '3c',
               '#': '3d', '$': '3e', '%': '3f', '&': '40', '’': '41', '(': '42', ')': '43',
               '*': '44', '+': '45', ',': '46', '-': '47', '.': '48', '/': '6b', ':': '4a',
               ';': '4b', '<': '4c', '=': '4d', '>': '4e', '?': '4f', 'A': '50', 'B': '51',
               'C': '52', 'D': '53', 'E': '54', 'F': '55', 'G': '56', 'H': '57', 'I': '58',
               'J': '59', 'K': '5a', 'L': '5b', 'M': '5c', 'N': '5d', 'O': '5e', 'P': '5f',
               'Q': '60', 'R': '61', 'S': '62', 'T': '63', 'U': '64', 'V': '65', 'W': '66',
               'X': '67', 'Y': '68', 'Z': '69', '[': '6a', ']': '6c', '^': '6d', '_': '6e',
               '‘': '6f', 'a': '70', 'b': '71', 'c': '72', 'd': '73', 'e': '74', 'f': '75',
               'g': '76', 'h': '77', 'i': '78', 'j': '79', 'k': '7a', 'l': '7b', 'm': '7c',
               'n': '7d', 'o': '7e', 'p': '7f', 'q': '80', 'r': '81', 's': '82', 't': '83',
               'u': '84', 'v': '85', 'w': '86', 'x': '87', 'y': '88', 'z': '89', '{': '8a',
               '|': '8b', '}': '8c', '~': '8d', '·': '8e', '【': '8f', '】': '90', '♪': '91',
               '♥': '92', '@': '13', '€': '0a','©': '96','®': '0b'}


def encode_text(text_value: str):
    encoded_hex_string = ""
    for character in text_value:
        encoded_hex_string = encoded_hex_string + encode_dict[character]
    return encoded_hex_string








def decode_chunk(chunk_text_val: str):
    b = bytearray.fromhex(chunk_text_val)
    chunk_val_list = []
    for byt in b:
        chunk_val_list.append(hex(byt)[2:])

    output_str = ""
    for ind, val in enumerate(chunk_val_list):
        try:
            output_str = output_str + decode_dict[val]
        except KeyError:
            #print (decode_dict[chunk_val_list[ind-5]]+decode_dict[chunk_val_list[ind-4]]+decode_dict[chunk_val_list[ind-3]]+decode_dict[chunk_val_list[ind-2]]+decode_dict[chunk_val_list[ind-1]]+"'"+val+"'"+decode_dict[chunk_val_list[ind+1]]+decode_dict[chunk_val_list[ind+2]]+decode_dict[chunk_val_list[ind+3]]+decode_dict[chunk_val_list[ind+4]]+decode_dict[chunk_val_list[ind+5]]+decode_dict[chunk_val_list[ind+6]])
            #a = input("Press a key to continue")
            output_str = output_str + "•"

    return output_str

ending_chunk_test  = get_big_chunks(get_all_segments=True,segment_type="command")[-1]
c = decode_chunk(ending_chunk_test)

# #Item
# global_abilities[0].new_name_text = "Berries" # +3
# global_abilities[0].new_help_text = "Eat some berries." # +5
# #Gunplay
# global_abilities[8].new_name_text = "Kate Bush"
# #Blue bullet
# global_abilities[10].new_help_text = "Bitchcraft of the witchiest witches in the wild west."
def change_command_text():
    global_abilities[3].new_name_text = "WAR Skills"
    global_abilities[3].new_help_text = "Use job-locked Warrior abilities."
    global_abilities[4].new_name_text = "BLM Skills"
    global_abilities[4].new_help_text = "Use job-locked Black Mage abilities."
    global_abilities[5].new_name_text = "WHM Skills"
    global_abilities[5].new_help_text = "Use job-locked White Mage abilities."
    global_abilities[6].new_name_text = "SAM Skills"
    global_abilities[6].new_help_text = "Use job-locked Samurai abilities."
    global_abilities[7].new_name_text = "DRK Skills"
    global_abilities[7].new_help_text = "Use job-locked Dark Knight abilities."
    global_abilities[545].new_name_text = "BSK Skills"
    global_abilities[545].new_help_text = "Use job-locked Berserker abilities."

# 3 swordplay; 4 blm; 5 whm; 6 bushido; 7 arcana, 545 instinct







def change_command_indexes(index_start: int):
    index_change = index_start
    for ability in global_abilities[0:554]:
        edited_chunk = ability.curr_hex_chunk
        if len(edited_chunk) < 1:
            edited_chunk = ability.og_hex_chunk
        chunk_length = len(edited_chunk)
        ability.name_start_index = ability.name_start_index + index_change
        name_diff = ability.name_new_length - ability.name_og_length
        index_change = index_change + name_diff
        ability.help_start_index = ability.help_start_index + index_change
        help_diff = ability.help_new_length - ability.help_og_length
        index_change = index_change + help_diff
        edited_chunk = convert_gamevariable_to_reversed_hex(ability.name_start_index,bytecount=2) + edited_chunk[4:8] + convert_gamevariable_to_reversed_hex(ability.help_start_index,bytecount=2) + edited_chunk[12:chunk_length]
        ability.curr_hex_chunk = edited_chunk
        if len(ability.curr_hex_chunk) != chunk_length:
            raise ValueError

    test = ""

def write_text_hex():
    output_string = ""
    for ability in global_abilities[0:554]:
        output_string = output_string + encode_text(ability.new_name_text) + "00" + encode_text(ability.new_help_text)+ "00"
    return output_string

change_command_text()
change_command_indexes(0)
output_text_hex = write_text_hex()

#
# FOR POTENCY HEX CHUNK CHANGER
#
#
#

# hex_cut = ability.og_hex_chunk[76:76 + 12]
# nth = 2
# hex_list = [hex_cut[i:i + nth] for i in range(0, len(hex_cut), nth)]
# # dmg_info_names = ["MP Cost", "Target", "Calc PS", "Crit", "Hit", "Power"]
# ability.dmg_info["MP Cost"] = int(hex_list[0], 16)
# ability.dmg_info["Target HP/MP"] = int(hex_list[1], 16)
# ability.dmg_info["Calc PS"] = int(hex_list[2], 16)
# ability.dmg_info["Crit"] = int(hex_list[3], 16)
# ability.dmg_info["Hit"] = int(hex_list[4], 16)
# ability.dmg_info["Power"] = int(hex_list[5], 16)
def write_potencies():
    for i in changed_ids:
        edited_chunk = global_abilities[i].curr_hex_chunk
        if len(edited_chunk) < 1:
            edited_chunk = global_abilities[i].og_hex_chunk
        chunk_length = int(len(edited_chunk))
        initial_pos = 76
        edited_chunk = (edited_chunk[0:initial_pos] + convert_gamevariable_to_reversed_hex(
            global_abilities[i].dmg_info["MP Cost"], bytecount=1)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Target HP/MP"],
                                                               bytecount=1)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Calc PS"], bytecount=1)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Crit"], bytecount=1)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Hit"], bytecount=1)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Power"], bytecount=1)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Number of Attacks"],
                                                               bytecount=1)
                        + edited_chunk[initial_pos + 14:chunk_length])
        castwait_initial_pos = 68
        edited_chunk = (edited_chunk[0:castwait_initial_pos]
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Wait Time"],bytecount=2)
                        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Cast Time"],bytecount=2)
                        + edited_chunk[castwait_initial_pos + 8:chunk_length])

        if len(edited_chunk) != chunk_length:
            raise ValueError
        else:
            global_abilities[i].curr_hex_chunk = edited_chunk


write_potencies()
# print_dmg_info()




# MAKE STRING FOR COMMAND.BIN
commands_shuffle_chunks = get_big_chunks(get_all_segments=True, segment_type="command")
command_string_to_output = commands_shuffle_chunks[0]
for cmd_search in global_abilities:
    # print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
    if cmd_search.type == "Auto-Ability":
        pass
    else:
        if len(cmd_search.curr_hex_chunk) != 280 and len(cmd_search.curr_hex_chunk) != 0:
            # print("AB NOT FOUND:"+ cmd_search.name)
            command_string_to_output = command_string_to_output + cmd_search.og_hex_chunk
        else:
            if len(cmd_search.curr_hex_chunk) == 0 and cmd_search.type != "Auto-Ability":
                # print("NOT IN THE POOL: " + cmd_search.name)
                command_string_to_output = command_string_to_output + cmd_search.og_hex_chunk
            command_string_to_output = command_string_to_output + cmd_search.curr_hex_chunk


# print("middle chunk: "+str(len(command_string_to_output)-64))
#command_string_to_output = command_string_to_output + commands_shuffle_chunks[2]
command_string_to_output = command_string_to_output + output_text_hex




# MAKE STRING FOR A_ABILITY.BIN
aa_shuffle_chunks = get_big_chunks(get_all_segments=True, segment_type="auto-ability")
aa_string_to_output = aa_shuffle_chunks[0]
for cmd_search in global_abilities:
    # print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
    if cmd_search.type == "Command":
        pass
    else:
        if len(cmd_search.curr_hex_chunk) != 352 and len(cmd_search.curr_hex_chunk) != 0:
            # print("AB NOT FOUND:"+ cmd_search.name)
            aa_string_to_output = aa_string_to_output + cmd_search.og_hex_chunk
        else:
            if len(cmd_search.curr_hex_chunk) == 0 and cmd_search.type != "Command":
                # print("NOT IN THE POOL: " + cmd_search.name)
                aa_string_to_output = aa_string_to_output + cmd_search.og_hex_chunk
            aa_string_to_output = aa_string_to_output + cmd_search.curr_hex_chunk
aa_string_to_output = aa_string_to_output + aa_shuffle_chunks[2]

# print("ending chunk: " + str(len(commands_shuffle_chunks[2])))
# print("all chunk: "+str(len(command_string_to_output)))
#
# print(command_string_to_output)
# print(global_abilities[88].og_hex_chunk)
# print(global_abilities[88].og_hex_chunk)

# for command in global_abilities:
#     print("************************")
#     print("ability id: " + command.id)
#     print("ability name: " + command.name)
#     print("************************")
#     print("------------------------")
# print(dresspheres[0].stat_formula(type="STR",tableprint=True))
# print(dresspheres[26].stat_formula(type="ACC",tableprint=True))
# print("****")


# Special characters
# 13 39 = Yuna Pet (Kogoro)          @9
# 13 3A = Rikku Pet (Ghiki)          @ (Space)
# 13 3B = Paine Pet (Flurry)         @!
# 0A 88 = Blue text                  €y (before word to be Blue'd); €’ (after text to end Blue)
# 96 = Summon ability help text?     ©
# 0B 33 = R1 button                  ®3



#mon-get string

mon_get_string = get_big_chunks(get_all_segments=True,segment_type="mon-get")[0]
for monster in global_monsters:
    mon_get_string = mon_get_string + monster.big_chunk




def execute_randomizer(reset_bins=False):
    os_prefix = os.getcwd()
    directory_name = str(seed)
    if reset_bins is True:
        directory_name = "reset"
    directory_path = os_prefix + "/" + directory_name + "/ffx_ps2/ffx2/master/new_uspc/battle/kernel"
    try:
        os.makedirs(directory_path)
    except FileExistsError:
        pass
    test = ""
    output_jobbin_path = pathlib.PureWindowsPath(directory_path + "\job.bin")
    test = ""
    output_cmdbin_path = pathlib.PureWindowsPath(directory_path + "/command.bin")
    output_aabin_path = pathlib.PureWindowsPath(directory_path + "/a_ability.bin")
    output_monget_path = pathlib.PureWindowsPath(directory_path + "/mon_get.bin")

    if reset_bins is True:
        binary_converted_jobbin = binascii.unhexlify(job_bin_to_hex())
        binary_converted_cmdbin = binascii.unhexlify(cmd_bin_to_hex())
        binary_converted_aabin = binascii.unhexlify(auto_bin_to_hex())
        binary_converted_mgetbin = binascii.unhexlify(monget_bin_to_hex())
    else:
        binary_converted_jobbin = binascii.unhexlify(job_bin_string)
        binary_converted_cmdbin = binascii.unhexlify(command_string_to_output)
        binary_converted_aabin = binascii.unhexlify(aa_string_to_output)
        binary_converted_mgetbin = binascii.unhexlify(mon_get_string)


    with open(output_jobbin_path, 'wb') as f:
        f.write(binary_converted_jobbin)
    with open(output_cmdbin_path, 'wb') as f:
        f.write(binary_converted_cmdbin)
    with open(output_aabin_path, 'wb') as f:
        f.write(binary_converted_aabin)
    # with open(output_monget_path, 'wb') as f:
    #     f.write(binary_converted_mgetbin)
    print("Files written successfully!")


# print("--- Completed in %s seconds ---" % (time.time() - start_time))


# for dress in dresspheres:
#     print(dress.dress_name)
#     print(dress.big_chunk)

# big_chunky = test_randomize_big_chunks(4)
# print_str=big_chunky[0]
# for i, x in enumerate(big_chunky[1]):
#     print(i)
#     print_str = print_str + x
# print_str= print_str + big_chunky[2]
# print(print_str)
# print(len(print_str))

# total = 248
# job_number = len(jobs_names) - 9
# job_ability_each = 11
# print("Job number: " + str(job_number))
# print("Job ability each: " + str(job_ability_each))
# print("tier1: " + str(len(tier1_abilities)) + "   %: " + str(len(tier1_abilities)/248) + "   No.: "
#       + str((len(tier1_abilities)/248)*job_ability_each))
# print("tier2: " + str(len(tier2_abilities)) + "   %: " + str(len(tier2_abilities)/248) + "   No.: "
#       + str((len(tier2_abilities)/248)*job_ability_each))
# print("tier3: " + str(len(tier3_abilities)) + "   %: " + str(len(tier3_abilities)/248) + "   No.: "
#       + str((len(tier3_abilities)/248)*job_ability_each))
