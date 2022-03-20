import binascii
import re
import pickle
from enemy import Enemy
from pathlib import Path

file_iterations = 183

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
            enemy.stat_bank["HP"] = int(enemy_info[1])
            enemy.stat_bank["MP"] = int(enemy_info[2])
            enemy.oversoul_stat_bank["HP"] = int(enemy_info[3])
            enemy.oversoul_stat_bank["MP"] = int(enemy_info[4])
            enemies.append(enemy)
            if id == max:
                break
    return enemies




enemies = []


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
for index, enemy in enumerate(enemies):
    hpmphex = enemy.output_HP_MP(formatted=False, oversoul=False)
    position = str(enemy.enemy_hex_data).find(hpmphex)
    if position == -1:
        errors = errors + 1
        normal_errors = normal_errors + 1
        print(enemy)
        print(f"{index + 1:03}" + ".    " + enemy.output_HP_MP(formatted=True, oversoul=False))
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
for index, enemy in enumerate(enemies):
    hpmphex = enemy.output_HP_MP(formatted=False, oversoul=True)
    position = str(enemy.enemy_hex_data).find(hpmphex)
    if position == -1:
        errors = errors + 1
        oversoul_errors = oversoul_errors + 1
        print(enemy)
        print(f"{index + 1:03}" + ".    " + enemy.output_HP_MP(formatted=True, oversoul=True))
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("%%%%%%%%%%%%%%%%%%")
print("Non-oversoul Errors: ", normal_errors, "/",file_iterations)
print("Oversoul Errors: ", oversoul_errors, "/",file_iterations)


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

