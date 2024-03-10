class Search:
    def __init__(self, env):
        self.env = env

    def find_entities(self, collection, criteria):
        return [entity for entity in collection if criteria(entity)]