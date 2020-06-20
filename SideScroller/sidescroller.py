import random
import shelve
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Side Scroller")

CLOCK = pygame.time.Clock()

score = 0

DGREY = (100, 100, 100)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

JUMPTIME = 25
GRAVITY = 5


class Background():
    def __init__(self, x, image):
        self.image = image
        self.xOne = 0
        self.xTwo = image.get_width()

    def checkBackgroundOffscreen(self):
        if self.xOne < self.image.get_width()*-1:
            self.xOne = self.image.get_width()
        if self.xTwo < self.image.get_width()*-1:
            self.xTwo = self.image.get_width()


class Player():
    runSkins = [
        pygame.image.load("C1.png"),
        pygame.image.load("C2.png"),
        pygame.image.load("C3.png"),
        pygame.image.load("C4.png"),
    ]
    jumpSkin = pygame.image.load("J3.png")

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.jumping = False
        self.sliding = False
        self.width = width
        self.height = height
        self.v = 5
        self.slideUp = False
        self.jumptime = JUMPTIME
        self.slideTime = 20
        self.runCount = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 60)
        self.bottom = pygame.Rect(self.x, self.rect.bottom, 50, 10)
        self.right = pygame.Rect(self.rect.right, self.y, 1, 40)
        self.top = pygame.Rect(self.x, self.y, 50, 1)

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, 40, 50)
        self.bottom = pygame.Rect(self.x, self.rect.bottom, 50, 10)
        self.right = pygame.Rect(self.rect.right, self.y, 1, 40)
        self.top = pygame.Rect(self.x, self.y, 50, 1)

        if self.jumping:
            SCREEN.blit(self.jumpSkin, (self.x, self.y))

        elif self.sliding or self.slideUp:
            SCREEN.blit(self.slideSkin, (self.x, self.y))

        else:
            if self.runCount >= 16:
                self.runCount = 0
            SCREEN.blit(self.runSkins[self.runCount // 4], (self.x, self.y))
            self.runCount += 1

    def jump(self):
        if self.jumping:
            if self.jumptime >= -JUMPTIME:
                neg = 1
                if self.jumptime < 0:
                    neg = -1
                    if onFloor:
                        self.jumping = False
                if self.jumping:
                    self.y += GRAVITY - self.jumptime ** 2 * (1/JUMPTIME) * neg
                    self.jumptime -= 1
                else:
                    self.jumptime = JUMPTIME
            else:
                self.jumping = False
                self.jumptime = JUMPTIME


class Floor(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(SCREEN, DGREY, self.rect)


def redrawGameWindow():
    SCREEN.blit(background.image, (background.xOne, 0))
    SCREEN.blit(background.image, (background.xTwo, 0))
    SCREEN.blit(midground.image, (midground.xOne, 0))
    SCREEN.blit(midground.image, (midground.xTwo, 0))
    SCREEN.blit(foreground.image, (foreground.xOne, 0))
    SCREEN.blit(foreground.image, (foreground.xTwo, 0))
    for nfloor in floors:
        nfloor.draw(SCREEN)
    man.draw(SCREEN)
    text = font.render("Score: " + str(score), 1, BLACK)
    text_width, text_height = font.size("Score: " + str(score))
    SCREEN.blit(text, (WIDTH - text_width, 10))

    pygame.display.update()


def endScreen():
    global score, FPS, floors, run
    d = shelve.open("score.txt")
    if score > d["score"]:
        d["score"] = score
        highscore = score
    else:
        highscore = d["score"]
    d.close()
    pygame.time.delay(100)
    ending = True
    FPS = 60
    floors = []
    man.x, man.y = 200, 150
    floors.append(Floor(0, HEIGHT / 2, WIDTH, 20))
    SCREEN.fill(BLACK)
    while ending:
        largeFont = pygame.font.SysFont("courier", 80)
        youDied = largeFont.render("You died.", 1, WHITE)
        medFont = pygame.font.SysFont("courier", 55)
        lastScore = medFont.render("With a score of " + str(score), 1, WHITE)
        smolFont = pygame.font.SysFont("arial", 20)
        highScore = smolFont.render("Highscore: " + str(highscore), 1, WHITE)
        newHighScore = smolFont.render("New High Score!", 1, WHITE)
        restart = smolFont.render("Press space to restart", 1, WHITE)

        SCREEN.blit(youDied, (WIDTH / 2 - youDied.get_width() / 2, HEIGHT / 2 - HEIGHT / 4))
        SCREEN.blit(lastScore, (WIDTH / 2 - lastScore.get_width() / 2, HEIGHT / 2))

        if highscore > score:
            SCREEN.blit(highScore, (WIDTH / 2 - highScore.get_width() / 2, HEIGHT / 2 + HEIGHT / 4),)
        else:
            SCREEN.blit(newHighScore, (WIDTH / 2 - newHighScore.get_width() / 2, HEIGHT / 2 + HEIGHT / 4),)

        SCREEN.blit(restart, (WIDTH / 2 - restart.get_width() / 2, HEIGHT / 2 + HEIGHT / 3))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending = False
                run = False
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_ESCAPE]):
            ending = False

    score = 0


foreground = Background(0, pygame.image.load("Foreground.png").convert_alpha())
midground = Background(0, pygame.image.load("Midground.png").convert_alpha())
background = Background(0, pygame.image.load("Background.png").convert())

font = pygame.font.SysFont("courier", 30, True)
man = Player(200, 150, 64, 64)

run = True
FPS = 60
onFloor = True

floors = []

pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
floors.append(Floor(0, HEIGHT / 2, WIDTH, 20))


while run:
    CLOCK.tick(FPS+score)
    midground.xOne -= 3
    midground.xTwo -= 3
    foreground.xOne -= 5
    foreground.xTwo -= 5
    impeded = False
    impededAbove = False
    onFloor = False

    for newfloor in floors:
        newfloor.x -= 5

        if man.bottom.colliderect(newfloor.rect):
            onFloor = True
            man.rect.bottom = newfloor.rect.top
            man.y = man.rect.top

        if man.right.colliderect(newfloor.rect):
            man.y -= 5
            impeded = True

        elif man.top.colliderect(newfloor.rect):
            jumping = False
            jumptime = JUMPTIME
            impededAbove = True

        if newfloor.x < 0 - newfloor.width:
            floors.pop(floors.index(newfloor))
            onFloor = True

    if not onFloor and not man.jumping:
        man.y += GRAVITY

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.USEREVENT + 1:
            FPS += 0.5
            score += 1

        if len(floors) < 2:
            lastY = floors[-1].y
            if lastY > HEIGHT - 100:
                newY = random.randrange(lastY - 100, HEIGHT) / 5 * 5
            elif lastY < 100:
                newY = random.randrange(100, lastY + 100)
            else:
                newY = random.randrange(lastY - 100, lastY + 100) / 5 * 5

            floors.append(
                Floor(
                    WIDTH,
                    newY,
                    random.randrange(WIDTH - WIDTH / 6, WIDTH),
                    20
                )
            )

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and man.x < WIDTH - man.v and not impeded:
        man.x += man.v

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.v
        man.sliding = False

    if keys[pygame.K_SPACE] or keys[pygame.K_UP] and not impededAbove:
        if onFloor:
            man.jumping = True

    midground.checkBackgroundOffscreen()
    foreground.checkBackgroundOffscreen()

    man.jump()
    redrawGameWindow()

    if man.y > HEIGHT:
        endScreen()