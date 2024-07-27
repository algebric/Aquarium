import pygame, sys, random, math
from pygame.locals import *
from enum import Enum
import collections

pygame.init()

BACKGROUND = (0, 68, 148)
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 680
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Maya’s Aquarium 0.3')
NUM_EXPLOSION_PARTICLES = 680
NUM_FOOD_PARTICLES = 22
NUM_BURST_BUBBLES = 42
fishAmmoniaImpact = 0.004
shrimpAmmoniaImpact = 0.00014
plantNitrateImpact = 0.0008

class Food:
    def __init__(self, x, y):
        self.posxtion = x
        self.posytion = 0
        self.color = (random.uniform(28, 168), random.uniform(28, 168), random.uniform(0, 68))
        self.drift = random.uniform(-0.22, 0.22)
        self.eaten = False
        self.dist = 0
        self.sparks = []

    
    def draw(self):
        if self.eaten:
            for i in range(NUM_FOOD_PARTICLES):
                pygame.draw.circle(WINDOW, self.color, (int(self.sparks[i].posxtion), int(self.sparks[i].posytion)), self.sparks[i].size)
            return
        
        pygame.draw.circle(WINDOW, self.color, (int(self.posxtion), int(self.posytion)), 8)
        pygame.draw.circle(                                                                                         \
            WINDOW,(                                                                                                \
                min(self.color[0] + 80, 255), min(self.color[1] + 80, 255), min(self.color[2] + 80, 255)),(         \
                int(self.posxtion) - 2, int(self.posytion) - 2),                                                    \
                3                                                                                                   \
            )

    
    def getEaten(self):
        self.eaten = True
        for i in range(NUM_FOOD_PARTICLES):
            self.sparks.append(                     \
                Spark(                              \
                    self.posxtion,                  \
                    self.posytion,                  \
                    random.uniform(0, 2*math.pi),   \
                    random.uniform(1, 2),           \
                    random.randint(1, 2),           \
                    2                               \
                )                                   \
            )


    def update(self):
        if not self.eaten:
            self.posxtion = self.posxtion + self.drift
            self.posytion = self.posytion + 1
            return

        for i in range(NUM_FOOD_PARTICLES):
            self.sparks[i].posxtion = self.sparks[i].posxtion + self.sparks[i].vel * math.sin(self.sparks[ i ].angle)
            self.sparks[i].posytion = self.sparks[i].posytion + self.sparks[i].vel * math.cos(self.sparks[ i ].angle)

        self.dist = self.dist + 1


    def isDecayed(self):
        if self.eaten and self.dist > 48:
            return True
        return self.posytion > WINDOW_HEIGHT - 120


class FaceDirection(Enum):
    LEFT = 0
    RIGHT = 1


class Fish:
    sprite1 = pygame.image.load('fleft.png').convert_alpha()
    sprite2 = pygame.image.load('fash.png').convert_alpha()
    spriteDead = pygame.image.load('fdead.png').convert_alpha()
    SPRITE_WIDTH = 178

    def __init__(self):
        self.posxtion = random.uniform(0, WINDOW_WIDTH - 220)
        self.posytion = random.uniform(0, WINDOW_HEIGHT - 220)
        self.vxl = random.uniform(0.22, 2)
        self.vyl = random.uniform(0.22, 2)
        treasureCounter = random.randint(0, 212)
        self.feedCounter = 0 #random.uniform(22, 1222)
        self.treasureCounter = random.randint(222, 422)
        self.moveCounter = 122
        self.faceDirection = FaceDirection.RIGHT
        self.health = random.uniform(42, 222)
        self.isAlive = True


    def findNewDirection(self):
        self.vxl = random.uniform(-0.8, 0.8)
        self.vyl = random.uniform(-0.2, 0.2)
        if random.uniform(0, 100) > 91:
                self.vxl = self.vxl * 8

        if self.vxl <= 0:
            self.faceDirection = FaceDirection.LEFT
        else:
            self.faceDirection = FaceDirection.RIGHT
                
        self.moveCounter = random.randint(48, 1222)
        

    def update(self, food, treasure, ammoniaLevel):
        if not self.isAlive:
            self.posytion = self.posytion - 1
            return

        if self.feedCounter < 22 and len(food) > 0:
            if self.faceDirection == FaceDirection.LEFT      \
            and abs(self.posxtion - food[0].posxtion) < 4    \
            and abs(self.posytion - food[0].posytion) < 4:
                food[0].getEaten()
                #self.feedCounter = 122
                self.findNewDirection()
                return

            if (self.faceDirection == FaceDirection.RIGHT                          \
            and abs((self.posxtion + Fish.SPRITE_WIDTH) - food[0].posxtion) < 4    \
            and abs(self.posytion - food[0].posytion) < 4):
                food[0].getEaten()
                #self.feedCounter = 122
                self.findNewDirection()
                self.faceDirection = FaceDirection.RIGHT
                return
            
            if self.posxtion - food[0].posxtion > 4:
                self.faceDirection = FaceDirection.LEFT
                self.vxl = -4
            elif self.posxtion - food[0].posxtion < -4 and self.posxtion - food[0].posxtion > -Fish.SPRITE_WIDTH:
                self.faceDirection = FaceDirection.RIGHT
                self.vxl = -4
            elif self.posxtion - food[0].posxtion < -Fish.SPRITE_WIDTH:
                self.faceDirection = FaceDirection.RIGHT
                self.vxl = 4
            else:
                self.vxl = 0

            if abs(self.posytion - food[0].posytion) < 4:
                self.vyl = 0
            elif self.posytion - food[0].posytion < 0:
                self.vyl = 4
            else:
                self.vyl = -4

        self.posxtion = self.posxtion + self.vxl
        self.posytion = self.posytion + self.vyl
        self.moveCounter = self.moveCounter - 1
        self.feedCounter = self.feedCounter - 1

        if self.feedCounter < 0:
            self.feedCounter = 0

        if self.moveCounter <= 0:
            self.findNewDirection()
            self.moveCounter = random.randint(48, 1222)
        
        if self.posxtion < 0 and self.vxl < 0:                   # Bump from left edge
            self.vxl = random.uniform(0.12, 2.0)
            self.faceDirection = FaceDirection.RIGHT

        if self.posxtion + 220 > WINDOW_WIDTH and self.vxl > 0:  # Bump from right edge
            self.vxl = -random.uniform(0.12, 2.0)
            self.faceDirection = FaceDirection.LEFT

        if self.posytion < 0 and self.vyl < 0:                   # Bump from upper edge
            self.vyl = random.uniform(0.12, 1.0)

        if self.posytion + 140 > WINDOW_HEIGHT and self.vyl > 0: # Bump from bottom edge
            self.vyl = -random.uniform(0.12, 1.0)

        self.treasureCounter = self.treasureCounter - 1

        if self.treasureCounter <= 0:
            treasure.append(Treasure(self.posxtion + 80, self.posytion + 122))
            self.treasureCounter = random.randint(222, 422)   


    def ammoniaPoisoning(self, ammoniaLevel):
        if(self.health < ammoniaLevel):
            if self.isAlive:
                self.isAlive = False


    def isDecayed(self):
        return not self.isAlive and self.posytion < 0


    def draw(self):
        if self.isAlive:
            if self.faceDirection == FaceDirection.LEFT:
                WINDOW.blit(self.sprite1, (self.posxtion, self.posytion))
            elif self.faceDirection == FaceDirection.RIGHT:
                WINDOW.blit(self.sprite2, (self.posxtion, self.posytion))
        else:
            WINDOW.blit(self.spriteDead, (self.posxtion, self.posytion))



