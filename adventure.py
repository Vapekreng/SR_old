START_LOCATION_ID = {}
START_LOCATION_ID[''] =
START_LOCATION_ID[''] =
START_LOCATION_ID[''] =
START_LOCATION_ID[''] =
START_LOCATION_ID[''] =
START_LOCATION_ID[''] =

class Adventure:


    def __init__(self):
        self.main_hero = self.generate_new_hero()
        self.current_location_id = START_LOCATION_ID
        self.save_game = False
        self.quit_game = False
        self.new_location = START_LOCATION_ID
        pass

    def run(self):
        self.change_location()

    def save(self):
        pass

    def load(self):
        pass

    def generate_new_hero(self):
        pass

    def generate_new_world(self):
        pass