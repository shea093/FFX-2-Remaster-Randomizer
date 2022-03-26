from dressphere import Dressphere
import pathlib

#INPUT VARIABLES
job_bin_path = "Test Files/job.bin"
jobs = []

def read_hex(path):
    with path.open(mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data

def job_bin_to_hex():
    job_bin = pathlib.Path(job_bin_path)
    hex_data = read_hex(job_bin)
    return hex_data

def find_chunk(id_input: int, hex_file_data: str):
    id = str("{:02d}".format(id_input))
    class_line = "ff00" + id
    position = hex_file_data.find(class_line)
    if position == "-1":
        return "Index position not found."
    else:
        return hex_file_data[position:position+104] #Returns everything up until Abilities (not including abilities)

def parse_chunk(chunk: str):
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

hex_string = job_bin_to_hex()
chunk = find_chunk(1, hex_string)
print(parse_chunk(chunk))