class Shrimp:
    sprite0right = pygame.image.load('shrimp0right.png').convert_alpha()
    sprite1right = pygame.image.load('shrimp1right.png').convert_alpha()
    sprite2right = pygame.image.load('shrimp2right.png').convert_alpha()
    sprite0left = pygame.image.load('shrimp3left.png').convert_alpha()
    sprite1left = pygame.image.load('shrimp1left.png').convert_alpha()
    sprite2left = pygame.image.load('shrimp2left.png').convert_alpha()
    spriteDead = pygame.image.load('shrimpdead.png').convert_alpha()
    SPRITE_WIDTH = 81

    def __init__(self):
        self.posxtion = random.uniform(0, WINDOW_WIDTH - 220)
        self.posytion = random.uniform(0, WINDOW_HEIGHT - 220)
        self.vxl = random.uniform(0.22, 2)
        self.vyl = random.uniform(0.22, 2)
        self.treasureCounter = random.randint(0, 212)
        self.feedCounter = 0 #random.uniform(22, 1222)
        self.moveCounter = 122
        self.treasureCounter = random.randint(1212, 2222)
        self.animationFrame = 0
        self.animationFrameOffset = random.randint(0, 2) # Random starting frame, so they don't all move in sync
        self.animationCounter = random.randint(7, 21)    # Random offset for the initial frame, so they don't all move in sync
        self.faceDirection = FaceDirection.RIGHT
        self.isJumping = False
        self.health = random.uniform(8, 68)
        self.isAlive = True


    def findNewDirection(self):
        self.vxl = random.uniform(-0.4, 0.4)
        self.vyl = random.uniform(-0.22, 0.22)
        self.isJumping = False
        
        if random.uniform(0, 1024) < 22:  # A small chance that the shrimp will violently eject itself backwards
            jumpDirection = 0
            self.isJumping = True
            if self.faceDirection == FaceDirection.RIGHT:
                jumpDirection = 1
            else:
                jumpDirection = -1
                
            self.vxl = 38 * jumpDirection
            self.vyl = random.uniform(-14, 22)
            self.moveCounter = 1
            
            if self.vxl <= 0:
                self.faceDirection = FaceDirection.RIGHT
            else:
                self.faceDirection = FaceDirection.LEFT
            return

        if self.vxl <= 0:
            self.faceDirection = FaceDirection.LEFT
        else:
            self.faceDirection = FaceDirection.RIGHT
                
        self.moveCounter = random.randint(48, 1222)
        

    def update(self, food, treasure, ammoniaLevel):
        if not self.isAlive:
            self.posytion = self.posytion - 1
            return

        self.animationCounter = self.animationCounter - 1
        if self.animationCounter <= 0:
            self.animationCounter = 14
            self.animationFrame = (self.animationFrame + 1) % 3

        if self.feedCounter < 22 and len(food) > 0:
            if self.faceDirection == FaceDirection.LEFT      \
            and abs(self.posxtion - food[0].posxtion) < 4    \
            and abs(self.posytion - food[0].posytion) < 4:
                food[0].getEaten()
                #self.feedCounter = 122
                self.findNewDirection()
                return

            if (self.faceDirection == FaceDirection.RIGHT                            \
            and abs((self.posxtion + Shrimp.SPRITE_WIDTH) - food[0].posxtion) < 4    \
            and abs(self.posytion - food[0].posytion) < 4):
                food[0].getEaten()
                #self.feedCounter = 122
                self.findNewDirection()
                self.faceDirection = FaceDirection.RIGHT
                return
            
            if self.posxtion - food[0].posxtion > 4:
                self.faceDirection = FaceDirection.LEFT
                self.vxl = -1.2
            elif self.posxtion - food[0].posxtion < -4 and self.posxtion - food[0].posxtion > -Shrimp.SPRITE_WIDTH:
                self.faceDirection = FaceDirection.RIGHT
                self.vxl = -1.2
            elif self.posxtion - food[0].posxtion < -Shrimp.SPRITE_WIDTH:
                self.faceDirection = FaceDirection.RIGHT
                self.vxl = 1.2
            else:
                self.vxl = 0

            if abs(self.posytion - food[0].posytion) < 4:
                self.vyl = 0
            elif self.posytion - food[0].posytion < 0:
                self.vyl = 1.2
            else:
                self.vyl = -1.2

        self.posxtion = self.posxtion + self.vxl
        self.posytion = self.posytion + self.vyl
        self.moveCounter = self.moveCounter - 1
        self.feedCounter = self.feedCounter - 1

        if self.feedCounter < 0:
            self.feedCounter = 0

        if self.moveCounter <= 0:
            self.findNewDirection()
            self.moveCounter = random.randint(48, 1222)
        
        if self.posxtion < 0 and self.vxl < 0:                   # Bump from left edge
            self.vxl = random.uniform(0.12, 0.8)
            self.faceDirection = FaceDirection.RIGHT
            if self.isJumping:
                self.vyl = random.uniform(0.12, 0.42)

        if self.posxtion + 220 > WINDOW_WIDTH and self.vxl > 0:  # Bump from right edge
            self.vxl = -random.uniform(0.12, 0.8)
            self.faceDirection = FaceDirection.LEFT
            if self.isJumping:
                self.vyl = random.uniform(0.12, 0.42)

        if self.posytion < 0 and self.vyl < 0:                   # Bump from upper edge
            self.vyl = random.uniform(0.12, 0.42)
            if self.isJumping:
                self.vxl = random.uniform(0.12, 0.42)

        if self.posytion + 140 > WINDOW_HEIGHT and self.vyl > 0: # Bump from bottom edge
            self.vyl = -random.uniform(0.12, 0.42)
            if self.isJumping:
                self.vxl = random.uniform(0.12, 0.42)

        self.treasureCounter = self.treasureCounter - 1

        if self.treasureCounter <= 0:
            treasure.append(Treasure(self.posxtion + 48, self.posytion + 42, True))
            self.treasureCounter = random.randint(1212, 2222)   


    def ammoniaPoisoning(self, ammoniaLevel):
        if self.health < ammoniaLevel:
            if self.isAlive:
                self.isAlive = False


    def isDecayed(self):
        return not self.isAlive and self.posytion < 0


    def draw(self):
        if self.isAlive:
            if self.faceDirection == FaceDirection.LEFT:
                if (self.animationFrame + self.animationFrameOffset) % 3 == 0:
                    WINDOW.blit(self.sprite0left, (self.posxtion, self.posytion))
                    
                if (self.animationFrame + self.animationFrameOffset) % 3 == 1:
                    WINDOW.blit(self.sprite1left, (self.posxtion, self.posytion))
                    
                if (self.animationFrame + self.animationFrameOffset) % 3 == 2:
                    WINDOW.blit(self.sprite2left, (self.posxtion, self.posytion + 1))
                
            elif self.faceDirection == FaceDirection.RIGHT:
                if (self.animationFrame + self.animationFrameOffset) % 3 == 0:
                    WINDOW.blit(self.sprite0right, (self.posxtion, self.posytion))
                    
                if (self.animationFrame + self.animationFrameOffset) % 3 == 1:
                    WINDOW.blit(self.sprite1right, (self.posxtion - 1, self.posytion))
                    
                if (self.animationFrame + self.animationFrameOffset) % 3 == 2:
                    WINDOW.blit(self.sprite2right, (self.posxtion, self.posytion + 1))
                    
        else:
            WINDOW.blit(self.spriteDead, (self.posxtion, self.posytion))



