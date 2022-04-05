from dressphere import Dressphere
import pathlib
import time
import random
from command import Command
from services import *

start_time = time.time()
#INPUT VARIABLES
job_bin_path = "Test Files/job.bin"
cmd_bin_path = "Test Files/command.bin"
jobs_names = [
    "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku2", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02", "trainer03", "mascot02",
    "mascot03", "psychic", "festivalist01", "festivalist02", "festilvalist03"
    ]
#previous seed: 111876967976853241
seed = 14749849


def job_bin_to_hex():
    job_bin = pathlib.Path(job_bin_path)
    hex_data = read_hex(job_bin)
    return hex_data

def cmd_bin_to_hex():
    cmd_bin = pathlib.Path(cmd_bin_path)
    hex_data = read_hex(cmd_bin)
    return hex_data

#####RANDOMIZE STUFF####
def get_big_chunks(get_all_segments=False, segmentType="job"):
    chunks = []
    hex_file = ""
    if segmentType == "job":
        hex_file = job_bin_to_hex()
        initial_position = 520
        next_position = 976
    elif segmentType == "command":
        hex_file = cmd_bin_to_hex()
        initial_position = 64
        next_position = 64 + 280
    start_chunk = hex_file[initial_position:next_position]
    chunks.append(start_chunk)
    ending_chunk = ""
    if segmentType == "command":
        for i in range(0, 553):
            initial_position = next_position
            next_position = next_position + 280
            chunks.append(hex_file[initial_position:next_position])
            if i == 552 and get_all_segments == True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segmentType == "job":
        for i in range (0,30):
            initial_position = next_position
            next_position = next_position + 456
            chunks.append(hex_file[initial_position:next_position])
            useless = ""
            if i == 29 and get_all_segments == True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    if get_all_segments == True:
        beginning_chunk = hex_file[0:520]
        if segmentType=="command":
            beginning_chunk = hex_file[0:64]
            return [beginning_chunk, chunks, ending_chunk]
        return [beginning_chunk,chunks,ending_chunk]
    else:
        return chunks


def test_randomize_big_chunks(seed: int):
    chunks = get_big_chunks(get_all_segments=True)
    random.Random(seed).shuffle(chunks[1])
    return chunks

#####RANDOMIZE STUFF ABOVE####
##############################

def cut_command_names(valid_abilities=False):
    command_ids = []
    filename = "Test Files/commands.txt"
    if valid_abilities == True:
        filename = "Test Files/valid_commands.txt"
    with open(filename, "r") as f:
        for line in f.readlines():
            id = line[32:36]
            name = line[46:len(line)]
            name = name[:name.find("\"")]
            tupl = (id,name)
            command_ids.append(tupl)
    return command_ids


def cut_autoability_names():
    autoability_ids = []
    with open("Test Files/auto_abilities.txt", "r") as f:
        for line in f.readlines():
            id = line[36:40]
            name = line[50:len(line)]
            name = name[:name.find("\"")]
            tupl = (id,name)
            autoability_ids.append(tupl)
    return autoability_ids

command_global_chunks = get_big_chunks(segmentType="command")


#Initiates the list of abilities
#valid_ability_pooling is an argument for shuffle_abilities() that returns only abilities that are intended to be shuffled
def initiate_abilities(valid_ability_pooling=False):
    abilities = []
    if valid_ability_pooling == True:
        valid_ability_tuples = cut_command_names(valid_abilities=True)
    else:
        command_tuples = cut_command_names()
        autoability_tuples = cut_autoability_names()
    if valid_ability_pooling == True:
        for ability in valid_ability_tuples:
            if int(ability[0],16) <= 12841:
                cmd = Command(id_value=ability[0], name_value=ability[1], type_value="Command")
                print(cmd)
                abilities.append(cmd)
            else:
                auto = Command(id_value=ability[0].upper(), name_value=ability[1], type_value="Auto-Ability")
                abilities.append(auto)
    else:
        for chunkindex, command in enumerate(command_tuples):
            cmd = Command(id_value=command[0],name_value=command[1],type_value="Command")
            cmd.og_hex_chunk = command_global_chunks[chunkindex]
            abilities.append(cmd)
        for autoability in autoability_tuples:
            auto = Command(id_value=autoability[0].upper(),name_value=autoability[1],type_value="Auto-Ability")
            abilities.append(auto)
    return abilities


