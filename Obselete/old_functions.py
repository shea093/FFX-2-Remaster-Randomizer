import random

from dressphere import Dressphere
from dressphere_randomize import get_big_chunks, dresspheres, seed, job_bin_to_hex, jobs_names
from services import find_chunk, parse_chunk


def job_bin_randomizer_bad():
    chunks_output = get_big_chunks(get_all_segments=True)
    dress_chunks = []
    county = 0
    for dress in dresspheres:
        print("----POSITION------")
        dress.big_chunk = dress.big_chunk.replace(dress.ability_hex_og, dress.ability_hex)
        dress_chunks.append(dress.big_chunk)
        print("----$$$$$$$#------")
    job_bin_string_randomed = chunks_output[0]
    chunks_to_random = dress_chunks[0:14]

    for chunk in dress_chunks[22:30]:
        chunks_to_random.append(chunk)

    random.Random(seed).shuffle(chunks_to_random)

    joined_chunks = []
    for i in range(1, 15):
        joined_chunks.append(chunks_to_random[i - 1])
    for i in range(1, 9):
        joined_chunks.append(dress_chunks[i + 13])
    for i in range(1, 9):
        joined_chunks.append(chunks_to_random[i + 13])

    for chunk in joined_chunks:
        job_bin_string_randomed = job_bin_string_randomed + chunk

    job_bin_string_randomed = job_bin_string_randomed + chunks_output[1][30] + chunks_output[2]
    print("size: ", len(job_bin_string_randomed))
    print(job_bin_string_randomed)
    print("complete")
    print(chunks_output[1][30])


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


def decode_chunk(chunk_val_list: list[str]):
    encode_dict = {
        '30': '0', '31': '1', '32': '2', '33': '3', '34': '4', '35': '5', '36': '6', '37': '7', '38': '8',
        '39': '9', '20': ' ', '21': '!', '9D': '.', '23': '#', '24': '$', '25': '%',
        '26': '&', '99': '™', '28': '(', '29': ')', '2A': '*', '2B': '+', '2C': ',',
        '2D': '-', '2E': '.', '2F': '/', '3A': ':', '3B': ';', '3C': '<', '3D': '=', '3E': '>', '3F': '?',
        '41': 'A', '42': 'B', '43': 'C', '44': 'D', '45': 'E', '46': 'F', '47': 'G', '48': 'H', '49': 'I',
        '4A': 'J', '4B': 'K', '4C': 'L', '4D': 'M', '4E': 'N', '4F': 'O', '50': 'P', '51': 'Q', '52': 'R',
        '53': 'S', '54': 'T', '55': 'U', '56': 'V', '57': 'W', '58': 'X', '59': 'Y', '5A': 'Z', '5B': '[',
        '5C': '/', '5D': ']', '5E': '^', '5F': '_', 'E2': 'â', '80': '€', '98': '˜', '61': 'a', '62': 'b',
        '63': 'c', '64': 'd', '65': 'e', '66': 'f', '67': 'g', '68': 'h', '69': 'i', '6A': 'j', '6B': 'k',
        '6C': 'l', '6D': 'm', '6E': 'n', '6F': 'o', '70': 'p', '71': 'q', '72': 'r', '73': 's', '74': 't',
        '75': 'u', '76': 'v', '77': 'w', '78': 'x', '79': 'y', '7A': 'z', '7B': '{', '7C': '|', '7D': '}',
    }

    output_str = ""
    for val in chunk_val_list:
        output_str = output_str + encode_dict[val]

    return output_str


ending_chunk_test  = commands_shuffle_chunks[-1]
b = bytearray()
b.extend(map(ord, ending_chunk_test))
endingchunklist = []
for byt in b:
    endingchunklist.append(hex(byt)[2:])
c = decode_chunk(endingchunklist)
print(c)
testy = ""



#################
byte_A = reverse_four_bytes("06000040") + reverse_four_bytes("17000000")
byte_B = reverse_four_bytes("ed02ed02")

monmaglast = get_big_chunks(get_all_segments=True,segment_type="mon-magic")[-1]
monmag_string = decode_chunk(monmaglast)
monmag_dicts = []

mon_mag_split = monmag_string.split("◘")

mon_mag_names = mon_mag_split[::2]
mon_mag_helps = mon_mag_split[1::2]

for index, monmag in enumerate(mon_magic_abilities):
    monmag.name = mon_mag_names[index]
    monmag.help_text = mon_mag_helps[index]
    this_list = [monmag]
    this_dict = {'Animation': reverse_two_bytes(monmag.og_hex_chunk[16:24]), 'Start Motion': monmag.og_hex_chunk[24:26],
                 'Line1 reversed': reverse_four_bytes(monmag.og_hex_chunk[32:40]),
                 'Line2 reversed': reverse_four_bytes(monmag.og_hex_chunk[40:48])}
    this_list.append(this_dict)
    monmag_dicts.append(this_list)

test
'032b032b'
'011a011a'
'00450045'
'00c300c3'
'4000000600000017'
'01180118'
'009a009a'
'032a032a'
'4100000600000031'
'6001000600000013'

