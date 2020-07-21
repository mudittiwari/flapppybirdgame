import pygame
import sys
import random
import time
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GAME_SPRITES = []
GAME_MUSIC = []
crossed=False
score=0
clock=pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("flappybird")
exit_game = False
bird_velocity=3
i=0
GAME_SPRITES.append(pygame.image.load("flappy-bird-hero-1240x1240.png"))
BIRD = pygame.image.load("bird.png")
GAME_SPRITES.append(BIRD)
GAME_SPRITES.append(pygame.image.load("base.png"))
GAME_SPRITES.append(pygame.image.load("upper.jpg"))
GAME_SPRITES.append(pygame.image.load("pipe.png"))
GAME_SPRITES.append(pygame.transform.rotate(pygame.image.load("pipe.png"),180))
GAME_SPRITES.append(pygame.image.load("gameover.png"))
GAME_SPRITES[2] = pygame.transform.scale(GAME_SPRITES[2], (400, 100)).convert_alpha()
GAME_SPRITES[1] = pygame.transform.scale(GAME_SPRITES[1], (90, 90)).convert_alpha()
GAME_SPRITES[3] = pygame.transform.scale(GAME_SPRITES[3], (400, 400)).convert_alpha()
GAME_SPRITES[4] = pygame.transform.scale(GAME_SPRITES[4], (60, 300)).convert_alpha()
GAME_SPRITES[5] = pygame.transform.scale(GAME_SPRITES[5], (60, 300)).convert_alpha()
GAME_SPRITES[6]=pygame.transform.scale(GAME_SPRITES[6],(400,500)).convert_alpha()
GAME_MUSIC.append(pygame.mixer.Sound("hit.wav"))
GAME_MUSIC.append(pygame.mixer.Sound("wing.wav"))
GAME_MUSIC.append(pygame.mixer.Sound("point.wav"))
font=pygame.font.SysFont(None,30)
black=(0,0,0)
white=(192,192,192)
game_over=False
bird_acc=0
def lowerpipegenerator():
    posi_y=random.randint(150,350)
    return posi_y
def upperpipegenerator(y):
    y=y-100
    posi_y=GAME_SPRITES[4].get_height()-y
    return posi_y
def text_generator(text,color,x,y):
    texttoshow=font.render(text,True,color)
    SCREEN.blit(texttoshow,[x,y])
    pygame.display.update()
def collison(bird_posi,lowerpipe,upperpipe):
    global crossed
    if bird_posi<-40:
        GAME_MUSIC[0].play()
        time.sleep(1)
        game_end()
    elif bird_posi>325:
        GAME_MUSIC[0].play()
        time.sleep(1)
        game_end()
    # elif bird_posi>lowerpipe[1]-75 and lowerpipe[0]==-20:
    #     game_end()
    elif bird_posi>lowerpipe[1]-75 and abs(lowerpipe[0]-50)<GAME_SPRITES[4].get_width():
        GAME_MUSIC[0].play()
        time.sleep(1)
        game_end()
    elif bird_posi<(upperpipe[1]+GAME_SPRITES[4].get_height()-50) and abs(lowerpipe[0]-50)<GAME_SPRITES[4].get_width():
        GAME_MUSIC[0].play()
        time.sleep(1)
        game_end()
    elif lowerpipe[0]<50 and crossed==False:
        global score
        # global crossed
        GAME_MUSIC[2].play()
        score+=10
        crossed=True
        print(score)
def game_end():
    with open("score.txt","r") as f:
        high_score=int(f.read())
    global exit_game
    while not exit_game:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_KP_ENTER:
                    start_screen()
        SCREEN.blit(GAME_SPRITES[6],(0,0))
        # text_generator(f"score:{score}           high-score:{high_score}",black,60,350)
        # pygame.display.update()
        # texttoshow = font.render("press enter to play again", True, black)
        text=font.render(f"score:{score}           high-score:{high_score}",True,black)
        SCREEN.blit(text,[60,350])
        # SCREEN.blit(texttoshow, [75, 400])
        enter = pygame.image.load("entertoplay.png")
        enter = pygame.transform.scale(enter, (200, 50)).convert_alpha()
        SCREEN.blit(enter, (100, 380))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()
def main_game():
    global bird_acc
    global game_over
    global bird_velocity
    global crossed
    with open("score.txt", "r") as f:
        high_score = int(f.read())
    ready=False
    pipes_list=[[400,300],[400,-100]]
    bird_posi=140
    velocity_pipe = -9
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    GAME_MUSIC[1].play()
                    if ready:
                        bird_acc = -1
                if event.key == pygame.K_KP_ENTER:
                    ready = True
        if ready:
            for pipes in pipes_list:
                pipes[0] = pipes[0] + velocity_pipe
                if pipes_list[0][0] < -170:
                    # print(pipes_list)
                    y = lowerpipegenerator()
                    # pipes_list=[]
                    pipes_list = [[400, y], [400, -upperpipegenerator(y)]]
                    crossed=False
            bird_velocity=bird_velocity+bird_acc
            if bird_velocity<-6:
                bird_acc=1
                bird_posi=bird_posi-bird_velocity
            else:
                bird_posi=bird_posi+bird_velocity
            collison(bird_posi,pipes_list[0],pipes_list[1])
        # texttoshow = font.render("score", True, black)
        SCREEN.blit(GAME_SPRITES[3], (0, 0))
        SCREEN.blit(GAME_SPRITES[5], (pipes_list[0][0], pipes_list[0][1]))
        SCREEN.blit(GAME_SPRITES[4], (pipes_list[1][0], pipes_list[1][1]))
        SCREEN.blit(GAME_SPRITES[2], (0, 400))
        SCREEN.blit(GAME_SPRITES[1], (50, bird_posi))
        # SCREEN.blit(texttoshow, [50, 50])
        if score>high_score:
            high_score=score
        high_score_toshow=f"high-score:{high_score}"
        text_generator(f"score:{score}                     {high_score_toshow}",black,20,30)
        # text_generator(high_score_toshow,black,230,30)
        pygame.display.update()
        clock.tick(30)
        with open("score.txt","w") as f2:
            f2.write(str(high_score))
    pygame.quit()
    quit()
def start_screen():
    GAME_SPRITES[0]=pygame.transform.scale(GAME_SPRITES[0], (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    SCREEN.blit(GAME_SPRITES[0], (0, 0))
    text_generator("Flappy Bird by Mudit Tiwari", white, 65, 340)
    enter=pygame.image.load("entertoplay.png")
    enter=pygame.transform.scale(enter,(200,50)).convert_alpha()
    SCREEN.blit(enter,(100,380))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_KP_ENTER:
                    main_game()
start_screen()