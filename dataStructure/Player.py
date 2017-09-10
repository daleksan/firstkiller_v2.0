class Player:
    def __init__(self, id, name="Unknown"):
        self.id = id
        self.name = name
        self.numberOfKills = 0
        self.victim = None

    def __str__(self, *args, **kwargs):
        return "Player {} (id = {})".format(
            self.name, self.id)
