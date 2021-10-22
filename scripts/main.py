
### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *

### 定数
D_SIZE_X = 400
D_SIZE_Y = 640
USER_POS = 40
USER_HP  = 100
BAL_SIZE = 18       # ボールサイズ
F_RATE   = 60       # フレームレート
K_REPEAT = 20       # キーリピート発生間隔
USER_SPD = 10       # ユーザー移動速度
USER_X   = 600      #
BAL_SPD  = 10       # ボール移動速度
F_SIZE   = 60       # フォントサイズ
S_TIME   = 2        # START画面時間(秒)
E_TIME   = 4        # CLEAR画面時間(秒)

### 画面定義(X軸,Y軸,横,縦)
SURFACE  = Rect(0, 0, D_SIZE_X, D_SIZE_Y) # 画面サイズ

class Timer:
    def __init__(self):
        self.first=True
        self.start=pygame.time.get_ticks()
    def reset(self):
        self.first=True
    def stand_by(self,t):#[ms]
        if self.first:
            self.start=pygame.time.get_ticks()
            self.first=False
        if (pygame.time.get_ticks()-self.start)>=t:
            self.first=True
            return True
        return False

class User(pygame.sprite.Sprite):
    def __init__(self,surface,ini,color):
        self.surface=surface
        self.ini=ini
        self.color=color
        self.x=self.ini[0]
        self.Hit=0
        self.hp=USER_HP
        self.hpflag=False
        self.t1=Timer()
        self.t2=Timer()
    def x(self,x):
        self.x=x
    def return_x(self):
        return self.x
    def addx(self,add):
        self.x+=add
    def Hp(self):
        return self.hp
    def hit(self,num):
        self.Hit=num
        self.hpflag=False
    def update(self):
        if self.x<=0:
            self.x=0
        elif self.x>=D_SIZE_X:
            self.x=400
        if self.Hit>0:
            if not self.hpflag:
                self.hp-=self.Hit
                self.hpflag=True
            if self.t2.stand_by(1000):
                pygame.draw.circle(self.surface,self.color, (self.x,self.ini[1]), 10)
            if self.t1.stand_by(5000):
                self.t2.reset()
                self.t1.reset()
                self.Hit=0
        else:
            pygame.draw.circle(self.surface,self.color, (self.x,self.ini[1]), 10)
        return

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
        if par_x-self.Range < self.x and self.x < par_x+self.Range and h:
            self.Hit=True
            return True
        if self.y<=0 or self.y>=D_SIZE_Y:
            self.y=self.ini[1]
            return True
        else:
            pygame.draw.ellipse(self.surface,self.color, (self.x,self.y,5,20,))
        return False

############################
### メイン関数
############################
def main():
    t=0
    bulletflag=False
    ### 画面初期化
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)
    ### 時間オブジェクト生成
    clock = pygame.time.Clock()
    ### Object
    t1=Timer()
    user1=User(surface,[200,600],[255,0,0])
    user2=User(surface,[200,40],[0,0,255])
    bullet1=[]
    bullet2=[]
    ### キーリピート有効
    pygame.key.set_repeat(K_REPEAT)
    ### STARTを表示
    font = pygame.font.Font(None, F_SIZE)
    text = font.render("START", True, (96,96,255))
    surface.fill((0,0,0))
    surface.blit(text, [133,299])
    pygame.display.update()
    ### 一時停止
    time.sleep(S_TIME)
    ### 無限ループ
    while True:
        ### フレームレート設定
        clock.tick(F_RATE)
        ### 背景色設定
        surface.fill((0,0,0))
        ###描画処理
        count=0
        for bullet in bullet1:
            if bullet.hit():
                count+=1
            if(bullet.update(user2.return_x())):
                del bullet1[bullet1.index(bullet)]
        user2.hit(count)
        count=0
        for bullet in bullet2:
            if bullet.hit():
                count+=1
            if(bullet.update(user1.return_x())):
                del bullet2[bullet2.index(bullet)]
        user1.hit(count)
        user1.update()
        user2.update()
        ### 画面更新
        pygame.display.update()
        ### イベント処理
        if t1.stand_by(800):#チャタリング防止
            bulletflag=False
        for event in pygame.event.get():
            ### 終了処理
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                ### キー操作
                if event.key == K_LEFT:
                    user1.addx(-USER_SPD)
                if event.key == K_RIGHT:
                    user1.addx(USER_SPD)
                if event.key == K_SPACE:
                    if not bulletflag:
                        bullet1.append(Bullet(surface,[user1.return_x(),D_SIZE_Y-USER_POS],[255,255,0],-10))
                        bulletflag=True
                if event.key == K_LCTRL:
                    if not bulletflag:
                        bullet2.append(Bullet(surface,[user2.return_x(),USER_POS],[0,255,255],10))
                        bulletflag=True
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