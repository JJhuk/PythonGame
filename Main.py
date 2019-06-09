
import pygame
from pygame.color import Color
import random
from UFO_class import UFO
from Boss_class import BOSS
from time import sleep
from UFO_Monster import UFO_MONSTER
from Meteor import METEOR
from Boss_class_Attak import BOSS_ATTACK

FPS = 28
pad_width = 800
pad_height = 200
background_width = 800
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)

meteor1_width = 34
meteor1_height = 36
meteor2_width = 86
meteor2_height = 60

def textObj(text,font) :
    textSurface = font.render(text,True,RED)
    return textSurface,textSurface.get_rect()

def dispMessage(text) :
    global gamepad
    global crashed

    largeText = pygame.font.Font("D2coding.ttf",40)
    TextSurf,TextRect = textObj(text,largeText)
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()
    sleep(10)
    crashed = True

def crash(x):
    global gamepad
    global explosion_sound,bgm_sound
    pygame.mixer_music.stop()
    pygame.mixer.Sound.play(explosion_sound)
    if x == 0 :
         dispMessage('주혁이가 운석에 맞고 죽었습니다.')
    elif x == 1 :
         dispMessage('주혁이가 UFO와 충돌하여 죽었습니다.')
    elif x == 2 :
         dispMessage('주혁이가 고압전류때문에 죽었습니다.')

   

def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def endgame() :
    global gamepad
    gamepad.fill(BLACK)
    dispMessage('성공적으로 새로운 행성을 찾았습니다.')
    sleep(10)
    pygame.quit()
    quit()

