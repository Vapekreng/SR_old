class level:

    def __init__(self, id, name, type_of_map_generation, connected_levels_id):
        self.id = id
        self.name = name
        self.connected_levels_id = connected_levels_id
        self.map = self.get_map(type_of_map_generation)