class Spark:
    def __init__(self, pxs, pys, ang, vel, size, color):
        self.posxtion = pxs
        self.posytion = pys
        self.angle = ang
        self.vel = vel
        self.size = size
        self.color = color



class Bubble:
    bubble0 = pygame.image.load('bub0.png').convert_alpha()
    bubble1 = pygame.image.load('bub1.png').convert_alpha()
    bubble2 = pygame.image.load('bub2.png').convert_alpha()
    bubble3 = pygame.image.load('bub3.png').convert_alpha()

    def __init__(self, pxs, pys, size):
        self.posxtion = pxs
        self.posytion = pys
        self.size = size
        self.sparks = []
        self.isBurst = False
        self.lifetime = 0


    def draw(self):
        if self.isBurst:
            for i in range(NUM_BURST_BUBBLES):
                pygame.draw.circle(WINDOW, (255, 255, 255), (int(self.sparks[i].posxtion), int(self.sparks[i].posytion)), self.sparks[i].size)
            return
        if self.size == 22:
            WINDOW.blit(Bubble.bubble0, (self.posxtion - self.size/2, self.posytion - self.size/2))
        elif self.size == 16:
            WINDOW.blit(Bubble.bubble1, (self.posxtion - self.size/2, self.posytion - self.size/2))
        elif self.size == 12:
            WINDOW.blit(Bubble.bubble2, (self.posxtion - self.size/2, self.posytion - self.size/2))
        elif self.size == 8:
            WINDOW.blit(Bubble.bubble3, (self.posxtion - self.size/2, self.posytion - self.size/2))


    def update(self):
        if not self.isBurst:
            self.posxtion = self.posxtion + random.uniform(-1, 1)
            self.posytion = self.posytion - 2
            return

        for i in range(NUM_BURST_BUBBLES):
            self.sparks[i].posxtion = self.sparks[i].posxtion + self.sparks[i].vel * math.sin(self.sparks[i].angle)
            self.sparks[i].posytion = self.sparks[i].posytion + self.sparks[i].vel * math.cos(self.sparks[i].angle)

        self.lifetime = self.lifetime + 1


    def burst(self):
        self.isBurst = True
        for i in range(NUM_BURST_BUBBLES):
            self.sparks.append(                       \
                Spark(                                \
                    self.posxtion,                    \
                    self.posytion,                    \
                    random.uniform(0, 2*math.pi),     \
                    random.uniform(0, 2),             \
                    1,                                \
                    2                                 \
                )                                     \
            )


    def isDecayed(self):
        if not self.isBurst:
            return self.posytion <= 0
        return self.lifetime > 22



