import pygame, math, os, random
from pygame.locals import *
from PIL import *

pygame.init()

def path_assets(fichier):

    return os.path.join('assets', fichier)

Window_size = (1280,720)
Window = pygame.display.set_mode(Window_size)

Menu = pygame.image.load(path_assets("Menu.png")).convert()
Background = pygame.image.load(path_assets("Black_screen.jpg")).convert()
RacketLimg = pygame.image.load(path_assets("Racket.png")).convert()
RacketRimg = RacketLimg
Ballimg = pygame.image.load(path_assets("Ball.png")).convert()
H_wall = pygame.image.load(path_assets("WallHorizontal.png")).convert()
V_wall = pygame.image.load(path_assets("WallVertical.png")).convert()
Icon = pygame.image.load(path_assets("Icon.png")).convert()

Backgroung_rect = pygame.Rect((1,1), (1279, 719))
H_wall_rect1 = pygame.Rect((0,0), (1280, 4))
H_wall_rect2 = pygame.Rect((0,716), (1280,720))
V_wall_rect1 = pygame.Rect((0,0), (3, 720))
V_wall_rect2 = pygame.Rect((1277,0), (1280,720))

Ball = Ballimg
Ball = {'rect' : Ball.get_rect(center = (639, 359)),
        'speed' : (0,0)}
Ball['pos'] = Ball['rect'].topleft

RacketL = RacketLimg
RacketL = { 'rect' : RacketL.get_rect(center = (5, 360)),
            'speed' : (0, 0)}
RacketL['pos'] = RacketL['rect'].topleft

RacketR = RacketRimg
RacketR = { 'rect' : RacketR.get_rect(center = (1275, 360)),
            'speed' : (0, 0)}
RacketR['pos'] = RacketR['rect'].topleft

def Mouvement (Obj, vitesse):

    vx, vy = vitesse
    Obj['speed'] = (vx, vy)

    return Obj['speed']

def Position (Obj) :

    vx, vy = Obj['speed']
    x, y = Obj['pos']
    x += vx
    y += vy
    Obj['pos'] = (x, y)
    Obj['rect'].topleft = (x, y)

def Delimitation (Obj, Zone) :

    x, y = Obj['pos']
    largeur, hauteur = Obj['rect'].size

    if x < Zone.left :
        x = Zone.left
    elif x + largeur > Zone.right :
        x = Zone.right - largeur
    if y < Zone.top :
        y = Zone.top
    elif y + hauteur > Zone.bottom :
        y = Zone.bottom - hauteur

    Obj['pos'] = (x,y)
    Obj['rect'].topleft = (x,y)

pygame.display.set_caption("Py Pong")
pygame.mouse.set_visible(False)
pygame.display.set_icon(Icon)

font = pygame.font.Font(path_assets("pongfont.ttf"), 100)

Continue = 1

BMvmtx = 0
BMvmty = 0
Mvmtupple = (BMvmtx, BMvmty)

start = 2
Score_P1 = 0
Score_P2 = 0
speedup = 0

BMxsave = 0
BMysave = 0


while Continue == 1 :

    for event in pygame.event.get() :

        if event.type == KEYDOWN :

            if event.key == K_ESCAPE or event.type == QUIT :

                Continue = 0

    Window.blit(Background, (0, 0))
    Window.blit(RacketLimg, RacketL['rect'])
    Window.blit(RacketRimg, RacketR['rect'])
    Window.blit(Ballimg, Ball['rect'])
    Window.blit(H_wall, (0,0))
    Window.blit(H_wall, (0,716))
    Window.blit(V_wall, (0,0))
    Window.blit(V_wall, (1277,0))

    Delimitation(RacketL, Backgroung_rect)
    Delimitation(RacketR, Backgroung_rect)
    Delimitation(Ball, Backgroung_rect)

    if event.type == KEYDOWN :

        if event.key == K_z :

            Mouvement(RacketL, (0,-2))

        if event.key == K_DOWN :

            Mouvement(RacketR, (0, 2))

        if event.key == K_UP :

            Mouvement(RacketR, (0,-2))

        if event.key == K_s :

            Mouvement(RacketL, (0, 2))

    if event.type == KEYUP :

        if event.key == K_z or event.key == K_s :

            Mouvement(RacketL, (0,0))

        if event.key == K_UP or event.key == K_DOWN :

            Mouvement(RacketR, (0,0))

    if start == 2 :

        Window.blit(Menu, (0,0))

        if event.type == KEYDOWN :

                start = 0

    if start == 0 :

        BMvmtx = BMxsave
        BMvmty = BMysave
        speedup = 0

        if event.type == KEYDOWN :

            if event.key == K_SPACE :

                Mouvement(Ball, (BMvmtx, BMvmty))
                start = 1
                Position(Ball)

            BMvmtx = random.randint(-1, 1)
            BMvmty = random.randint(-1, 1)

            while BMvmtx == 0 or BMvmty == 0 :

                while BMvmtx == 0 :

                    BMvmtx = random.randint(-1, 1)

                while BMvmty == 0 :

                    BMvmty = random.randint(-1, 1)

            BMxsave = BMvmtx
            BMysave = BMvmty

    if start == 1 :

        if Ball['rect'].colliderect(RacketL['rect']) or Ball['rect'].colliderect(RacketR['rect']) :
            BMvmtx = BMvmtx * -1
            BMvmty = BMvmty * 1
            speedup = speedup + 1

        if Ball['rect'].colliderect(H_wall_rect1) or Ball['rect'].colliderect(H_wall_rect2):

            BMvmtx = BMvmtx * 1
            BMvmty = BMvmty * -1

        if Ball['rect'].colliderect(V_wall_rect1) :

            Score_P2 = Score_P2 + 1
            start = 0
            Ball['pos'] = (640, 360)

        if Ball['rect'].colliderect(V_wall_rect2) :

            Score_P1 = Score_P1 + 1
            start = 0
            Ball['pos'] = (640, 360)

        if speedup == 5 :

            BMvmtx += BMvmtx
            BMvmty += BMvmty
            speedup = 0

        Mouvement(Ball, (BMvmtx, BMvmty))
        Position(Ball)

        Position(RacketL)
        Position(RacketR)

        if Score_P1 == 5 or Score_P2 == 5 :

            start = 3

    if start == 3 :

        if Score_P1 == 5 :

            winner = str("Player 1")

        if Score_P2 == 5 :

            winner = str("Player 2")

        if event.type == KEYDOWN :

            if event.key == K_RETURN :

                start = 2
                Score_P1 = 0
                Score_P2 = 0

        Pwin = font.render(winner, 1, (255, 255, 255))
        Window.blit(Pwin, (340, 260))
        Wins = font.render(str("Wins"), 1, (255, 255, 255))
        Window.blit(Wins, (540, 560))

    ScoreP1 = font.render(str(Score_P1), 1, (255, 255, 255))
    ScoreP2 = font.render(str(Score_P2), 1, (255, 255, 255))
    Window.blit(ScoreP1, (360,50))
    Window.blit(ScoreP2, (870,50))

    pygame.display.flip()

pygame.quit()
