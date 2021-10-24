import os
import pygame
from pygame.locals import *
from Timer import Timer

def load_image(fname):
    fpath=os.path.join("images",fname)
    print(fpath)
    try:
    	return pygame.image.load(fpath)
    except:
    	return pygame.image.load("../"+fpath)

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
            try:
            		pygame.mixer.music.load(self.fname)     # 音楽ファイルの読み込み
            except:
            		pygame.mixer.music.load("../"+self.fname)     # 音楽ファイルの読み込み
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
