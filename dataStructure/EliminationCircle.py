from Player import Player
from copy import copy
from random import shuffle


class EliminationCircle:
    def __init__(self, playersList, isShuffled=False):

        """
        Creates data structure of killers and their victims.
        If input list is empty, it raises an exception.
        :param playersList: list of Players, or a list of tuples with id and names(optional).
        :param isShuffled: if enabled, shuffle a list before the victim arrangement
        """
    self.circle = []
    self.gameFinished = False
    for listElement in playersList:
        playerObject = copy(listElement) if isinstance(listElement, Player) else Player(*listElement)
        self.circle.append(playerObject)
    if isShuffled:
        shuffle(self.circle)
    if self.circle:
        for index in range(len(self.circle)):
            self.circle[index - 1].victim = self.circle[index]
    else:
        raise Exception("Killers circle is empty!")


def kill(self, killerId, victimId, isChecked=True, printStatus=True):
    """

    :param killerId: Id of a killer
    :param victimId: Id of a killer's victim
    :param isChecked: if True, check input victimId with victim Id in data structure
    :param printStatus: if True, print all status messages to stdout
    :return:
    """
    if self.gameFinished:
        if printStatus:
            print("Game is already finished")
        return False
    killer = list(filter(lambda x: x.id == killerId, self.circle))[0]
    killerListIndex = self.circle.index(killer)
    victimListIndex = self.circle.index(killer.victim)
    oldVictim = killer.victim
    if killer.victim.id == victimId or not isChecked:
        killer.victim = oldVictim.victim
        killer.numberOfKills += 1
        if printStatus:
            print(
                "Player {} (id = {}) has killed player {} (id = {}). His new victim is player {} (id = {})".format(
                    killer.name, killer.id, oldVictim.name, oldVictim.id, killer.victim.name, killer.victim.id))
        self.circle.remove(oldVictim)
        if len(self.circle) == 2:
            if printStatus:
                print(
                    "Game over. Winners are player {} (id = {}) and player {} (id = {})".format(self.circle[0].name,
                                                                                                self.circle[0].id,
                                                                                                self.circle[1].name,
                                                                                                self.circle[1].id))
            return True
    else:
        if printStatus:
            print("Incorrect victimId for killer")
    return False


def printPlayers(self):
    for player in self.circle:
        print(player)


if __name__ == "__main__":
    a = Player(1, "Vasya")
    b = Player(2, "Petya")
    c = Player(3, "Misha")
    game = EliminationCircle([a, b, c])
    game.printPlayers()
    game.kill(1, 2)
