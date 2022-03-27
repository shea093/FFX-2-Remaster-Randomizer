from dressphere import Dressphere
import pathlib


#INPUT VARIABLES
job_bin_path = "Test Files/job.bin"
jobs_names = [
    "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02", "trainer03", "mascot02",
    "mascot03"
    ]

def read_hex(path):
    with path.open(mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data

def job_bin_to_hex():
    job_bin = pathlib.Path(job_bin_path)
    hex_data = read_hex(job_bin)
    return hex_data

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
        return hex_file_data[position:position+104] #Returns everything up until Abilities (not including abilities)

def parse_chunk(chunk: str):
    if chunk == "Index position not found." or len(chunk) != 104:
        return "Error"
    else:
        seperated_chunks = []
        default_attack = chunk[8:12]
        seperated_chunks.append(default_attack)
        hp_mp_length = 6
        stat_length = 10
        initial_position = 12
        for i in range(1,11):
            if i < 3:
                seperated_chunks.append(chunk[initial_position:initial_position+hp_mp_length])
                initial_position = initial_position+ hp_mp_length
            else:
                seperated_chunks.append(chunk[initial_position:initial_position + stat_length])
                initial_position = initial_position + stat_length
        return seperated_chunks

def initiate_dresspheres():
    # Get the job file string
    hex_string = job_bin_to_hex()

    # Initiate dresspheres
    dresspheres = []
    for index, job in enumerate(jobs_names):
        problematic_ids = [12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

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
        for index, stat in enumerate(stat_names):
            dressphere.stats[stat] = formulae[index + 1]

    return dresspheres




dresspheres = initiate_dresspheres()
print("_---------------------------")
print(dresspheres[7])
print(dresspheres[7].stats["MAG"])
#0e 0a 11 12 01
variable_str = "0e 0a 11 12 01"
variable_str = variable_str.replace(" ", "")
dresspheres[7].stats["MAG"] = variable_str
stat_names = ["STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
dresspheres[7].stat_formula("MAG",tableprint=True)




