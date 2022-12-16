import pygame
from cards import *
from settings import *
from animation import *

pygame.init()
cardRankFont = pygame.font.SysFont('arial', 48)
cardSuitFont = pygame.font.SysFont('arial', 72)
cardsLeftInStockFont = pygame.font.SysFont('arial', 24)
endSplashFont = pygame.font.SysFont('arial', 36)


def drawCard(card, screen, x, y, up=True, scale=1.0):
	if not card:
		return

	cs = pygame.Surface((CARD_W, CARD_H)).convert_alpha()
	cs.fill((0, 0, 0, 0))

	# Draw a card and it's outline
	pygame.draw.rect(cs, (255, 255, 255), pygame.Rect(0, 0, CARD_W, CARD_H),  0, 15)
	pygame.draw.rect(cs, (0, 0, 0), pygame.Rect(0, 0, CARD_W, CARD_H),  1, 15)

	if up:
		# Draw a card's rank in 4 corners
		ts = cardRankFont.render(card.rankAsText(), True, (0, 0, 0))
		size = ts.get_size()
		cs.blit(ts, (TEXT_MARGIN, TEXT_MARGIN))
		cs.blit(ts, (CARD_W - size[0] - TEXT_MARGIN, TEXT_MARGIN))
		ts = pygame.transform.flip(ts, True, True)
		cs.blit(ts, (TEXT_MARGIN, CARD_H - size[1] - TEXT_MARGIN))
		cs.blit(ts, (CARD_W - size[0] - TEXT_MARGIN, CARD_H - size[1] - TEXT_MARGIN))

		color = (255, 0, 0) if card.isRed() else (0, 0, 0)
		ts = cardSuitFont.render(card.suitAsSymbol(), True, color)
		size = ts.get_size()
		cs.blit(ts, (CARD_W // 2 - size[0] // 2, CARD_H // 2 - size[1] // 2))

	else:
		# Draw a back side
		for i in range(BACKSIDE_MARGIN, CARD_W - BACKSIDE_MARGIN + 1, 10):
			pygame.draw.line(
				cs, (255, 0, 0),
				[i, BACKSIDE_MARGIN], [i, CARD_H - BACKSIDE_MARGIN])

		for i in range(BACKSIDE_MARGIN, CARD_H - BACKSIDE_MARGIN + 1, 10):
			pygame.draw.line(
				cs, (255, 0, 0),
				[BACKSIDE_MARGIN, i], [CARD_W - BACKSIDE_MARGIN, i])

	if scale != 1.0:
		cs = pygame.transform.smoothscale_by(cs, scale)

	screen.blit(cs, (x, y))


def drawWastePile(waste, screen, scale=1.0):
	x = 0
	y = SCREEN_H - CARD_H * SCALE
	card = waste.peek()
	if animation.isActive()\
	   and animation.getType() in (Animation.STOCK_TO_WASTE,
	                               Animation.ARR_TO_WASTE):
		card = waste.peek2()

	drawCard(card, screen, x, y, up=True, scale=SCALE)


def drawStock(deck, screen, scale=1.0):
	x = CARD_W * SCALE
	y = SCREEN_H - CARD_H * SCALE
	drawCard(deck.peek(), screen, x, y, up=False, scale=SCALE)

	ts = cardsLeftInStockFont.render(f'({deck.size()})', True, (0, 0, 0))
	textSize = ts.get_size()
	textX = x + CARD_W * SCALE // 2 - textSize[0] // 2
	textY = y + CARD_H * SCALE // 2 - textSize[1] // 2
	screen.blit(ts, (textX, textY))

def drawEndSplash(gameState, screen):
	lines = [
		'You won!' if gameState == GAME_WON else 'You lose!',
		'Press `R` to restart the game'
	]

	if gameState == GAME_LOST:
		lines.append('Press `Z` to revert your last actions')

	surfaces = [endSplashFont.render(x, True, (255, 255, 255)) for x in lines]
	combinedHeight = sum([x.get_size()[1] for x in surfaces])
	maxWidth = max([x.get_size()[0] for x in surfaces])

	# Draw a backdrop
	pygame.draw.rect(
		screen, (128, 128, 128),
		pygame.Rect(
			SCREEN_W // 2 - maxWidth // 2 - SPLASH_BACKDROP_MARGIN,
			SCREEN_H // 2 - combinedHeight // 2 - SPLASH_BACKDROP_MARGIN,
			maxWidth + SPLASH_BACKDROP_MARGIN * 2,
			combinedHeight + SPLASH_BACKDROP_MARGIN * 2))

	y = SCREEN_H // 2 - combinedHeight // 2
	for ts in surfaces:
		textSize = ts.get_size()
		x = SCREEN_W // 2 - textSize[0] // 2

		screen.blit(ts, (x, y))
		y += textSize[1]

