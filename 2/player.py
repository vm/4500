# The specification mentioned that this team wanted to place initial values on
# the class and modify that. This is not ideal since for any mutable
# data structures (list for example), each new class gets the same reference to
# that list and all operations are done on the same list, not on a list
# per instance. As this is what the specification asked for we have
# implemented it as provided.
class Player:
    playerNum = -1
    strategy = 0
    bullPoints = 0
    cards = []

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

    # This was not specified in the specification, but it's impossible to play
    # the game without it, as stack selection is only done on certain cases
    # and after all players have discarded cards (so cannot be selected in
    # chooseCard). We implement this here, with stacks being passed
    # in as an argument.
    def chooseStack(self, stacks):
        """select a stack to place a card on

        :param stacks: stacks to select from
        :type stacks: list of list of Card

        :returns: index of the stack to place card on
        :rtype: int
        """

        def sumStackBullPoints(i):
            return sum(card.BullPoints for card in stacks[i])

        return min(range(len(stacks)), key=sumStackBullPoints)