def btl_bins():
    valid_battle_bin_names = []
    with open ("Test Files/btl.txt",mode='r') as f:
        for line in f.readlines():
            valid_battle_bin_names.append(line.strip())

    btl_sub_dirs = monster_edit.get_subdirectories(btl_path_name)
    btl_bin_files = {}
    for directory in btl_sub_dirs:
        if directory.name in valid_battle_bin_names:
            for file in directory.iterdir():
                dir_compare = directory.name + ".bin"
                if file.is_file() and (file.name == dir_compare):
                    hex_data = read_hex(file)
                    btl_bin_files[directory.name] = read_hex(file)

    for bbin_directory, bbin_hex in btl_bin_files.items():
        os_prefix = os.getcwd()
        os_prefix = os_prefix + "/BTLBINS/"

        bin_name = bbin_directory + ".bin"
        os_filename = os_prefix + bin_name
        # directory_path = os.path.join(os_prefix, bbin_directory)
        filepath = pathlib.PureWindowsPath(os_filename)
        binary_converted = binascii.unhexlify(bbin_hex)
        with open(filepath, mode="wb") as f:
            test
            f.write(binary_converted)





def test_ids():
    test_ids = []
    bin_enemy_index_directory = {}
    for valid_id in valid_enemy_hex_ids:
        valid_id_end_separate = " " + valid_id[0:2] + " " + valid_id [2:4] + " ff ff ff ff "
        valid_id_find_index = btl_bin_hexes["lchb19_229.bin"].find(valid_id_end_separate)
        if valid_id_find_index > 0:
            valid_id_new_search = btl_bin_hexes["lchb19_229.bin"][valid_id_find_index-42:valid_id_find_index+len(valid_id_end_separate)]
            id_found = []
            for jalid_id in valid_enemy_hex_ids:
                jalid_id_separate = " " + jalid_id[0:2] + " " + jalid_id[2:4] + " "
                m = [m.start() for m in re.finditer(jalid_id_separate, valid_id_new_search)]
                if m:
                    id_with_m = [jalid_id,m]
                    id_found.append(id_with_m)
            bin_enemy_index_directory["lchb19_229.bin"] = id_found
            break

def bin_id_find_encounters_OLDER():
    bin_enemy_index_directory = {}
    for btl_bin_hex_name, btl_bin_hex in btl_bin_hexes.items():
        test_ids = []
        for valid_id in valid_enemy_hex_ids:
            valid_id_end_separate = " " + valid_id[0:2] + " " + valid_id[2:4] + " ff ff ff ff "
            valid_id_find_index = btl_bin_hex.find(valid_id_end_separate)
            if valid_id_find_index > 0:
                valid_id_new_search = btl_bin_hex[
                                      valid_id_find_index - 42:valid_id_find_index + len(valid_id_end_separate)]
                id_found = []
                for jalid_id in valid_enemy_hex_ids:
                    jalid_id_separate = " " + jalid_id[0:2] + " " + jalid_id[2:4] + " "
                    m = [m.start() for m in re.finditer(jalid_id_separate, valid_id_new_search)]
                    if m:
                        id_with_m = [jalid_id, m]
                        id_found.append(id_with_m)
                bin_enemy_index_directory[btl_bin_hex_name] = id_found
                break

def bin_id_find_encounters_new():
    bin_enemy_index_directory = {}
    for btl_bin_hex_name, btl_bin_hex in btl_bin_hexes.items():
        test_ids = []
        for valid_id in valid_enemy_hex_ids:
            valid_id_end_separate = " " + valid_id[0:2] + " " + valid_id[2:4] + " ff ff ff ff "
            valid_id_find_index = btl_bin_hex.find(valid_id_end_separate)
            if valid_id_find_index > 0:
                valid_id_new_search = btl_bin_hex[
                                      valid_id_find_index - 42:valid_id_find_index + len(valid_id_end_separate)]
                id_found = []
                for jalid_id in valid_enemy_hex_ids:
                    jalid_id_separate = jalid_id[0:2] + " " + jalid_id[2:4] + " "
                    m = [m.start() for m in re.finditer(jalid_id_separate, valid_id_new_search)]
                    for jnd in range(0, len(m)):
                        m[jnd] = m[jnd] + valid_id_find_index - 42
                    if m:
                        id_with_m = [jalid_id, m]
                        id_found.append(id_with_m)
                bin_enemy_index_directory[btl_bin_hex_name] = id_found

def get_enemy_ids_of_enemy_matches(enemy_match_dir: dict):
    return_list = []
    for e in enemy_match_dir.values():
        e_id = hex(e.enemy_id)[2:]
        e_id = e_id[2:4] + e_id[0:2]
        test
        return_list.append(e_id)
    return return_list


oversoul_hex_pos,  #EXP
                                       oversoul_hex_pos + 8,  #GIL
                                       oversoul_hex_pos + 8 + 8,  #STEALGIL
                                       oversoul_hex_pos + 8 + 8 + 8,  #AP
                                       oversoul_hex_pos + 8 + 8 + 8 + 4,  #ITEM RATE
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2,  #STEAL RATE
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2,  #NORMAL DROP
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4,  #NORMAL DROP NUM
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4,  #RARE DROP
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4,  #RARE DROP NUM,
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4 + 4,  # STEALITEM
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4 + 4 + 4,  # STEALITEM NUM
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4 + 4 + 4 + 4,  #BRIBE ITEM
                                       oversoul_hex_pos + 8 + 8 + 8 + 4 + 2 + 2 + 4 + 4 + 4 + 4 + 4 + 4 + 4, # BRIBE ITEM NUM