import pygame

import numpy as np


def load():
    PLAYER_PATH = 'blue-square.png'
    BACKGROUND_PATH = 'background-black.png'
    LINE_PATH = 'line.png'
    GOLD_PATH = 'gold.png'

    IMAGES, HITMASKS = {}, {}

    IMAGES['background'] = pygame.image.load(BACKGROUND_PATH).convert()
    IMAGES['player'] = pygame.image.load(PLAYER_PATH).convert_alpha()
    IMAGES['line'] = pygame.image.load(LINE_PATH).convert_alpha()
    IMAGES['gold'] = pygame.image.load(GOLD_PATH).convert_alpha()

    HITMASKS['line'] = getHitmask(IMAGES['line'])
    HITMASKS['player'] = getHitmask(IMAGES['player'])
    HITMASKS['gold'] = getHitmask(IMAGES['gold'])

    return IMAGES, HITMASKS


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


FPS = 45 #45 orjınal
SCREENWIDTH = 512
SCREENHEIGHT = 256

pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('The World\'s Hardest Game')

IMAGES, HITMASKS = load()
BASEY = SCREENHEIGHT

PLAYER_WIDTH = IMAGES['player'].get_width()
PLAYER_HEIGHT = IMAGES['player'].get_height()
LINE_WIDTH = IMAGES['line'].get_width()
LINE_HEIGHT = IMAGES['line'].get_height()
GOLD_WIDTH = IMAGES['gold'].get_width()
GOLD_HEIGHT = IMAGES['gold'].get_height()
BACKGROUND_WIDTH = IMAGES['background'].get_width()
LINE_START = 70


class GameState:
    def __init__(self):
        self.score = 0
        self.playerx = 10
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)

        self.lines = getRandomLine()
        self.golds = getGolds()

        self.lineVelX = 3
        self.playerVelX = 4
        self.playerVelY = 4

    def play(self):
        while True:
            pressed = pygame.key.get_pressed()
            left = pressed[pygame.K_LEFT]
            right = pressed[pygame.K_RIGHT]
            up = pressed[pygame.K_UP]
            down = pressed[pygame.K_DOWN]

            action = [0, 0, 0, 0, 0]
            action[1] = 1 if up else 0
            action[2] = 1 if down else 0
            action[3] = 1 if left else 0
            action[4] = 1 if right else 0

            self.frame_step(action)

    def frame_step(self, input_actions):
        pygame.event.pump()

        # you should update this value each frame to train your model
        reward = 0.28
        terminal = False

        up = input_actions[1]
        bottom = input_actions[2]

        left = input_actions[3]
        right = input_actions[4]

        if up == 1 and self.playery > 0:
            self.playery -= self.playerVelY
        elif bottom == 1 and (self.playery + PLAYER_HEIGHT) < SCREENHEIGHT:
            self.playery += self.playerVelY

        if left == 1 and self.playerx > 0:
            self.playerx -= self.playerVelX
        elif right == 1 and (self.playerx + PLAYER_WIDTH) < SCREENWIDTH:
            self.playerx += self.playerVelX

        # returns true if any gold collected in THIS FRAME
        hasGold = checkGolds({'x': self.playerx, 'y': self.playery}, self.golds)

        self.lines[0]['x'] -= self.lineVelX
        self.lines[1]['x'] += self.lineVelX

        if self.lines[0]['x'] < LINE_START or self.lines[1]['x'] < LINE_START:
            self.lineVelX *= -1

        # returns true if square collided with any line
        # if collided, game is restarted.
        isCrash = checkCrash({'x': self.playerx, 'y': self.playery}, self.lines)
        if isCrash:
            terminal = True
            self.__init__()

        SCREEN.blit(IMAGES['background'], (0, 0))

        for line in self.lines:
            SCREEN.blit(IMAGES['line'], (line['x'], line['y']))

        for gold in self.golds:
            SCREEN.blit(IMAGES['gold'], (gold['x'], gold['y']))

        SCREEN.blit(IMAGES['player'], (self.playerx, self.playery))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        return image_data, reward, terminal


def getRandomLine():
    return [
        {'x': SCREENWIDTH - 10, 'y': 10},
        {'x': LINE_START, 'y': SCREENHEIGHT - LINE_HEIGHT - 10},
    ]


def getGolds():
    golds = []
    xs = np.linspace(LINE_START, SCREENWIDTH, num=10)
    for i in range(10):
        golds.append({'x': xs[i], 'y': 25})
        golds.append({'x': xs[i], 'y': SCREENHEIGHT - GOLD_HEIGHT - 25})
    return golds


def checkGolds(player, golds):
    """returns True if player collders with base or pipes."""
    player['w'] = IMAGES['player'].get_width()
    player['h'] = IMAGES['player'].get_height()

    playerRect = pygame.Rect(player['x'], player['y'],
                             player['w'], player['h'])

    for gold in golds:
        line_rect = pygame.Rect(gold['x'], gold['y'], GOLD_WIDTH, GOLD_HEIGHT)

        p_hitmask = HITMASKS['player']
        g_hitmask = HITMASKS['gold']

        collide = pixelCollision(playerRect, line_rect, p_hitmask, g_hitmask)

        if collide:
            golds.remove(gold)
            return True

    return False


def checkCrash(player, lines):
    player['w'] = IMAGES['player'].get_width()
    player['h'] = IMAGES['player'].get_height()

    player_rect = pygame.Rect(player['x'], player['y'], player['w'], player['h'])

    for line in lines:
        # upper and lower pipe rects
        line_rect = pygame.Rect(line['x'], line['y'], LINE_WIDTH, LINE_HEIGHT)

        # player and upper/lower pipe hitmasks
        p_hitmask = HITMASKS['player']
        l_hitmask = HITMASKS['line']

        # if bird collided with upipe or lpipe
        collide = pixelCollision(player_rect, line_rect, p_hitmask, l_hitmask)

        if collide:
            return True

    return False


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False
