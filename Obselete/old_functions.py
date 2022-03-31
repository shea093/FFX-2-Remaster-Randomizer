import random

from dressphere_execute import get_big_chunks, dresspheres, seed


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