class Treasure:
    def __init__(self, pxs, pys, isPowerup = None):
        self.posxtion = pxs
        self.posytion = pys
        self.isGotten = False
        self.isPowerup = isPowerup
        self.sparks = []
        self.color = 208
        self.isLighteningUp = True
        self.lifetime = 0


    def update(self):
        if not self.isGotten:
            self.posytion = self.posytion + 1
            if not self.isLighteningUp:
                self.color = self.color - 2
                if self.color <= 128:
                    self.isLighteningUp = True
                    
            if self.isLighteningUp:
                self.color = self.color + 2
                if self.color >= 253:
                    self.isLighteningUp = False
            return

        for i in range(NUM_EXPLOSION_PARTICLES):
            self.sparks[i].posxtion = self.sparks[i].posxtion + self.sparks[i].vel * math.sin(self.sparks[i].angle)
            self.sparks[i].posytion = self.sparks[i].posytion + self.sparks[i].vel * math.cos(self.sparks[i].angle)

        self.lifetime = self.lifetime + 1
        return
            

    def collect(self, isChainReaction = False):
        self.isGotten = True
        for i in range(NUM_EXPLOSION_PARTICLES):
            self.sparks.append(                       \
                Spark(                                \
                    self.posxtion,                    \
                    self.posytion,                    \
                    random.uniform(0, 2*math.pi),     \
                    random.uniform(0, 42),            \
                    random.randint(1, 4),             \
                    2                                 \
                )                                     \
            )


    def isDecayed(self):
        if not self.isGotten:
            return self.posytion > WINDOW_HEIGHT
        else:
            return self.lifetime > 22


    def draw(self):
        if self.isGotten:
            for i in range(NUM_EXPLOSION_PARTICLES):
                if self.isPowerup:
                    pygame.draw.circle(WINDOW, (255, 0, 0), (int(self.sparks[i].posxtion), int(self.sparks[i].posytion)), self.sparks[i].size)
                else:
                    pygame.draw.circle(WINDOW, (255, 212, 0), (int(self.sparks[i].posxtion), int(self.sparks[i].posytion)), self.sparks[i].size)
            return

        if self.isPowerup:
            pygame.draw.circle(WINDOW, (self.color, 0, 0), (int(self.posxtion), int(self.posytion)), 16)
            pygame.draw.circle(WINDOW, (188, 0, 0), (int(self.posxtion), int(self.posytion)), 12)
            pygame.draw.circle(WINDOW, (255, 255, 255), (int(self.posxtion - 4), int(self.posytion - 4)), 4)

        else:  
            pygame.draw.circle(WINDOW, (self.color, self.color - 40, 0), (int(self.posxtion), int(self.posytion)), 16)
            pygame.draw.circle(WINDOW, (188, 148, 0), (int(self.posxtion), int(self.posytion)), 12)
            pygame.draw.circle(WINDOW, (255, 255, 255), (int(self.posxtion - 4), int(self.posytion - 4)), 4)
        

