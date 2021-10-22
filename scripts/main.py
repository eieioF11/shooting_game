
### インポート
import sys
import time
import os
import random
import pygame
from pygame.locals import *

### 定数
D_SIZE_X = 400
D_SIZE_Y = 640
USER_POS = 40
USER_HP  = 10
USER1_HP_X= 10
USER1_HP_Y= 10
USER2_HP_X= 255
USER2_HP_Y= 10
BAL_SIZE = 18       # ボールサイズ
F_RATE   = 60       # フレームレート
K_REPEAT = 20       # キーリピート発生間隔
USER_SPD = 10       # ユーザー移動速度
USER_X   = 600      #
BAL_SPD  = 10       # ボール移動速度
F_SIZE   = 60       # フォントサイズ
S_TIME   = 1        # START画面時間(秒)
E_TIME   = 3        # CLEAR画面時間(秒)

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
        else:
            if (pygame.time.get_ticks()-self.start)>=t:
                self.first=True
                return True
        return False

class sound:
    def __init__(self,fname):
        self.fname=os.path.join("sounds",fname)
        self.t1=Timer()
        self.PLAY=False
    def play(self):
        self.PLAY=True
    def stop(self):
        pygame.mixer.music.stop()
    def update(self,n=-1,t=1):#[s]
        if self.PLAY:
            pygame.mixer.init(frequency = 44100)    # 初期設定
            pygame.mixer.music.load(self.fname)     # 音楽ファイルの読み込み
            pygame.mixer.music.play(n)             # 音楽の再生回数(ループ再生)
            if n==-1:
                if self.t1.stand_by(t*1000):
                    self.PLAY=False
                    pygame.mixer.music.stop()               # 再生の終了
                    return False
        if n!=-1:
            self.PLAY=False
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()               # 再生の終了
                return False
        return True
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
        self.t3=Timer()
        self.hitflag=False
    def x(self,x):
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
                c=[0,0,0]
                if self.t3.stand_by(100):
                    self.t2.reset()
                    self.hitflag=False
            else:
                c=self.color
            pygame.draw.circle(self.surface,c, (self.x,self.ini[1]), 10)
            if self.t1.stand_by(1000):
                self.t2.reset()
                self.t1.reset()
                self.Hit=0
                self.hpflag=False
                self.hitflag=False
        else:
            pygame.draw.circle(self.surface,self.color, (self.x,self.ini[1]), 10)
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

class Button:
    def __init__(self, x, y, w, h, text=''):
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 40)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200,200,200)
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        self.txt_surface = self.FONT.render(self.text, True, (0,0,0))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
    def onClick(self):
        r = self.active
        self.active = False
        return r


class InputBox:
    def __init__(self, x, y, w, h, text='192.168.100.100'):
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 40)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.inflag1=False
        self.inflag2=False
    def handle_event(self, event):
        r = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        pygame.key.set_repeat()
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    r = self.text
                    self.text = ''
                elif event.key == pygame.K_DELETE:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    if not self.inflag2:
                        self.text = self.text[:-1]
                        self.inflag2=True
                else:
                    if not self.inflag1:
                        self.text += event.unicode
                        self.inflag1=True
                self.txt_surface = self.FONT.render(self.text, True, self.color)
        else:
            self.inflag1=False
            self.inflag2=False
        return r
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def menu(surface):
    decide=sound("decide15.wav")
    error=sound("error3.wav")
    cancel=sound("cancel3.wav")
    input_box = InputBox(100, 100, 200, 40)
    button = Button(100, 150, 140, 40, "Please Enter")
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
        surface.fill((30, 30, 30))
        input_box.draw(surface)
        button.draw(surface)
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
    return ip

def hpshow(surface,c,p,hp):
    for i in range(hp):
        pygame.draw.circle(surface,c,(p[0]+i*15,p[1]),5)

############################
### メイン関数
############################
def main():
    bulletflag=False
    GAMEOVER1=GAMEOVER2=False
    shot=sound("shot.wav")
    hit1=sound("hit.wav")
    hit2=sound("hit.wav")
    win=sound("win.wav")
    lose=sound("lose.wav")
    ### 画面初期化
    pygame.init()
    pygame.mixer.init()
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
    ### メニュー
    ip=menu(surface)
    print(ip)
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
            hpshow(surface,[255,0,0],[USER1_HP_X,USER1_HP_Y],user1.Hp())
            hpshow(surface,[0,0,255],[USER2_HP_X,USER2_HP_Y],user2.Hp())
        else:
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
            time.sleep(E_TIME)
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
        for event in pygame.event.get():
            ### 終了処理
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                ### キー操作
                pygame.key.set_repeat(100, 20)
                if event.key == K_LEFT:
                    user1.addx(-USER_SPD)
                if event.key == K_RIGHT:
                    user1.addx(USER_SPD)
                if event.key == K_SPACE:
                    if not bulletflag:
                        shot.play()
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