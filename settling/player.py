from abc import ABCmeta, abstractmethod


class Player(metaclass=ABCmeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def starting_town(self, board):
        pass

    @abstractmethod
    def play_action_card(self, board, hand):
        pass

    @abstractmethod
    def act(self, board, hand):
        pass