global_abilities = initiate_abilities()


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
    dresspheres = []
    hex_chunks = get_big_chunks()

    for index, job in enumerate(jobs_names):
        new_dressphere = Dressphere(job, index + 1)
        new_dressphere.hex_chunk = hex_chunks[index][16:16+232]
        new_dressphere.big_chunk = hex_chunks[index]
        dresspheres.append(new_dressphere)



    for dressphere in dresspheres:
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
        for i in range (1, len(ability_list)):
            if (i % 2) == 0 or (i==0):
                pass
            else:
                # ORDER = (Required Ability, Actual Ability)
                ability_hex_og_string = ability_hex_og_string + ability_list[i - 1]
                ability_hex_og_string = ability_hex_og_string + ability_list[i]
                ability_tuple = (ability_list[i - 1], ability_list[i])
                dressphere.abilities.append(ability_tuple)
        dressphere.ability_hex_og = ability_hex_og_string

    return dresspheres


#   RANDOMIZATION OF ABILITIES IN EVERY DRESSPHERE EXCEPT SPECIAL DRESSPHERES
#   "Mask" abilities have problematic hex so those will not be in the ability pool
def shuffle_abilities(dresspheres: list[Dressphere], percent_chance_of_branch=50):
    special_jobs = ["super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3"]
    dresspheres_edited = dresspheres

    no_ap_abilities =[]

    valid_abilities = initiate_abilities(valid_ability_pooling=True)
    commands_to_shuffle = valid_abilities[0:257]
    auto_abilities_to_shuffle = valid_abilities[257:len(valid_abilities)]
    random.Random(seed).shuffle(commands_to_shuffle)
    random.Random(seed).shuffle(auto_abilities_to_shuffle)
    seed_increment = 1
    print("size before: ", len(commands_to_shuffle))


    convert_to_mug = ["Pilfer Gil","Borrowed Time","Pilfer HP","Pilfer MP","Sticky Fingers","Master Thief","Soul Swipe","Steal Will","Flee","Tantalize","Bribe","Silence Mask","Darkness Mask",
                      "Poison Mask", "Sleep Mask", "Stop Mask", "Petrify Mask"]
    abilities_to_edit = []

    for dress in dresspheres_edited:
        if dress.dress_name in special_jobs:
            pass
        else:
            this_dress_abilities = []
            activated_abilities = [] #To make sure the ability branching always goes to the root
            output_abilities = [dress.abilities[0]]
            root_abilities = []
            mug_flaggu = False
            for i in range(1,12):
                new_command = commands_to_shuffle.pop()
                if new_command.name in convert_to_mug:
                    mug_flaggu = True
                new_command.job = dress.dress_name
                this_dress_abilities.append(new_command)
                abilities_to_edit.append(new_command) #Might be useless

                #Edit global ability flags
                for f_index, flag_search in enumerate(global_abilities):
                    if flag_search.id == new_command.id:
                        global_abilities[f_index].mug_flag = mug_flaggu
                        global_abilities[f_index].job = dress.dress_name


            for i in range(1,5):
                new_auto_ability = auto_abilities_to_shuffle.pop()
                this_dress_abilities.append(new_auto_ability)
            for i, ability in enumerate(dress.abilities[1:len(dress.abilities)]):
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
                elif random.Random(seed+seed_increment).randint(1, 100) > percent_chance_of_branch:
                    if this_dress_abilities[i].id not in activated_abilities:
                        activated_abilities.append(this_dress_abilities[i].id)
                    ability_required = "0001"
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                else:
                    found = False
                    while(found == False):
                        index_check = random.Random(seed+seed_increment).randint(0, len(this_dress_abilities)-1)
                        if (this_dress_abilities[index_check].id in activated_abilities) and (this_dress_abilities[index_check].id not in root_abilities) :
                            ability_to_add = this_dress_abilities[i].id
                            ability_required = this_dress_abilities[index_check].id
                            activated_abilities.append(this_dress_abilities[i].id)
                            seed_increment = seed_increment + 1
                            found=True
                        else:
                            seed_increment = seed_increment + 1
                ability_required_reverse = ability_required.lower()[2:4] + ability_required.lower()[0:2]
                ability_to_add_reverse = ability_to_add.lower()[2:4] + ability_to_add.lower()[0:2]
                ability_tuple = (ability_required_reverse, ability_to_add_reverse)
                output_abilities.append(ability_tuple)
                seed_increment = seed_increment + 1
            dress.abilities = output_abilities
    print("CHECKU CHECKU")
    print("CHECKU CHECKU")

    for i in dresspheres_edited:
        print(i)

    print("CHECKU CHECKU")
    print("CHECKU CHECKU")
    print("size after: " , len(commands_to_shuffle))
    print(len(auto_abilities_to_shuffle))
    return dresspheres_edited