class Plant:
    sprite1 = pygame.image.load('plant1.png').convert_alpha()
    sprite2 = pygame.image.load('plant1.png').convert_alpha()

    def __init__(self):
        self.numSprite = random.randint(1, 2)
        self.posxtion = random.randint(-220, WINDOW_WIDTH - 220)
        if self.numSprite == 1:
            self.posytion = random.randint(WINDOW_HEIGHT - 512, WINDOW_HEIGHT - 220)
        if self.numSprite == 2:
            self.posytion = random.randint(WINDOW_HEIGHT - 512, WINDOW_HEIGHT - 220)
        

    def draw(self):
        if self.numSprite == 1:
            WINDOW.blit(self.sprite1, (self.posxtion, self.posytion))
        if self.numSprite == 2:
            WINDOW.blit(self.sprite2, (self.posxtion, self.posytion))



class HUD:
    ammoniaBar = pygame.Rect(180, 620, 258, 22)
    filterBar = pygame.Rect(580, 620, 258, 22)
    sprite1 = pygame.image.load('nh3.png').convert_alpha()
    sprite2 = pygame.image.load('filter.png').convert_alpha()
    fontObj = pygame.font.Font(None, 27)

    def draw(self, ammoniaLevel, filterLevel, score, numFPS):
        capAmmoniaLevel = ammoniaLevel
        if ammoniaLevel > 255:
            capAmmoniaLevel = 255
        if ammoniaLevel < 0:
            capAmmoniaLevel = 0
            
        pygame.draw.rect(WINDOW, (0, 0, 0), self.ammoniaBar)
        WINDOW.blit(self.sprite1, (112, 606))
        if int(ammoniaLevel)/480.0 == 0:
            pygame.draw.rect(                                                             \
                WINDOW,                                                                   \
                (0, 255, 0),                                                              \
                pygame.Rect(182, 622, 255, 18)                                            \
            )
        else:
            pygame.draw.rect(                                                             \
                WINDOW,                                                                   \
                (min(2 * capAmmoniaLevel, 255), max(0, 255 - 2 * capAmmoniaLevel), 0),    \
                pygame.Rect(182, 622, capAmmoniaLevel, 18)                                \
            )
        textSufaceObj = self.fontObj.render(str('%.3f' %(int(ammoniaLevel) / 480.0)) + ' ppm', True, (255, 255, 255), None)
        WINDOW.blit(textSufaceObj, (260, 622))
        pygame.draw.rect(WINDOW, (0, 0, 0), self.filterBar)
        WINDOW.blit(self.sprite2, (508, 598))
        pygame.draw.rect(                                                                 \
            WINDOW,                                                                       \
            (255 - filterLevel * 255.0/80.0, filterLevel * 255.0 / 80.0, 0),              \
            pygame.Rect(582, 622, filterLevel * 255.0 / 80.0, 18)                         \
        )
        textSufaceObj = self.fontObj.render(str('%.3f' %(filterLevel * 100.0 / 80.0)) + ' %', True, (255, 255, 255), None)
        WINDOW.blit(textSufaceObj, (670, 622))
        textSufaceObj = self.fontObj.render('%.i' %(score) + ' $', True, (255, 255, 255), None)
        pygame.draw.circle(WINDOW, (168, 168, 0), (1140, 40), 16)
        pygame.draw.circle(WINDOW, (188, 148, 0), (1140, 40), 12)
        pygame.draw.circle(WINDOW, (255, 255, 255), (1140 - 4, 40 - 4), 4)
        WINDOW.blit(textSufaceObj, (1172, 31))
        textSufaceObj = self.fontObj.render(str('%.1f' %(numFPS)) + ' fps', True, (255, 255, 255), None)
        WINDOW.blit(textSufaceObj, (970, 622))

        

