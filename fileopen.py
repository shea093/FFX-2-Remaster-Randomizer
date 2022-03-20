import binascii
import re
import pickle
from enemy import Enemy
from pathlib import Path


# Read a binary file and convert it into hex data
def read_hex(path):
    with path.open(mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data


# Get the directories with the monster files
def get_subdirectories(path):
    vbf_str = "/" + path
    vbf_dir = Path(vbf_str)  # VBF Directory
    vbf_subdirs = []   # Subdirectory list initialized

    # Iterate through subdirectories and append them to a list
    [vbf_subdirs.append(x) for x in vbf_dir.iterdir() if x.is_dir()]

    return vbf_subdirs


# Possibly useless lol
def mon_binlist_generator():
    mon_nums = list(range(1, 5)) #Range of files to traverse
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


# Get hex data from the files
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
    with open("english_creature_names.txt", "r") as f:
        for line in f.readlines():
            pre_slice = line[5:27]
            pre_slice = re.sub(r"\s+", "", pre_slice, flags=re.UNICODE)
            creature_names.append(pre_slice)
    with open("new_english_creature_names.txt", "w") as f:
        for line in creature_names:
            f.write(line + "\n")


def search_stats(hexes):
    stat_hex = "237a0800"
    position = str(hexes[0]).find(stat_hex)
    return position

def test_enemy_maker():
    pass

enemies = []


# Tests
cut_creature_english_names()
print(get_subdirectories("VBF_X2"))
print(mon_binlist_generator())
hex_test = traverse_files()
print(type(hex_test[0]))
object_test = Enemy("Sallet", 1, hex_test[0])
object_test.stat_bank["HP"] = 60
object_test.stat_bank["MP"] = 4
object_test.oversoul_stat_bank["HP"] = 248
object_test.oversoul_stat_bank["MP"] = 4
print(object_test.stat_bank)
print(object_test.output_HP_MP(formatted=True))
print(object_test.output_HP_MP(formatted=True, oversoul=True))
print(search_stats(hex_test))
print(object_test.search_stats(object_test.output_HP_MP(oversoul=True)))
# cut_creature_values()

