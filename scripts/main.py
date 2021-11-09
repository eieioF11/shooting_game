#!/usr/bin/env python
# -*- coding: utf-8 -*-
### インポート
import sys
import time
import pygame
from pygame.locals import *
from Timer import Timer
from GameIO import *

from client import *

import random

### 設定
D_SIZE_X     = 400      #windowサイズ
D_SIZE_Y     = 640
BG_SP        = 5        #背景スクロールスピード
USER_POS     = 40       #ユーザーの位置(上もしくは下からの距離)
USER_X       = 600      #ユーザーの初期位置(x)
USER_HP      = 10       #ユーザーのHP上限
USER_SPD     = 10       # ユーザー移動速度
USER1_HP_X   = 10       #ユーザー１のHP表示場所
USER1_HP_Y   = 10
USER2_HP_X   = 240      #ユーザー2のHP表示場所
USER2_HP_Y   = 10
USERIMG_SIZE = 30       #imageサイズ
BAL_SIZE     = 10       # ボールサイズ
F_RATE       = 60       # フレームレート
K_REPEAT     = 20       # キーリピート発生間隔
BAL_SPD      = 10       # ボール移動速度
F_SIZE       = 60       # フォントサイズ
S_TIME       = 1        # START画面時間(秒)
E_TIME       = 2        # CLEAR画面時間(秒)

### 画面定義(X軸,Y軸,横,縦)
SURFACE  = Rect(0, 0, D_SIZE_X, D_SIZE_Y) # 画面サイズ

