# The specification mentioned that this team wanted to place initial values on
# the class and modify that. However, this is not ideal since for any mutable
# data structures (list for example), each new class gets the same reference to
# that list. Therefore, all operations are done on the same list, not on a list
# per instance. However, since this is what the specification asked for we have
# implemented it that way.
class Player:
    def __init__(self, playerNum, strategy=None):
        if strategy is None or strategy == 0:
            self.strategy = 0
        else:
            raise ValueError('unknown strategy')

        self.playerNum = playerNum

    def chooseCard(self, board):
        last_index = len(self.cards)
        card = self.cards.pop(last_index)
        board.placeCard(card)

        # The docstring specifies to return Tuple(Card, Nat), but says nothing
        # about what the natural number represents. Maybe this was meant to be
        # the stack to place the card on, but that's not how the game works.
        # We have decided to return the index of the card in the hand instead.
        return card, last_index

    def addBullPoint(self, n):
        self.bullpoints += n

