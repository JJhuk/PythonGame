
import pygame
from pygame.color import Color
import random
from UFO_class import UFO
from Boss_class import BOSS
from time import sleep
from UFO_Monster import UFO_MONSTER
from Meteor import METEOR


FPS = 28
pad_width = 800
pad_height = 200
background_width = 800
WHITE = (255,255,255)



def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def runGame():
    global background1,background2,UFO1,clock,boss,UFO_Monster
    global bullet,meteors

    
    font = pygame.font.Font("D2coding.ttf",20)
     
    bullet_xy = []

    isShotBoss = False
    isShotUFO = False
    isShotMeteor = False
 
    crashed = False
    clock = pygame.time.Clock()

   # UFO1.rect.x = pad_width * 0.05
    UFO1.rect.y = 120
    UFO1.rect.x = 50
    boss.rect.x = 550
    boss.rect.y = 0

    meteor_x = pad_width
    meteor_y = random.randrange(0,pad_height)
    random.shuffle(meteors)
    meteor = meteors[0]

    UFO_Monster.rect.x = pad_width
    UFO_Monster.rect.y = random.randrange(0,pad_height)

    UFO1_y_change = 0
    UFO1_x_change = 0

    background1_x = 0
    background2_x = background_width

    # 게임 루프
    while not crashed:

        #시간에 따른 점수 + 폰트 출력
       
        time = pygame.time.get_ticks() // 1000
        textSurface = font.render("Time : "+str(time), True,(216,216,216))
        textRect = textSurface.get_rect()
        textRect.center = (80,20)

        plus_score = 0

        # 1) 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    UFO1_y_change = -UFO1.speed
                elif event.key == pygame.K_DOWN:
                    UFO1_y_change = UFO1.speed  
                elif event.key == pygame.K_RIGHT:
                    UFO1_x_change = UFO1.speed
                elif event.key == pygame.K_LEFT:
                    UFO1_x_change = -UFO1.speed
                elif event.key == pygame.K_SPACE: ##총알 발사
                    bullet_x = UFO1.rect.x+UFO1.sprite_width
                    bullet_y = UFO1.rect.y+UFO1.sprite_height/2
                    bullet_xy.append([bullet_x,bullet_y])
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    UFO1_x_change = 0
                    UFO1_y_change = 0 

        gamepad.fill(WHITE)
        background1_x -= 5
        background2_x -= 5
        boss.rect.x = random.randrange(580,600)

        if background1_x <= -background_width:
            background1_x = background_width

        if background2_x <= -background_width:
            background2_x = background_width

        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)

        drawObject(textSurface,textRect.x,textRect.y)

        #UFO_Monster Positon
        UFO_Monster.rect.x -= 7
        if UFO_Monster.rect.x <= 0:
            UFO_Monster.rect.x = pad_width
            UFO_Monster.rect.y = random.randrange(0,pad_height)

        ##메테오가
        if meteor == None:
            meteor_x -= 30
        else :
            meteor_x -= 15

        if meteor_x <= 0:
            meteor_x = pad_width
            meteor_y = random.randrange(0,pad_height)
            random.shuffle(meteors)
            meteor = meteors[0]
                   
        # UFO Postion
        UFO1.rect.y +=UFO1_y_change
        UFO1.rect.x +=UFO1_x_change
        if UFO1.rect.y<0:
            UFO1.rect.y=0
        elif UFO1.rect.y> pad_height - UFO1.sprite_height:
            UFO1.rect.y = pad_height - UFO1.sprite_height
        if UFO1.rect.x<0:
            UFO1.rect.x=0
        elif UFO1.rect.x > 500 :
            UFO1.rect.x = 500

        
        #Bullet Postion
        if len(bullet_xy) != 0:
            for i,bxy in enumerate(bullet_xy) :
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                if bxy[0] > boss.rect.x and boss.IsAlive and time>=10:
                    if bxy[1] > boss.rect.y and bxy[1] <boss.rect.y + boss.sprite_height:
                        bullet_xy.remove(bxy)
                        isShotBoss = True
                if bxy[0] > meteor_x :
                    if meteor!=None and bxy[1] > meteor_y and bxy[1] < meteor_y + meteor.sprite_height:
                        bullet_xy.remove(bxy)
                        isShotMeteor =True
                if bxy[0] > UFO_Monster.rect.x :
                    if  bxy[1] > UFO1.rect.y and bxy[1] < UFO1.rect.y + UFO1.sprite_height:
                        bullet_xy.remove(bxy)
                        isShotUFO =True


                if bxy[0] >= pad_width:
                    try :
                        bullet_xy.remove(bxy)
                    except :
                        pass
                  

        # 2) 게임 상태 업데이트      
        UFO1.update()
        if not isShotUFO :
            UFO_Monster.update()
        if time>=10 and boss.IsAlive:
            boss.update()
        if meteor != None and not isShotMeteor:
            meteor.update()

        # 3) 게임 상태 그리기
        drawObject(UFO1.image,UFO1.rect.x,UFO1.rect.y)
        if not isShotUFO :
           drawObject(UFO_Monster.image,UFO_Monster.rect.x,UFO_Monster.rect.y)
        if meteor != None and not isShotMeteor :
            drawObject(meteor.image,meteor_x,meteor_y)
        
        if len(bullet_xy) != 0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)

        if time>= 10 : #보스 출현 시간 time이 10이 나와야 출연을 함
         if not boss.HP <= 0 :
                if not isShotBoss :
                    drawObject(boss.image,boss.rect.x,boss.rect.y)
                else :
                    drawObject(boss.image,boss.rect.x,boss.rect.y)
                    boss.HP -= 1
                    isShotBoss = False
         else :
                boss.IsAlive = False
       

        pygame.display.update()
        clock.tick(FPS)
        
    pygame.quit()
    quit()

def initGame():
    global gamepad,clock,UFO1,background1,background2,bullet,boss,boom,UFO_Monster,meteors
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width,pad_height))
    pygame.display.set_caption("UFO game")
    UFO1 = UFO()
    boss = BOSS()
    meteors = []
    for i in range(5) :
        meteors.append(None)

    meteors.append(METEOR())
    meteors.append(METEOR())
    UFO_Monster = UFO_MONSTER()
    background1 = pygame.image.load("background_1.png")
    background2 = background1.copy()
    bullet = pygame.image.load("bullet.png")
    boom = pygame.image.load("boom.png")
    clock = pygame.time.Clock()
    runGame()

initGame()