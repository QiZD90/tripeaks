import random

class Card:
	CLUBS = 1 # ♣
	DIAMONDS = 2 # ♦
	HEARTS = 3 # ♥
	SPADES = 4 # ♠

	def rankDiff(self, card, wrap=False):
		normalDiff = abs(self.rank - card.rank)
		wrappedDiff = min(self.rank, card.rank) + 13 - max(self.rank, card.rank)

		if wrap:
			return min(normalDiff, wrappedDiff)

		return normalDiff

	def isRed(self):
		return self.suit == Card.DIAMONDS or self.suit == Card.HEARTS

	def isBlack(self):
		return self.suit == Card.CLUBS or self.suit == Card.SPADES

	def suitAsSymbol(self):
		if self.suit == Card.CLUBS:
			return '♣'

		if self.suit == Card.DIAMONDS:
			return '♦'

		if self.suit == Card.HEARTS:
			return '♥'

		if self.suit == Card.SPADES:
			return '♠'

		return '?'

	def suitAsText(self):
		if self.suit == Card.CLUBS:
			return 'clubs'

		if self.suit == Card.DIAMONDS:
			return 'diamonds'

		if self.suit == Card.HEARTS:
			return 'hearts'

		if self.suit == Card.SPADES:
			return 'spades'

		return '?'

	def rankAsText(self):
		if self.rank >= 2 and self.rank <= 10:
			return str(self.rank)

		if self.rank == 1:
			return 'A'

		if self.rank == 11:
			return 'J'

		if self.rank == 12:
			return 'Q'

		if self.rank == 13:
			return 'K'

		return '??'

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __repr__(self):
		return f'({self.rankAsText()} {self.suitAsSymbol()})'


class Deck:
	# Randomly shuffles the card of the deck
	def shuffle(self):
		random.shuffle(self.cards)

	# Returns the topmost card from the deck or `None` if there is none
	def peek(self):
		if not self.cards:
			return None

		return self.cards[-1]

	# Returns the second from the top card from the deck or `None` if there is none
	def peek2(self):
		if not self.cards or len(self.cards) < 2:
			return None

		return self.cards[-2]

	# Returns the topmost card from the deck and removes it from the deck
	def deal(self):
		return self.cards.pop()

	# Adds the given card on top of the deck
	def add(self, card):
		self.cards.append(card)

	def isEmpty(self):
		return self.cards == None or len(self.cards) == 0

	def size(self):
		return len(self.cards)

	def __init__(self, empty=False, shuffle=True):
		self.cards = []

		if empty:
			return

		# Generate and add cards of all suits and oll ranks in order
		for suit in (Card.CLUBS, Card.DIAMONDS, Card.HEARTS, Card.SPADES):
			for rank in range(1, 14):
				self.cards.append(Card(suit, rank))

		if shuffle:
			random.shuffle(self.cards)

	def __repr__(self):
		return '[{}]'.format(', '.join([str(card) for card in self.cards]))