class User(pygame.sprite.Sprite):
    def __init__(self,surface,ini,img):
        self.surface=surface
        self.ini=ini
        self.img=img
        self.color=[255,255,255]
        self.x=self.ini[0]
        self.Hit=0
        self.hp=USER_HP
        self.hpflag=False
        self.t1=Timer()
        self.t2=Timer()
        self.t3=Timer()
        self.hitflag=False
    def X(self,x):
        self.x=x
    def return_x(self):
        return self.x
    def addx(self,add):
        self.x+=add
    def Hp(self):
        return self.hp
    def hit(self,num):
        if num!=0:
            self.Hit=num
            self.hpflag=False
            self.hitflag=False
    def update(self):
        if self.x<=0:
            self.x=0
        elif self.x>=D_SIZE_X:
            self.x=400
        if self.Hit>0:
            if not self.hpflag:
                self.hp-=self.Hit
                self.hpflag=True
            if self.t2.stand_by(100) and not self.hitflag:
                self.t3.reset()
                self.hitflag=True
            if self.hitflag:
                if self.t3.stand_by(100):
                    self.t2.reset()
                    self.hitflag=False
            else:
                self.surface.blit(self.img,(self.x-(USERIMG_SIZE//2),self.ini[1]-(USERIMG_SIZE//2)))
            if self.t1.stand_by(1000):
                self.t2.reset()
                self.t1.reset()
                self.Hit=0
                self.hpflag=False
                self.hitflag=False
        else:
            self.surface.blit(self.img,(self.x-(USERIMG_SIZE//2),self.ini[1]-(USERIMG_SIZE//2)))
        if self.hp<=0:
            self.hp=0
            return True
        return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self,surface,ini,color,shootsp):
        self.surface=surface
        self.ini=ini
        self.color=color
        self.x=self.ini[0]
        self.y=self.ini[1]
        self.shootsp=shootsp
        self.Hit=False
        self.Range=20
    def hit(self):
        return self.Hit
    def update(self,par_x):
        self.y+=self.shootsp
        if self.shootsp>0:
            h=self.y>=D_SIZE_Y-USER_POS
        elif self.shootsp<0:
            h=self.y<=USER_POS
        if self.Hit:
            return True
        if par_x-self.Range < self.x and self.x < par_x+self.Range and h:
            self.Hit=True
        if self.y<=0 or self.y>=D_SIZE_Y:
            self.y=self.ini[1]
            return True
        else:
            pygame.draw.ellipse(self.surface,self.color, (self.x,self.y,5,20,))
        return False

def menu(surface):
    decide=sound("decide15.wav")
    error=sound("error3.wav")
    cancel=sound("cancel3.wav")
    input_box = InputBox(100, 100, 200, 40)
    button = Button(100, 150, 140, 40, "Please Enter")
    button2 = Button(100, 250, 140, 40, "Single")
    exit_sw = False
    bt=False
    t=Timer()
    while not exit_sw:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            r=input_box.handle_event(event)
            if r != "":
                button.text = "OK?"
                IP_TEXT=r
                bt=True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    cancel.play()
                    while cancel.update(1):pass
                    bt=False
                    button.text = "Please Enter"
                ### キー操作
            input_box.update()
            button.handle_event(event)
            button.update()
            button2.handle_event(event)
            button2.update()
        surface.fill((30, 30, 30))
        input_box.draw(surface)
        button.draw(surface)
        button2.draw(surface)
        if button2.onClick():
            ip=[]
            exit_sw=True
            decide.play()
            while decide.update(1):pass
        if bt:
            if button.onClick():
                try:
                    print(IP_TEXT)
                    ip=[int(i) for i in IP_TEXT.split('.')]
                    exit_sw=True
                    decide.play()
                    while decide.update(1):pass
                except:
                    button.text = "error"
                    bt=False
                    button.draw(surface)
                    error.play()
                    pygame.display.update()
                    while error.update(1):pass
                    button.text = "Please Enter"
        font = pygame.font.Font(None, F_SIZE)
        text = font.render("Enter IP", True, (255,255,255))
        surface.blit(text, [10,10])
        pygame.display.update()
    return IP_TEXT , ip

def hpshow(surface,img,p,hp):
    for i in range(hp):
        surface.blit(img,(p[0]+i*15,p[1]))

############################
### メイン関数
############################
def main():
    bg_y = 0
    bulletflag=False
    bulletflag2=False
    GAMEOVER1=GAMEOVER2=False
    Single=False
    #音声読み込み
    shot=sound("shot.wav")
    hit1=sound("hit.wav")
    hit2=sound("hit.wav")
    win=sound("win.wav")
    lose=sound("Lose.wav")
    ### 画像読み込み
    rhimg = load_image("redheart.png")
    bhimg = load_image("blueheart.png")
    rhimg = pygame.transform.scale(rhimg, (14,14))
    bhimg = pygame.transform.scale(bhimg, (14,14))
    U1img = load_image("USER1.png")
    U2img = load_image("USER2.png")
    U1img = pygame.transform.scale(U1img, (USERIMG_SIZE,USERIMG_SIZE))
    U2img = pygame.transform.scale(U2img, (USERIMG_SIZE,USERIMG_SIZE))
    BGimg = load_image("BG.png")
    BGimg = pygame.transform.scale(BGimg, (D_SIZE_X,D_SIZE_Y))
    ### 画面初期化
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode(SURFACE.size)
    ### 時間オブジェクト生成
    clock = pygame.time.Clock()
    ### Object
    t1=Timer()
    t2=Timer()
    user1=User(surface,[200,600],U1img)
    user2=User(surface,[200,40],U2img)
    bullet1=[]
    bullet2=[]
    ### メニュー
    iptxt,ip =menu(surface)
    if len(ip)==0:
        Single=True
    print(iptxt,ip)
    ### STARTを表示
    font = pygame.font.Font(None, F_SIZE)
    text = font.render("START", True, (96,96,255))
    surface.fill((0,0,0))
    surface.blit(text, [133,299])
    pygame.display.update()
    ### 一時停止
    time.sleep(S_TIME)
    ### キーリピート有効
    pygame.key.set_repeat(K_REPEAT)
    ###送受信データ作成
    # ホスト名を取得、表示
    host = socket.gethostname()
    print(host)
    # ipアドレスを取得、表示
    myip = socket.gethostbyname(host)
    myip=myip.split('.')
    print(myip)
    #id作成
    id=int(myip[3])
    wdata=[id,200,False]
    rdata=[]
    print(wdata)
    while True:
        rdata=communication(iptxt,wdata)
        if rdata[0]!=0:
            break
    ### 無限ループ
    while True:
        ### フレームレート設定
        clock.tick(F_RATE)
        ### 背景色設定
        surface.fill((0,0,0))
        ###描画処理
        #背景
        bg_y = (bg_y+BG_SP)%D_SIZE_Y
        surface.blit(BGimg,[0,bg_y-D_SIZE_Y])
        surface.blit(BGimg,[0,bg_y])
        #ゲーム画面
        if not GAMEOVER1 and not GAMEOVER2:
            count=0
            for bullet in bullet1:
                if bullet.hit():#当たり判定
                    count+=1
                    hit1.play()
                if(bullet.update(user2.return_x())):
                    del bullet1[bullet1.index(bullet)]
            user2.hit(count)
            count=0
            for bullet in bullet2:
                if bullet.hit():#当たり判定
                    count+=1
                    hit2.play()
                if(bullet.update(user1.return_x())):
                    del bullet2[bullet2.index(bullet)]
            user1.hit(count)
            GAMEOVER1=user1.update()
            GAMEOVER2=user2.update()
            hpshow(surface,rhimg,[USER1_HP_X,USER1_HP_Y],user1.Hp())
            hpshow(surface,bhimg,[USER2_HP_X,USER2_HP_Y],user2.Hp())
        else:#終了画面
            if GAMEOVER1:
                text = font.render("LOSE", True, (255,0,0))
                surface.blit(text, [140,299])
                lose.play()
            elif GAMEOVER2:
                text = font.render(" VICTORY", True, (255,255,0))
                surface.blit(text, [100,299])
                win.play()
            pygame.display.update()
            while lose.update(1):pass
            while win.update(1):pass
            while True:
                for event in pygame.event.get():
                    ### 終了処理
                    if event.type == QUIT:
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            exit()
                if t2.stand_by(E_TIME*1000):
                    exit()
        ### 画面更新
        pygame.display.update()
        ### 再生
        shot.update(1)
        hit1.update(1)
        hit2.update(1)
        ### イベント処理
        if t1.stand_by(800):#チャタリング防止
            bulletflag=False
            bulletflag2=False
        for event in pygame.event.get():
            ### 終了処理
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                ### キー操作
                #pygame.key.set_repeat(100, 20)
                if event.key == K_LEFT:
                    user1.addx(-USER_SPD)
                if event.key == K_RIGHT:
                    user1.addx(USER_SPD)
                if event.key == K_SPACE:
                    if not bulletflag:
                        shot.play()
                        bullet1.append(Bullet(surface,[user1.return_x(),D_SIZE_Y-USER_POS],[255,255,0],-10))
                        bulletflag=True

        if Single:
            u2r=random.randint(0,1)
            u2s=random.randint(0,1)
            if u2r:
                user2.addx(-USER_SPD)
            else:
                user2.addx(USER_SPD)
            if u2s:
                if not bulletflag2:
                    bullet2.append(Bullet(surface,[user2.return_x(),USER_POS],[0,255,255],10))
                    wdata[2]=True
                    bulletflag2=True
        else:
            wdata[1]=user1.return_x()
            rdata=communication(iptxt,wdata)
            print(rdata)
            user2.X(rdata[1])
            if rdata[2]:
                if not bulletflag2:
                    bullet2.append(Bullet(surface,[user2.return_x(),USER_POS],[0,255,255],10))
                    bulletflag2=True
            wdata[2]=False




############################
### 終了関数
############################
def exit():
    pygame.quit()
    sys.exit()

############################
### メイン関数呼び出し
############################
if __name__ == "__main__":
    ### 処理開始
    main()