class Aquarium:
    MEMORY_LENGTH = 480
    FILTER_MAX_CAP = 80.0

    def __init__(self):
        self.filterHealth = 0.0
        self.historyAmmonia = collections.deque(maxlen = Aquarium.MEMORY_LENGTH)
        self.fish = []
        self.food = []
        self.foodSparks = []
        self.treasure = []
        self.plants = []
        self.ammoniaLevel = 0.0
        self.algaeLevel = 0.0
        self.shrimp = []
        self.bubbles = []
        self.score = 40
        self.isDemo = False
        self.ammoniaTimeCounter = 0.0
        self.numPlants = 0
        self.bubbleTimeCounter = 122
        self.maxAmmonia = 0.0
        self.hud = HUD()
        self.clock = pygame.time.Clock()


    def updateDraw(self):
        self.drawBackground()
        self.drawPlants()
        self.updateDrawFish()
        if self.isDemo:
            self.updateDrawBubbles()
            self.drawTitle()
            return
        self.updateDrawShrimp()
        self.updateDrawBubbles()
        self.updateAmmoniaLevel()
        self.updateAlgaeLevel()
        self.updateDrawFood()
        self.updateDrawTreasure()
        self.updateDrawFoodSparks()
        self.applyAmmonia()
        self.cleanDecays()
        self.drawHUD()


    def drawTitle(self):
        splash = pygame.image.load('splash_a.png').convert_alpha()
        WINDOW.blit(splash, (170, -12))


    def addFood(self):
        if self.score >= 2:
            self.food.append(Food(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            self.score = self.score - 0#2


    def addFish(self):
        if self.score >= 40:
            self.fish.append(Fish())
            self.score = self.score - 0#80


    def addPlant(self):
        if self.score >= 2:
            self.plants.append(Plant())
            self.score = self.score - 0#2


    def addShrimp(self):
        if self.score >= 4:
            self.shrimp.append(Shrimp())
            self.score = self.score - 0#4


    def addBubbles(self):
        self.bubbleTimeCounter = self.bubbleTimeCounter - 1
        if self.bubbleTimeCounter <= 0:
            self.bubbleTimeCounter = random.randint(422,848)#(422,1242)
            numBubbles = random.randint(4, 22)
            newPosxtion = random.randint(0, WINDOW_WIDTH)
            for i in range(numBubbles):
                choice = random.uniform(0,1024)
                if choice >= 948:
                    self.bubbles.insert(0, Bubble(0, 0, 22))
                elif 712 <= choice < 948:
                    self.bubbles.insert(0, Bubble(0, 0, 16))
                elif 312 <= choice < 712:
                    self.bubbles.insert(0, Bubble(0, 0, 12))
                else:
                    self.bubbles.insert(0, Bubble(0, 0, 8))
                    
                self.bubbles[0].posxtion = newPosxtion + random.uniform(-38, 38)
                self.bubbles[0].posytion = WINDOW_HEIGHT + 42*i + random.uniform(0, 22)

            


    def addHistoryPoint(self, ammoniaLevel):
        self.historyAmmonia.append(ammoniaLevel)
        self.saveHighest()


    def getFilterHealth(self):  #TODO - Find an actually good formula that doesn't suck ballz
        return min(max(sum(self.historyAmmonia)/Aquarium.MEMORY_LENGTH, self.maxAmmonia/Aquarium.MEMORY_LENGTH), Aquarium.FILTER_MAX_CAP)


    def saveHighest(self):
        if sum(self.historyAmmonia) > self.maxAmmonia:
            self.maxAmmonia = sum(self.historyAmmonia)


    def createDemo(self):
        self.isDemo = True
        
        self.fish.append(Fish())
        self.fish.append(Fish())
        
        self.plants.append(Plant())
        self.plants.append(Plant())
        self.plants.append(Plant())
        self.plants.append(Plant())
        self.plants.append(Plant())
        self.plants.append(Plant())
        self.plants.append(Plant())
        self.plants.append(Plant())
        
        self.plants[0].posxtion = -120
        self.plants[0].posytion = 322

        self.plants[1].posxtion = 220
        self.plants[1].posytion = 222

        self.plants[2].posxtion = 480
        self.plants[2].posytion = 248

        self.plants[3].posxtion = 730
        self.plants[3].posytion = 322

        self.plants[4].posxtion = -80
        self.plants[4].posytion = 282

        self.plants[5].posxtion = 140
        self.plants[5].posytion = 322

        self.plants[6].posxtion = 580
        self.plants[6].posytion = 308

        self.plants[7].posxtion = 810
        self.plants[7].posytion = 322


    def drawBackground(self):
        WINDOW.fill((0, min(68 + self.algaeLevel/4.0, 168), max(148 - self.algaeLevel/4.0, 42)))


    def drawPlants(self):
        self.numPlants = 0
        for i in self.plants:
            i.draw()
            self.numPlants = self.numPlants + 1   
        self.algaeLevel = self.algaeLevel - self.numPlants * 12.0 * (self.getFilterHealth()**2 / 12000)
        if self.algaeLevel < 0:
           self.algaeLevel = 0


    def updateDrawFish(self):
        self.numFish = 0
        for i in self.fish:
            i.update(self.food, self.treasure, self.ammoniaLevel)
            i.draw()
            self.numFish = self.numFish + 1


    def updateDrawShrimp(self):
        self.numShrimp = 0
        for i in self.shrimp:
            i.update(self.food, self.treasure, self.ammoniaLevel)
            i.draw()
            self.numShrimp = self.numShrimp + 1


    def updateDrawFood(self):
        for i in self.food:
            i.update()
            i.draw()
            if i.isDecayed():
                self.ammoniaLevel = self.ammoniaLevel + 1


    def updateDrawTreasure(self):
        for i in self.treasure:
            i.update()
            i.draw()
            if not i.isGotten and i.isDecayed():
                self.score = self.score + 1


    def updateDrawFoodSparks(self):
        for index, item in enumerate(self.food):
            if item.eaten:
                self.foodSparks.append(self.food.pop(index))
        for i in self.foodSparks:
            i.update()
            i.draw()

            
    def updateDrawBubbles(self):
        self.addBubbles()
        for i in self.bubbles:
            i.update()
            i.draw()


    def applyAmmonia(self):
        for i in self.fish:
            i.ammoniaPoisoning(self.ammoniaLevel)
        for i in self.shrimp:
            i.ammoniaPoisoning(self.ammoniaLevel)


    def cleanDecays(self):
        self.food[:]       = [i for i in self.food       if not i.isDecayed()]
        self.fish[:]       = [i for i in self.fish       if not i.isDecayed()]
        self.shrimp[:]     = [i for i in self.shrimp     if not i.isDecayed()]
        self.bubbles[:]    = [i for i in self.bubbles    if not i.isDecayed()]
        self.treasure[:]   = [i for i in self.treasure   if not i.isDecayed()]
        self.foodSparks[:] = [i for i in self.foodSparks if not i.isDecayed()]
        

    def updateAmmoniaLevel(self):
        self.ammoniaLevel = self.ammoniaLevel + (self.numFish * fishAmmoniaImpact + self.numShrimp * shrimpAmmoniaImpact)
        self.ammoniaLevel = self.ammoniaLevel * 0.99991 - (self.getFilterHealth()**2 / 12000)
        if self.ammoniaLevel < 0:
            self.ammoniaLevel = 0
            
        dt = self.clock.tick() 
        self.ammoniaTimeCounter += dt
        if self.ammoniaTimeCounter > 1000:
            self.addHistoryPoint(self.ammoniaLevel)
            self.ammoniaTimeCounter = 0


    def updateAlgaeLevel(self):
        self.algaeLevel = self.algaeLevel - self.numShrimp * 12.0 * (self.getFilterHealth()**2 / 12000)
        self.algaeLevel = self.algaeLevel + self.numFish * (self.getFilterHealth()**2 / 12000)
        if self.algaeLevel < 0:
            self.algaeLevel = 0


    def burstBubbles(self):
        for i in self.bubbles:
            if abs(pygame.mouse.get_pos()[0] - i.posxtion) < i.size/2    \
            and abs(pygame.mouse.get_pos()[1] - i.posytion) < i.size/2:
                i.burst()
                

    def drawHUD(self):
        self.hud.draw(self.ammoniaLevel, self.getFilterHealth(), self.score, self.clock.get_fps())
        

    def collectTreasure(self):
        for i in self.treasure:
            if (abs(pygame.mouse.get_pos()[0] - i.posxtion)) < 16 and abs((pygame.mouse.get_pos()[1] - i.posytion)) < 16:
                i.collect()
                self.score = self.score + 10
                if i.isPowerup:
                    for f in self.treasure:
                        f.collect(True)
                        if f.isPowerup:
                            continue
                        self.score = self.score + 4
                    break


class GameState(Enum):
    PLAYING = 0
    MENU = 1


GAME_STATE = GameState.MENU


class MenuItem(Enum):
    NEW_GAME = 0
    QUIT = 1
    HELP = 2
    CREDITS = 3



class MenuState(Enum):
    MAIN = 0
    HELP_SCREEN = 1
    CREDITS_SCREEN = 2
    NONE = -1


class Menu:
    fontObj = pygame.font.SysFont('Century Gothic', 62)
    smallFont = pygame.font.SysFont('Century Gothic', 14)
    menuBackgroundColor = (0, 48, 48)
    newlineInterval = 22
    colorActive = (0xFF, 0xA0, 0x00)
    colorInactive = (255, 255, 255)
    newGamePos = (468, 222)
    creditsPos = (522, 382)
    helpPos = (562, 302)
    quitPos = (562, 462)
    backPos = (562, 548)
    helpContentsPos = (48, 222)
    creditsContentsPos = (338, 242)
    fontHeight = 62

    def __init__(self):
        self.menuState = MenuState.MAIN

        
    def draw(self):
        if self.menuState == MenuState.MAIN:
            if Menu.newGamePos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.newGamePos[1] + Menu.fontHeight + 14:   
                textSufaceObj = self.fontObj.render('New Game', True, Menu.colorActive, None)
            else:
                textSufaceObj = self.fontObj.render('New Game', True, Menu.colorInactive, None)
            WINDOW.blit(textSufaceObj, Menu.newGamePos)

            if Menu.helpPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.helpPos[1] + Menu.fontHeight + 14:   
                textSufaceObj = self.fontObj.render('Help', True, Menu.colorActive, None)
            else:
                textSufaceObj = self.fontObj.render('Help', True, Menu.colorInactive, None)
            WINDOW.blit(textSufaceObj, Menu.helpPos)

            if Menu.creditsPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.creditsPos[1] + Menu.fontHeight + 14:   
                textSufaceObj = self.fontObj.render('Credits', True, Menu.colorActive, None)
            else:
                textSufaceObj = self.fontObj.render('Credits', True, Menu.colorInactive, None)
            WINDOW.blit(textSufaceObj, Menu.creditsPos)
        
            if Menu.quitPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.quitPos[1] + Menu.fontHeight + 14:
                textSufaceObj = self.fontObj.render('Quit', True, Menu.colorActive, None)
            else:
                textSufaceObj = self.fontObj.render('Quit', True, Menu.colorInactive, None)
            WINDOW.blit(textSufaceObj, Menu.quitPos)

        elif self.menuState == MenuState.HELP_SCREEN:
            pygame.draw.rect(WINDOW, Menu.menuBackgroundColor, pygame.Rect(22, 198, 1238, 342), 0)
            
            textSufaceObj = self.smallFont.render(
                'The objective of the game is to stabilize and maintain a healthy aquarium and take care of the inhabiting animals.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, Menu.helpContentsPos)
            
            textSufaceObj = self.smallFont.render(
                'Use the left mouse button in order to collect treasure dropped by the animals.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 2*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'Use the right mouse button in order to feed the animals.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 3*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'Press [X] in order to purchase a new gourami fish.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 4*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'Press [S] in order to purchase a new cherry shrimp.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 5*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'Press [P] in order to purchase a new plant.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 6*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'Ammonia (NH3) is a toxic waste product of fish’s metabolism and food’s decomposition. '       \
                + 'Excessive ammonia concentration is harmful to the aquarium’s inhabitants.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 8*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'The aquarium contains an off-screen filter, which automatically works to remove ammonia.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 9*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'The filter’s efficiency of ammonia removal is very low at the beginning. '                  \
                + 'However, it gets more efficient over time, as it consumes ammonia.',
                True,
                Menu.colorInactive,
            
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 10*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'Try not to overwhelm your filter’s current capacity and do not introduce too many new animals all at once.',
                True,
                Menu.colorInactive,
            
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 11*Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                'If the aquarium water turns green, that is an algae bloom. Introduce some plants and/or shrimps to the aquarium.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.helpContentsPos, (0, 12*Menu.newlineInterval)))))

            if Menu.backPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.backPos[1] + Menu.fontHeight + 14:
                textSufaceObj = self.fontObj.render('Back', True, Menu.colorActive, None)
            else:
                textSufaceObj = self.fontObj.render('Back', True, Menu.colorInactive, None)
            WINDOW.blit(textSufaceObj, Menu.backPos)

        elif self.menuState == MenuState.CREDITS_SCREEN:
            pygame.draw.rect(WINDOW, Menu.menuBackgroundColor, pygame.Rect(288, 222, 708, 148), 0)
            
            textSufaceObj = self.smallFont.render(
                'Maya’s Aquarium -- version 0.3',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, Menu.creditsContentsPos)
            
            textSufaceObj = self.smallFont.render(
                'Made in the loving memory of Maya the Cat, who passed away on March 26th, 2024.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.creditsContentsPos, (0, Menu.newlineInterval)))))

            textSufaceObj = self.smallFont.render(
                '                                                                           '   \
                + '                                                                  -- P.B.',
                True,
                Menu.colorInactive,
                None
            )
            WINDOW.blit(textSufaceObj, tuple(map(sum,zip(Menu.creditsContentsPos, (0, 3*Menu.newlineInterval)))))

            if Menu.backPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.backPos[1] + Menu.fontHeight + 14:
                textSufaceObj = self.fontObj.render('Back', True, Menu.colorActive, None)
            else:
                textSufaceObj = self.fontObj.render('Back', True, Menu.colorInactive, None)
            WINDOW.blit(textSufaceObj, Menu.backPos)

    def interact(self):
        if self.menuState == MenuState.MAIN:
            if Menu.newGamePos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.newGamePos[1] + Menu.fontHeight + 14:  
                return MenuItem.NEW_GAME
            if Menu.quitPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.quitPos[1] + Menu.fontHeight + 14:
                return MenuItem.QUIT
            if Menu.helpPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.helpPos[1] + Menu.fontHeight + 14:
                self.menuState = MenuState.HELP_SCREEN
                return MenuItem.HELP
            if Menu.creditsPos[1] <= pygame.mouse.get_pos()[1] < Menu.creditsPos[1] + Menu.fontHeight + 14:
                self.menuState = MenuState.CREDITS_SCREEN
                return MenuItem.CREDITS
            
        if self.menuState == MenuState.CREDITS_SCREEN or self.menuState == MenuState.HELP_SCREEN:
            if Menu.backPos[1] + 14 <= pygame.mouse.get_pos()[1] < Menu.backPos[1] + Menu.fontHeight + 14:
                self.menuState = MenuState.MAIN
                return None
    
        
# The main function that controls the game
def main () :
    looping = True
    aquarium = Aquarium()
    demo = Aquarium()
    demo.createDemo()
    global GAME_STATE
    aquarium.fish.append(Fish())
    aquarium.fish.append(Fish())
    aquarium.shrimp.append(Shrimp())
    menu = Menu()
        
    while looping:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and GAME_STATE == GameState.PLAYING:
                if event.button == 3:
                    aquarium.addFood()
                if event.button == 1:
                    aquarium.collectTreasure()
                    aquarium.burstBubbles()

            if event.type == pygame.MOUSEBUTTONDOWN and GAME_STATE == GameState.MENU and event.button == 1:
                if menu.interact() == MenuItem.NEW_GAME:
                    GAME_STATE = GameState.PLAYING
                if menu.interact() == MenuItem.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.KEYDOWN and GAME_STATE == GameState.PLAYING:
                if (pygame.key.get_pressed()[K_x]):
                    aquarium.addFish()
                if (pygame.key.get_pressed()[K_p]):
                    aquarium.addPlant()
                if (pygame.key.get_pressed()[K_s]):
                    aquarium.addShrimp()
                if (pygame.key.get_pressed()[K_ESCAPE]):
                    GAME_STATE = GameState.MENU
                    aquarium = Aquarium()
                
        if GAME_STATE == GameState.PLAYING:
            aquarium.updateDraw() 

        if GAME_STATE == GameState.MENU:
            demo.updateDraw()
            menu.draw()
        
        pygame.display.update()
        fpsClock.tick(FPS)
 
main()












