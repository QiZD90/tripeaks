import random
import pygame
from cards import *
from graphics import *
from settings import *


class Node:
	def hasCard(self):
		return bool(self.card)

	def takeCard(self):
		card = self.card
		self.card = None
		return card

	def setCard(self, card):
		self.card = card

	def isFree(self):
		return not self.depends_on\
		       or (not self.depends_on[0].hasCard()\
		       	   and not self.depends_on[1].hasCard())

	def __init__(self, card, x, y, depends_on):
		self.card = card
		self.x = x
		self.y = y
		self.depends_on = depends_on


class TakeCardFromStockAction:
	def apply(self):
		card = deck.deal()
		waste.add(card)

		animation.start(
			Animation.STOCK_TO_WASTE, card,
			(CARD_W * SCALE, SCREEN_H - CARD_H * SCALE),
			(0, SCREEN_H - CARD_H * SCALE))

	def revert(self):
		card = waste.deal()
		deck.add(card)

		animation.start(
			Animation.WASTE_TO_STOCK, card,
			(0, SCREEN_H - CARD_H * SCALE),
			(CARD_W * SCALE, SCREEN_H - CARD_H * SCALE))


class TakeCardFromArrAction:
	def apply(self):
		card = self.node.takeCard()
		waste.add(card)

		animation.start(
			Animation.ARR_TO_WASTE, card,
			(self.node.x * SCALE, self.node.y * SCALE),
			(0, SCREEN_H - CARD_H * SCALE))

	def revert(self):
		card = waste.deal()
		self.node.setCard(card)

		animation.start(
			Animation.WASTE_TO_ARR, card,
			(0, SCREEN_H - CARD_H * SCALE),
			(self.node.x * SCALE, self.node.y * SCALE))

	def __init__(self, node):
		self.node = node


class ActionManager:
	def takeFromStock(self):
		if deck.isEmpty():
			loseGame()
			return

		action = TakeCardFromStockAction()
		self.actions.append(action)
		action.apply()

		if self.reverts_left < MAX_REVERTS:
			self.reverts_left += 1

	def takeFromArr(self, node):
		if not node.isFree() or not node.hasCard():
			return

		card = node.card
		wcard = waste.peek()

		if card.rankDiff(wcard, wrap=True) != 1:
			return

		action = TakeCardFromArrAction(node)
		self.actions.append(action)
		action.apply()

		if checkForWin():
			winGame()

		if self.reverts_left < MAX_REVERTS:
			self.reverts_left += 1

	def revert(self):
		global gameState

		if self.reverts_left <= 0 or not self.actions:
			return

		self.actions.pop().revert()
		self.reverts_left -= 1

		if gameState == GAME_LOST:
			gameState = GAME_IN_PROGRESS

	def __init__(self):
		self.actions = []
		self.reverts_left = MAX_REVERTS


def newGame():
	deck = Deck(shuffle=True)

	arrangement = []
	arrangement.insert(
		0, [Node(deck.deal(), i * CARD_W, LAYER_GAP * 3, []) for i in range(10)]) # last level

	temp = [Node(deck.deal(), i * CARD_W + CARD_W // 2, LAYER_GAP * 2, [arrangement[0][i], arrangement[0][i + 1]]) for i in range(9)]
	arrangement.insert(0, temp) # third level

	temp = []
	for i in range(6):
		x = CARD_W + i * CARD_W + CARD_W * (i // 2)
		y = LAYER_GAP * 1
		depends_on = [arrangement[0][i + i // 2], arrangement[0][i + i // 2 + 1]]
		temp.append(Node(deck.deal(), x, y, depends_on))
	arrangement.insert(0, temp) # second level

	temp = []
	for i in range(3):
		x = CARD_W + CARD_W // 2 + i * CARD_W * 3
		y = LAYER_GAP * 0
		depends_on = [arrangement[0][i * 2], arrangement[0][i * 2 + 1]]
		temp.append(Node(deck.deal(), x, y, depends_on))
	arrangement.insert(0, temp) # first level

	waste = Deck(empty=True)
	waste.add(deck.deal())

	animation.stop()

	return deck, arrangement, waste, ActionManager(), GAME_IN_PROGRESS

def getPressedNode(pos, scale):
	for row in arrangement[::-1]:
		for node in row:
			if not node.hasCard() or not node.isFree():
				continue

			if node.x * scale > pos[0] or node.x * scale + CARD_W * scale <= pos[0]:
				continue

			if node.y * scale > pos[1] or node.y * scale + CARD_H * scale <= pos[1]:
				continue

			return node

def wasStockPressed(pos, scale):
	if pos[0] < CARD_W * scale or pos[0] > CARD_W * scale + CARD_W * scale:
		return False

	if pos[1] < SCREEN_H - CARD_H * scale or pos[1] > SCREEN_H:
		return False

	return True

def checkForWin():
	for row in arrangement:
		for node in row:
			if node.hasCard():
				return False

	return True

def loseGame():
	global gameState
	gameState = GAME_LOST

def winGame():
	global gameState
	gameState = GAME_WON


clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

deck, arrangement, waste, actionManager, gameState = newGame()

running = True
while running:
	dt = clock.tick()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_z and gameState != GAME_WON:
				actionManager.revert()

			elif event.key == pygame.K_r:
				deck, arrangement, waste, actionManager, gameState = newGame()

		elif event.type == pygame.MOUSEBUTTONUP and gameState == GAME_IN_PROGRESS:
			if event.button == 1: # LMB
				node = getPressedNode(event.pos, SCALE)

				if node:
					actionManager.takeFromArr(node)

				elif wasStockPressed(event.pos, SCALE):
					actionManager.takeFromStock()

	screen.fill((0, 0, 0))

	# Draw the "pyramids"
	for i, nodes in enumerate(arrangement):
		for j, node in enumerate(nodes):
			if animation.isActive() and animation.getType() == Animation.WASTE_TO_ARR:
				if animation.end_pos == (node.x * SCALE, node.y * SCALE):
					continue

			card = node.card
			isFree = node.isFree()
			drawCard(card, screen, node.x * SCALE, node.y * SCALE, up=isFree, scale=SCALE)

	# Draw the waste pile and deck
	drawWastePile(waste, screen, scale=SCALE)
	drawStock(deck, screen, scale=SCALE)

	# Draw animation
	if animation.isActive():
		animation.tick(dt)
		drawCard(animation.card, screen, animation.x, animation.y, up=True, scale=SCALE)

	if gameState != GAME_IN_PROGRESS:
		drawEndSplash(gameState, screen)

	pygame.display.update()

pygame.quit()