def runGame():
    global background1,background2,UFO1,clock,boss,UFO_Monster
    global bullet,meteors,boss_bullet
    global crashed,shot_sound
    
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

    boss_bullet.rect.x = boss.rect.x
    boss_bullet.rect.y = random.randrange(0,boss.sprite_height-boss_bullet.sprite_height)

    meteor_x = pad_width
    meteor_y = random.randrange(0,pad_height-80)
    random.shuffle(meteors)
    meteor = meteors[0]

    UFO_Monster.rect.x = pad_width
    UFO_Monster.rect.y = random.randrange(0,pad_height-UFO_Monster.sprite_height)

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
                    pygame.mixer.Sound.play(shot_sound)
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

        if boss_bullet.rect.x >= 0 and boss.Attack == True :
            boss_bullet.rect.x -= 20
        else :
            boss_bullet.rect.x = boss.rect.x
            boss_bullet.rect.y = random.randrange(0,boss.sprite_height)

                   
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
                if bxy[0] > meteor_x and meteor != None and isShotMeteor == False:
                    if meteor!=None and bxy[1] > meteor_y and bxy[1] < meteor_y + meteor.sprite_height:
                        try :   #예외처리 오류가 나서 그냥 페스해버림...
                            bullet_xy.remove(bxy)
                        except :
                            pass
                        meteor_x = pad_width
                        meteor_y = random.randrange(0,pad_height)
                        random.shuffle(meteors)
                        meteor = meteors[0]
                        isShotMeteor = True
                if bxy[0] > UFO_Monster.rect.x and isShotUFO == False: ##여기서도 오류남 나오지않았는데 xy좌표나옴
                     if  bxy[1] < UFO_Monster.rect.bottomleft[1] and bxy[1] > UFO_Monster.rect.topleft[1]:
                        try :
                            bullet_xy.remove(bxy)
                        except :
                            pass
                        UFO_Monster.rect.x = pad_width
                        UFO_Monster.rect.y = random.randrange(0,pad_height)
                        isShotUFO =True


                if bxy[0] >= pad_width:
                    try :
                        bullet_xy.remove(bxy)
                    except :
                        pass

        #충돌 체크

        if UFO1.rect.x + UFO1.sprite_width > meteor_x and meteor != None:
            if (UFO1.rect.y > meteor_y and UFO1.rect.y < meteor_y+meteor.sprite_height) or (UFO1.rect.y + UFO1.sprite_height > meteor_y and UFO1.rect.y + UFO1.sprite_height < meteor_y + meteor.sprite_height):
                crash(0)
        if UFO1.rect.x + UFO1.sprite_width > UFO_Monster.rect.x:
            if (UFO1.rect.y > UFO_Monster.rect.y and UFO1.rect.y < UFO_Monster.rect.y+UFO_Monster.sprite_height) or (UFO1.rect.y + UFO1.sprite_height > UFO_Monster.rect.y and UFO1.rect.y + UFO1.sprite_height < UFO_Monster.rect.y + UFO_Monster.sprite_height):
                crash(1)
        if UFO1.rect.x + UFO1.sprite_width > boss_bullet.rect.x:
            if (UFO1.rect.y > boss_bullet.rect.y and UFO1.rect.y < boss_bullet.rect.y+boss_bullet.sprite_height) or (UFO1.rect.y + UFO1.sprite_height > boss_bullet.rect.y and UFO1.rect.y + UFO1.sprite_height < boss_bullet.rect.y + boss_bullet.sprite_height):
                crash(2)

        # 2) 게임 상태 업데이트      
        
        
        UFO1.update()
        boss_bullet.update()

        if  UFO_Monster.IsAlive and isShotUFO == False: #UFO 쐈을때 없어지는거 구현
            UFO_Monster.update()
        if isShotUFO == True :
            isShotUFO = False
        if time>=10 and boss.IsAlive:
            boss.update()
        if meteor != None and isShotMeteor == False:
            meteor.update()
        if isShotMeteor == True :
            isShotMeteor = False

        # 3) 게임 상태 그리기
        if boss.Attack :
            drawObject(boss_bullet.image, boss_bullet.rect.x ,boss_bullet.rect.y)

        drawObject(UFO_Monster.image,UFO_Monster.rect.x,UFO_Monster.rect.y)

        drawObject(UFO1.image,UFO1.rect.x,UFO1.rect.y)


        if meteor != None and not isShotMeteor :
            if not isShotMeteor :
                drawObject(meteor.image, meteor_x,meteor_y)
            else :
                drawObject(meteor.image, meteor_x,meteor_y)
                meteor.HP -= 1
                isShotMeteor = False
        
        if len(bullet_xy) != 0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)

        if time>= 50 : #보스 출현 시간 time이 10이 나와야 출연을 함
         if not boss.HP <= 0 :  #보스체력이 0이 아닐때
                drawObject(boss.image,boss.rect.x,boss.rect.y) #일단 출력하고
                if not isShotBoss : #보스를 쏘지 않았으면
                    if boss.Attack == True and not boss.HP <= 0:
                        drawObject(boss_bullet.image,boss_bullet.rect.x,boss_bullet.rect.y)
                    else :
                        boss.Attack = not boss.Attack
                else : #보스를 쐇으면
                    boss.HP -= 1
                    isShotBoss = False
         else :
                boss.IsAlive = False
                boss.Attack = False
                endgame()

        if meteor == None :
            isShotMeteor = False
            random.shuffle(meteors)
            meteor = meteors[0]

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def initGame():
    global gamepad,clock,UFO1,background1,background2,bullet,boss,boom,UFO_Monster,meteors,boss_bullet
    global shot_sound,explosion_sound,bgm_sound
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width,pad_height))
    pygame.display.set_caption("UFO game")
    UFO1 = UFO()
    boss = BOSS()
    meteors = []
    for i in range(3) :
        meteors.append(None)

    meteors.append(METEOR())
    meteors.append(METEOR())
    UFO_Monster = UFO_MONSTER()
    background1 = pygame.image.load("background_1.png")
    background2 = background1.copy()
    bullet = pygame.image.load("bullet.png")
    boom = pygame.image.load("boom.png")
    clock = pygame.time.Clock()
    boss_bullet = BOSS_ATTACK()
    shot_sound = pygame.mixer.Sound('shot.wav')
    explosion_sound = pygame.mixer.Sound('explosion.wav')
    bgm_sound = pygame.mixer_music.load('mybgm.wav')
    bgm_sound = pygame.mixer_music.play(-1)
    runGame()

initGame()
