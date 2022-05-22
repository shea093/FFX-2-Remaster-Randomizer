from dressphere import Dressphere


def read_hex(path):
    with path.open(mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data


def find_chunk(id_input: int, hex_file_data: str, problematic_id=0):
    id = hex(id_input)[2:]
    unique_ids = []
    if len(id) == 1:
        id = "0" + id
    if problematic_id != 0:
        if problematic_id == 23:
            class_line = "1a5c"
            position = hex_file_data.find(class_line) - 4
        elif problematic_id == 24:
            class_line = "1b5c"
            position = hex_file_data.find(class_line) - 4
        elif problematic_id == 25:
            class_line = "1c5e"
            position = hex_file_data.find(class_line) - 4
        elif problematic_id == 26:
            class_line = "1d5e"
            position = hex_file_data.find(class_line) - 4
        else:
            adjacent_to_id = hex(id_input + 80)[2:]
            class_line = id + str(adjacent_to_id)
            position = hex_file_data.find(class_line) - 4
    else:
        class_line = "ff00" + id
        position = hex_file_data.find(class_line)
    if position == "-1":
        return "Index position not found."
    else:
        return hex_file_data[
               position:position + 232]  # Returns everything up until after Abilities (including abilities)


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
        for i in range(1, 11):
            if i < 3:
                seperated_chunks.append(chunk[initial_position:initial_position + hp_mp_length])
                initial_position = initial_position + hp_mp_length
            else:
                seperated_chunks.append(chunk[initial_position:initial_position + stat_length])
                initial_position = initial_position + stat_length
        for i in range(1, 33):
            seperated_chunks.append(chunk[initial_position:initial_position + ability_length])
            initial_position = initial_position + ability_length
        return seperated_chunks


def pool_stats(dresspheres: list[Dressphere]):
    stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
    stat_pool = [[] for i in range(10)]
    special_dresspheres = ["super_yuna1", "super-yuna2", "super-yuna3",
                           "super_rikku1", "super-rikku2", "super-rikku3",
                           "super_paine1", "super-paine2", "super-paine3", ]
    for dress in dresspheres:
        if dress.dress_name in special_dresspheres:
            test = ""
            pass
        else:
            for index, stat_name in enumerate(stat_names):
                put_into_pool = dress.stat_variables[stat_name]
                stat_pool[index].append(put_into_pool)
    return stat_pool


def replace_stats(dresspheres: list[Dressphere], stat_pool_values: list[list]):
    randomized_output = dresspheres.copy()
    stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
    special_dresspheres = ["super_yuna1", "super-yuna2", "super-yuna3",
                           "super_rikku1", "super-rikku2", "super-rikku3",
                           "super_paine1", "super-paine2", "super-paine3", ]
    stat_pool = stat_pool_values
    county = -1
    for index, dress in enumerate(randomized_output):
        county = county + 1
        if dress.dress_name in special_dresspheres:
            county = county - 1
        else:
            for jndex, stat_name in enumerate(stat_names):
                put_into_pool = stat_pool[jndex][county]
                dress.stat_variables[stat_name] = put_into_pool
                pass
    return randomized_output


def reverse_four_bytes(byte_reverse: str):
    reversed = byte_reverse[6:] + byte_reverse[4:6] + byte_reverse[2:4] + byte_reverse[0:2]
    return reversed


def reverse_two_bytes(byte_reverse: str):
    reversed = byte_reverse[2:] + byte_reverse[0:2]
    return reversed


def search_items_by_id(item_list: list, id_value: str):
    for item in item_list:
        if str(id_value) == str(item.id):
            return item
    return None


def convert_gamevariable_to_reversed_hex(value: int, bytecount=1):
    output_prep = hex(value)
    output_prep = output_prep[2:]
    # 1 Byte
    if bytecount == 1:
        output_prep = output_prep.zfill(2)
        return output_prep
    # 2 Bytes
    if bytecount == 2:
        output_prep = output_prep.zfill(4)
        output_prep = output_prep[2:] + output_prep[0:2]
        return output_prep
    if bytecount == 3:
        output_prep = output_prep.zfill(6)
        output_prep = output_prep[4:] + output_prep[2:4] + output_prep[0:2]
        return output_prep
    if bytecount == 4:
        output_prep = output_prep.zfill(8)
        output_prep = output_prep[6:] + output_prep[4:6] + output_prep[2:4] + output_prep[0:2]
        return output_prep
