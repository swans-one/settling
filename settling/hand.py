class Hand:
    def __init__(self, cards=None, action_cards=None):
        self.cards = cards or []
        self.action_cards = action_cards or []
