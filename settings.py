# A module to store important "magic values" in

SCREEN_W, SCREEN_H = 800, 640 # width and height of the game screen in pixels
CARD_W, CARD_H = 250, 350 # width and height of the card with scale set to 1.0
LAYER_GAP = 200 # gap between layers of pyramids with scale set to 1.0
SCALE = 0.3

TEXT_MARGIN = 5 # the margin between cornerns of a card
                # and a text representation of a card's rank

BACKSIDE_MARGIN = 20 # the margin between sides of a card
                     # and a backside pattern

SPLASH_BACKDROP_MARGIN = 40

MAX_REVERTS = 3

# Game state constants
GAME_IN_PROGRESS = 0
GAME_WON = 1
GAME_LOST = 2