from dressphere import Dressphere
import pathlib
import time
import random
from command import Command

start_time = time.time()
#INPUT VARIABLES
job_bin_path = "Test Files/job.bin"
jobs_names = [
    "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02", "trainer03", "mascot02",
    "mascot03", "psychic", "festivalist01", "festivalist02", "festilvalist03"
    ]


def read_hex(path):
    with path.open(mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data

def job_bin_to_hex():
    job_bin = pathlib.Path(job_bin_path)
    hex_data = read_hex(job_bin)
    return hex_data


#####RANDOMIZE STUFF####
def get_big_chunks(get_all_segments=False):
    chunks = []
    hex_file = job_bin_to_hex()
    initial_position = 520
    next_position = 976
    start_chunk = hex_file[initial_position:next_position]
    chunks.append(start_chunk)
    ending_chunk = ""
    for i in range (1,31):
        initial_position = next_position
        next_position = next_position + 456
        chunks.append(hex_file[initial_position:next_position])
        if i == 30 and get_all_segments == True:
            ending_chunk = hex_file[next_position:len(hex_file)]
    if get_all_segments == True:
        beginning_chunk = hex_file[0:520]
        return [beginning_chunk,chunks,ending_chunk]
    else:
        return chunks

def test_randomize_big_chunks(seed: int):
    chunks = get_big_chunks(get_all_segments=True)
    random.Random(seed).shuffle(chunks[1])
    return chunks

#####RANDOMIZE STUFF ABOVE####
##############################

def cut_command_names():
    command_ids = []
    with open("Test Files/commands.txt", "r") as f:
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


def find_chunk(id_input: int, hex_file_data: str, problematic_id=0):

    id = hex(id_input)[2:]
    unique_ids = []
    if len(id) == 1:
        id = "0" + id
    if problematic_id != 0:
        if problematic_id==23:
            class_line = "1a5c"
            position = hex_file_data.find(class_line) - 4
        elif problematic_id==24:
            class_line = "1b5c"
            position = hex_file_data.find(class_line) - 4
        elif problematic_id==25:
            class_line = "1c5e"
            position = hex_file_data.find(class_line) - 4
        elif problematic_id==26:
            class_line = "1d5e"
            position = hex_file_data.find(class_line) - 4
        else:
            adjacent_to_id = hex(id_input+80)[2:]
            class_line = id + str(adjacent_to_id)
            position = hex_file_data.find(class_line)-4
    else:
        class_line = "ff00" + id
        position = hex_file_data.find(class_line)
    if position == "-1":
        return "Index position not found."
    else:
        return hex_file_data[position:position+232] #Returns everything up until after Abilities (including abilities)

def parse_chunk(chunk: str):
    if chunk == "Index position not found." or len(chunk) != 232:
        return "Error"
    else:
        seperated_chunks = []
        default_attack = chunk[8:12]
        seperated_chunks.append(default_attack)
        hp_mp_length = 6
        stat_length = 10
        ability_length = 4
        initial_position = 12
        for i in range(1,11):
            if i < 3:
                seperated_chunks.append(chunk[initial_position:initial_position+hp_mp_length])
                initial_position = initial_position+ hp_mp_length
            else:
                seperated_chunks.append(chunk[initial_position:initial_position + stat_length])
                initial_position = initial_position + stat_length
        for i in range (1,33):
            seperated_chunks.append(chunk[initial_position:initial_position + ability_length])
            initial_position = initial_position + ability_length
        return seperated_chunks




def initiate_abilities():
    command_tuples = cut_command_names()
    autoability_tuples = cut_autoability_names()
    abilities = []
    for command in command_tuples:
        cmd = Command(id_value=command[0],name_value=command[1],type_value="Command")
        abilities.append(cmd)
    for autoability in autoability_tuples:
        auto = Command(id_value=autoability[0].upper(),name_value=autoability[1],type_value="Auto-Ability")
        abilities.append(auto)
    return abilities


abilities = initiate_abilities()


def translate_ability(hex_byte: str):
    hex_byte_reverse = hex_byte[2:4] + hex_byte[0:2]
    hex_byte_reverse = hex_byte_reverse.upper()
    for ability in abilities:
        if ability.search_by_id(hex_byte_reverse) != "Not found.":
            return ability.search_by_id(hex_byte_reverse)
        else:
            pass
    return "N/A"


#Unused
def initiate_dresspheres_legacy():
    # Get the job file string
    hex_string = job_bin_to_hex()

    # Initiate dresspheres
    dresspheres = []
    for index, job in enumerate(jobs_names):
        problematic_ids = [12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

        if index + 1 not in problematic_ids:
            new_dressphere = Dressphere(job, index + 1)
            new_dressphere.hex_chunk = find_chunk(index + 1, hex_string)
            dresspheres.append(new_dressphere)

        # Trainer01
        if index + 1 == 12:
            new_dressphere = Dressphere(job, index + 1)
            new_dressphere.hex_chunk = find_chunk(index + 1, hex_string, problematic_id=12)
            dresspheres.append(new_dressphere)
        # Mascot01
        if index + 1 == 14:
            new_dressphere = Dressphere(job, index + 1)
            new_dressphere.hex_chunk = find_chunk(index + 1, hex_string, problematic_id=14)
            dresspheres.append(new_dressphere)
        # Trainer02and03
        if index + 1 == 23 or index + 1 == 24 or index + 1 == 25 or index + 1 == 26:
            new_dressphere = Dressphere(job, index + 1)
            new_dressphere.hex_chunk = find_chunk(index + 1, hex_string, problematic_id=index + 1)
            dresspheres.append(new_dressphere)

    # Add formulae to dresspheres
    for dressphere in dresspheres:
        formulae = parse_chunk(dressphere.hex_chunk)
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        ability_initial_position = 0
        for index, stat in enumerate(stat_names):
            dressphere.stat_variables[stat] = formulae[index + 1]
            ability_initial_position = index + 1
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

def initiate_dresspheres_new():
    # Initiate dresspheres
    dresspheres = []
    hex_chunks = get_big_chunks()

    for index, job in enumerate(jobs_names):
        new_dressphere = Dressphere(job, index + 1)
        new_dressphere.hex_chunk = hex_chunks[index][16:16+232]
        dresspheres.append(new_dressphere)

    for dressphere in dresspheres:
        formulae = parse_chunk(dressphere.hex_chunk)
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        ability_initial_position = 0
        for index, stat in enumerate(stat_names):
            dressphere.stat_variables[stat] = formulae[index + 1]
            ability_initial_position = index + 1
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



#Initialization
dresspheres = initiate_dresspheres_new()

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
print(abilities[0].id)
print(dresspheres[7].abilities)
print(dresspheres[7].ability_hex)
print(dresspheres[7].ability_hex_og)
for ability_tuple in dresspheres[7].abilities:
    print (translate_ability(ability_tuple[1]) + " requires " + translate_ability(ability_tuple[0]))
dresspheres[7].change_ability(0,abilities[0].id)
dresspheres[7].change_required_ability(0,abilities[11].id)
print(dresspheres[7].ability_hex)
print(dresspheres[7].ability_hex_og)
print(dresspheres[7].stat_variables)




for dress in initiate_dresspheres_new():
    print(dress)
    for ability in dress.abilities:
        print(translate_ability(ability[1]))
print("--- Completed in %s seconds ---" % (time.time() - start_time))




# big_chunky = test_randomize_big_chunks(4)
# print_str=big_chunky[0]
# for i, x in enumerate(big_chunky[1]):
#     print(i)
#     print_str = print_str + x
# print_str= print_str + big_chunky[2]
# print(print_str)
# print(len(print_str))
