import random
import shelve
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("Background.png").convert()
BACKGROUND2 = pygame.image.load("Background.png").convert()
MIDGROUND = pygame.image.load("Midground.png").convert_alpha()
MIDGROUND2 = pygame.image.load("Midground.png").convert_alpha()
FOREGROUND = pygame.image.load("Foreground.png").convert_alpha()
FOREGROUND2 = pygame.image.load("Foreground.png").convert_alpha()

pygame.display.set_caption("Side Scroller")

CLOCK = pygame.time.Clock()
BGX = 0
BGX2 = BACKGROUND.get_width()
FGX = 0
FGX2 = FOREGROUND.get_width()
MGX = 0
MGX2 = MIDGROUND.get_width()
score = 0

DGREY = (100, 100, 100)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

JUMPTIME = 15


class player(object):
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
        self.jumpTime = JUMPTIME
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
            if self.jumpTime >= -JUMPTIME:
                neg = 1
                if self.jumpTime < 0:
                    neg = -1
                    if onFloor:
                        self.jumping = False
                if self.jumping:
                    self.y -= self.jumpTime ** 2 * 0.10 * neg
                    self.jumpTime -= 1
                else:
                    self.jumpTime = JUMPTIME
            else:
                self.jumping = False
                self.jumpTime = JUMPTIME


class floor(object):
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
    SCREEN.blit(BACKGROUND, (BGX, 0))
    SCREEN.blit(BACKGROUND, (BGX2, 0))
    SCREEN.blit(MIDGROUND, (MGX, 0))
    SCREEN.blit(MIDGROUND, (MGX2, 0))
    SCREEN.blit(FOREGROUND, (FGX, 0))
    SCREEN.blit(FOREGROUND, (FGX2, 0))
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
    floors.append(floor(0, HEIGHT / 2, WIDTH, 20))
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
        
        SCREEN.blit(restart, (WIDTH / 2 - restart.get_width() /2, HEIGHT / 2 + HEIGHT / 3))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending = False
                run = False
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_ESCAPE]):
            ending = False

    score = 0


font = pygame.font.SysFont("courier", 30, True)
man = player(200, 150, 64, 64)

run = True
FPS = 60
onFloor = True

floors = []

pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
floors.append(floor(0, HEIGHT / 2, WIDTH, 20))


while run:
    CLOCK.tick(FPS)
    MGX -= 3
    MGX2 -= 3
    FGX -= 5
    FGX2 -= 5
    impeded = False
    ouch = False
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
            jumpTime = JUMPTIME
            ouch = True

        if newfloor.x < 0 - newfloor.width:
            floors.pop(floors.index(newfloor))
            onFloor = True

    if not onFloor and not man.jumping:
        man.y += 15

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
                floor(
                    WIDTH,
                    newY,
                    random.randrange(WIDTH - WIDTH / 4, WIDTH),
                    random.randrange(5, 20),
                )
            )

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and man.x < WIDTH - man.v and not impeded:
        man.x += man.v

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.v
        man.sliding = False

    if keys[pygame.K_SPACE] or keys[pygame.K_UP] and not ouch:
        if onFloor:
            man.jumping = True

    if MGX < MIDGROUND.get_width() * -1:
        MGX = MIDGROUND2.get_width()

    if MGX2 < MIDGROUND.get_width() * -1:
        MGX2 = MIDGROUND2.get_width()

    if FGX < BACKGROUND.get_width() * -1:
        FGX = BACKGROUND.get_width()

    if FGX2 < BACKGROUND.get_width() * -1:
        FGX2 = BACKGROUND.get_width()

    man.jump()
    redrawGameWindow()

    if man.y > HEIGHT:
        endScreen()
