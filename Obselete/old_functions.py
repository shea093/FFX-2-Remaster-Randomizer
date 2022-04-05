import random

from dressphere import Dressphere
from dressphere_execute import get_big_chunks, dresspheres, seed, job_bin_to_hex, jobs_names
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