def randomize_stat_pool(stat_pool_values = list):
    stat_pool = stat_pool_values
    seed_increment = 1
    for index, stat_pool_sublist in enumerate(stat_pool):
        random.Random(seed).shuffle(stat_pool_sublist)
        if index == 0 or index == 1:    # HP / MP
            for jndex, stat_hex in enumerate(stat_pool_sublist):
                var_A = int(stat_hex[0:2], 16) + ( random.Random(seed).randint(-5, 5) )
                seed_increment = seed_increment + 1
                if var_A > 81:
                    var_A = 81
                if var_A <= 4:
                    var_A = 5

                var_B = int(stat_hex[2:4], 16) + (random.Random(seed).randint(-5, 5))
                seed_increment = seed_increment + 1
                if var_B < 67:
                    var_B = 67
                if var_B > 200:
                    var_B = 200


                var_C = int(stat_hex[4:6], 16) + (random.Random(seed).randint(-50, 50))
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

        else:   # All other stats
            for jndex, stat_hex in enumerate(stat_pool_sublist):
                var_A = int(stat_hex[0:2], 16)
                if var_A < 4:
                    pass
                else:
                    var_A = var_A + (random.Random(seed).randint(-2, 2))
                    seed_increment = seed_increment + 1
                    if var_A <= 0:
                        var_A = 1
                    if var_A > 24:
                        var_A = 24
                var_A = round(var_A)

                var_B = int(stat_hex[2:4], 16)
                #var_B = round(var_B)

                var_C = int(stat_hex[4:6], 16)
                # + (random.Random(seed+seed_increment).randint(-2, 2))
                # seed_increment = seed_increment + 1
                # if var_C < 1:
                #     var_C = 1
                # if var_C > 30:
                #     var_C = 30
                # var_C = round(var_C)


                var_D = int(stat_hex[6:8], 16)
                #var_D = round(var_D)

                var_E = int(stat_hex[8:10], 16) + (random.Random(seed+seed_increment).randint(5, 100))
                seed_increment = seed_increment + 1
                if var_E <= 0:
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


