from abc import ABCMeta, abstractmethod


class Player(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        """
        Returns:
          A string, unique between players. The real life player's name.
        """
        pass

    @abstractmethod
    def starting_town(self, board):
        """
        Returns:
          A tuple (hexagon_coord, vertex) containing the location to place
          the town on.
        """
        pass

    @abstractmethod
    def play_action_card(self, board, hand):
        """
        Returns:
          An instance of a player_action.PlayerActionCard or None.
        """
        pass

    @abstractmethod
    def act(self, board, hand):
        """
        Returns:
          An instance of a class from settling.player_action. If no action
          is to be taken, return EndTurn.
        """
        pass
