# shooting_game
ネットワーク課題用リポジトリ
# 環境構築
pythonバージョン:3.7.8
## pygameインストール
```bash
pip install pygame
```
## 学校の環境でインストールする場合
pythonバージョン:3.8.5\
pygameディレクトリに移動
```bash
 & C:/ProgramData/Anaconda3/python.exe -m pip install .\pygame-2.0.2-cp38-cp38-win_amd64.whl
```
# 遊び方
scriptsに移動
```bash
    python3 main.py
```
マルチプレイの場合はサーバーも起動
```bash
    python3 server.py
```
![menue](/images/image1.png)\
シングルプレイの場合はSingleをクリックする。\
マルチプレイの場合はサーバーipを入力しEnterキーを押し、下の"OK?"ボタンをクリックする。\
![menue](/images/image2.png)\
相手がサーバーに接続するとゲームが始まる。\
![menue](/images/image3.png)\
赤い宇宙船が自分で青が相手になる。キーボードの左右キーで移動、Spaceキーで弾を撃つ。
赤いハートがなくなったら自分の負け。青のハートがなくなったら相手の負になる。

# pygame参考
[図形表示](https://shizenkarasuzon.hatenablog.com/entry/2018/12/29/213355)\
[キー入力](https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/184932)\
[画像入力](https://shizenkarasuzon.hatenablog.com/entry/2019/02/23/151418)