def change_ability_jobs_to_shuffled(dresspheres: list[Dressphere],ability_list: list):
    attack_motion_start_index = 24
    attack_motion_stop_index = 24+2
    sub_menu_action_start_index = 26     #00 for non-submenu
    sub_menu_action_start_index = 26+2
    sub_menu_start_index = 28
    sub_menu_stop_index = 28+4

    sub_shared_start_index = sub_menu_start_index-2
    sub_shared_stop_index = sub_menu_stop_index

    belongs_to_job_start_index = 272
    belongs_to_job_stop_index = 272+4

    # "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    # "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    # "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02", "trainer03", "mascot02",
    # "mascot03", "psychic", "festivalist01", "festivalist02", "festilvalist03"

    the_0b0b_jobs = ["gunner", "gunmage","alchemist","darkknight","songstress", "thief", "trainer01", "gambler", "mascot01", "psychic", "festivalist01"]
    the_0c0c_jobs = ["trainer02", "mascot02", "festivalist02"]
    the_0d0d_jobs = ["trainer03","mascot03", "festilvalist03"]
    shared_menu_abilities = ["Swordplay","Bushido","Arcana", "Instinct", "Black Magic", "White Magic","Festivities","Gunplay","Fiend Hunter","Blue Bullet","Dance",
                             "Sing","Kupo!","Wildcat","Cutlery","Flimflam","Gamble", "Kogoro" ,"Ghiki","Flurry", "Psionics"]
    edited_abilities = []
    pass

    for ability_index, ability in enumerate(ability_list):

        if ability.job not in jobs_names or ability.job == "" or ability.type == "Auto-Ability" or ability.name in shared_menu_abilities:
            edited_abilities.append(ability)
        else:
            chunk_edited = ability.og_hex_chunk
            chunk_length = len(chunk_edited)
            job_hex = ""
            for dress_search in dresspheres:
                a = ability.job
                b = dress_search.dress_name
                if a == b:
                    poppy = "yes"
                made_it="no"
                if dress_search.dress_name == ability.job:
                    job_hex = hex(dress_search.dress_id)
                    made_it="yas"
                    break
            job_hex_sliced = str(job_hex[2:len(job_hex)])
            useless = "breakpoint"
            if len(job_hex_sliced) == 1:
                job_hex_sliced = "0" + job_hex_sliced
                pass
            checku = ability.job
            if ability.mug_flag == True:
                chunk_edited = chunk_edited[0:attack_motion_start_index] + "00" + chunk_edited[attack_motion_stop_index:chunk_length]
            if ability.job in the_0b0b_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0b0b" + chunk_edited[sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[belongs_to_job_stop_index:chunk_length]
            if ability.job in the_0c0c_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0c0c" + chunk_edited[sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job in the_0d0d_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0d0d" + chunk_edited[sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job == "blackmage":
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000101" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job == "whitemage":
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000202" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job == "warrior":
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000606" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job == "samurai":
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000808" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job == "darkknight":
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000808" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job == "berserker":
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000A0A" + chunk_edited[
                                                                               sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]

            if len(chunk_edited) != len(ability.og_hex_chunk):
                print("Raise Alarum for: "+ability.name)
                alarum = "bitch"
            ability.curr_hex_chunk = chunk_edited
            edited_abilities.append(ability)
    return edited_abilities









#Initialization
dresspheres = initiate_dresspheres_new()
print("_---------------------------")
print(global_abilities[46].og_hex_chunk)
print("_---------------------------")
print("_---------------------------")

