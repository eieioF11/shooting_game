
### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *

### 定数
BAL_SIZE = 18       # ボールサイズ
F_RATE   = 60       # フレームレート
K_REPEAT = 20       # キーリピート発生間隔
RKT_SPD  = 10       # ラケット移動速度
BAL_SPD  = 10       # ボール移動速度
F_SIZE   = 60       # フォントサイズ
S_TIME   = 2        # START画面時間(秒)
E_TIME   = 4        # CLEAR画面時間(秒)

### 画面定義(X軸,Y軸,横,縦)
SURFACE  = Rect(0, 0, 400, 640) # 画面サイズ

class User(pygame.sprite.Sprite):
    def __init__(self,surface,ini,color):
        self.surface=surface
        self.ini=ini
        self.color=color
    def update(self,t):
        x=self.ini[0]
        pygame.draw.circle(self.surface,self.color, (x,self.ini[1]), 10)
        return

class Bullet(pygame.sprite.Sprite):
    def __init__(self,surface,ini,color):
        self.surface=surface
        self.ini=ini
        self.color=color
    def update(self,t):
        x=self.ini[0]
        y=self.ini[1]
        pygame.draw.ellipse(self.surface,self.color, (x,y,5,20,))
        return

############################
### メイン関数
############################
def main():
    t=0
    ### 画面初期化
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)
    ### 時間オブジェクト生成
    clock = pygame.time.Clock()
    ### Object
    user1=User(surface,[200,600],[255,0,0])
    user2=User(surface,[200,40],[0,0,255])
    bullet1=Bullet(surface,[200,600],[255,255,0])
    bullet2=Bullet(surface,[200,40],[0,255,255])
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
        user1.update(t)
        user2.update(t)
        bullet1.update(t)
        bullet2.update(t)
        ### 画面更新
        pygame.display.update()
        ### イベント処理
        for event in pygame.event.get():
            ### 終了処理
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                ### キー操作
                if event.key == K_LEFT:
                    racket_pos -= RKT_SPD
                if event.key == K_RIGHT:
                    racket_pos += RKT_SPD

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