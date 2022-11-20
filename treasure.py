class Treasure:
    def __init__(self, treasure_id: str, treasure_num: str, type_index: int, treasure_type: str):
        self.treasure_id = treasure_id
        self.treasure_num = treasure_num
        self.treasure_type = treasure_type
        self.treasure_type_index = type_index
        self.treasure_num_index = type_index + 2
        self.treasure_id_index = type_index + 4