print(dresspheres[7])
print(dresspheres[7].stat_variables["MAG"])
#0e 0a 11 12 01
variable_str = "0e 0a 11 12 01"
variable_str = variable_str.replace(" ", "")
dresspheres[7].stat_variables["MAG"] = variable_str
stat_names = ["STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
print(dresspheres[0].hex_chunk)
print(dresspheres[7].abilities)
print(dresspheres[7].ability_hex)
#Test change ability
print(global_abilities[0].id)
print(dresspheres[7].abilities)
print(dresspheres[7].ability_hex)
print(dresspheres[7].ability_hex_og)
for ability_tuple in dresspheres[7].abilities:
    print (translate_ability(ability_tuple[1]) + " requires " + translate_ability(ability_tuple[0]))
print(dresspheres[7].ability_hex)
print(dresspheres[7].ability_hex_og)
print(dresspheres[7].stat_variables)



valid_abilities_test = initiate_abilities(valid_ability_pooling=True)

print(valid_abilities_test)
random_dresspheres_test = initiate_abilities(valid_ability_pooling=True)
print(dresspheres[7].abilities)

print("$$$$")
print(randomize_stat_pool(pool_stats(dresspheres)))

print("$$$$")

dresspheres = shuffle_abilities(dresspheres,percent_chance_of_branch=70)
print("$$$$")
print("$$$$")
print("$$$$")
for dress in dresspheres:
    print(dress.dress_name)
print("$$$$")
print("$$$$")
print("$$$$")

chunks_output = get_big_chunks(get_all_segments=True)
dress_chunks = []
county = 0
dresspheres = replace_stats(dresspheres,randomize_stat_pool(pool_stats(dresspheres)))


for dress in dresspheres:

    dress.big_chunk = dress.big_chunk.replace(dress.ability_hex_og, dress.ability_hex)
    dress.big_chunk = dress.big_chunk.replace(dress.stat_hex_og, dress.stat_hex)
    dress_chunks.append(dress.big_chunk)

dress_number = len(dress_chunks)

job_bin_string = chunks_output[0]
for chunk in dress_chunks:
    job_bin_string = job_bin_string + chunk
job_bin_string = job_bin_string + chunks_output[2]


#TEST JOBBIN REPLACE


print(dresspheres[0].abilities)
print(dresspheres[0].stat_variables["STR"])
for i in range (0,9):
    if i % 2 != 0:
        pass
    else:
        num = (dresspheres[0].stat_variables["STR"][i] + dresspheres[0].stat_variables["STR"][i+1]).replace(" ","")
        num = int(num, 16)
        print(num)

# print(pool_stats(dresspheres))
# print(len(pool_stats(dresspheres)))
# for pool in pool_stats(dresspheres):
#     print(len(pool))




for dress in replace_stats(dresspheres,randomize_stat_pool(pool_stats(dresspheres))):
    dress.stat_formula("MAG", tableprint=True)



# for command in global_abilities:
#     print("************************")
#     print("ability id: " + command.id)
#     print("ability name: " + command.name)
#     print("************************")
#     print("------------------------")


print(job_bin_string)

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


global_abilities = change_ability_jobs_to_shuffled(dresspheres,global_abilities)



print("Length of new abilities: "+str(len(global_abilities)))

print("****")
print("****")
print("START")
#MAKE STRING FOR COMMAND.BIN
commands_shuffle_chunks = get_big_chunks(get_all_segments=True,segmentType="command")
command_string_to_output = commands_shuffle_chunks[0]
print("beg chunk: "+str(len(command_string_to_output)))
for cmd_search in global_abilities:
    # print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
    if len(cmd_search.curr_hex_chunk) != 280 and len(cmd_search.curr_hex_chunk) != 0:
        # print("AB NOT FOUND:"+ cmd_search.name)
        command_string_to_output = command_string_to_output + cmd_search.og_hex_chunk
    else:
        if len(cmd_search.curr_hex_chunk) == 0 and cmd_search.type != "Auto-Ability":
            # print("NOT IN THE POOL: " + cmd_search.name)
            command_string_to_output = command_string_to_output + cmd_search.og_hex_chunk
        command_string_to_output = command_string_to_output + cmd_search.curr_hex_chunk



print("middle chunk: "+str(len(command_string_to_output)-64))
command_string_to_output = command_string_to_output + commands_shuffle_chunks[2]
print("ending chunk: " + str(len(commands_shuffle_chunks[2])))
print("all chunk: "+str(len(command_string_to_output)))

print(command_string_to_output)

# for command in global_abilities:
#     print("************************")
#     print("ability id: " + command.id)
#     print("ability name: " + command.name)
#     print("************************")
#     print("------------------------")

print("****")
print("--- Completed in %s seconds ---" % (time.time() - start_time))


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
