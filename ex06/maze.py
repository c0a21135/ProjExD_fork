import sys
import random
import time

import pygame as pg

#ローカルモジュールのimport
from maze_maker import make_maze


#定数の設定
WIDTH = 1500 #ウィンドウの横幅
HEIGHT = 900 #ウィンドウの縦幅
MAZE_X, MAZE_Y = 50, 50 #迷宮のマスの数
WINDOW_BLOCK = 60 #1マスの大きさ
NUM_ENEMY = 20 #敵の数
MAIN_FLOOR_LEN = 3 # フロアの数（階層数） <児玉>
SUB_FLOOR_LEN = 50 # 穴の数 <児玉>


class Screen: # スクリーン

    def __init__(self, title, width_height): 
        pg.display.set_caption(title) #タイトルの設定
        self.sfc = pg.display.set_mode(width_height) #スクリーンのサイズを設定
        self.rct = self.sfc.get_rect() #スクリーンのrectオブジェクトを取得
    

class Maze:#迷宮

    def __init__(self, yoko, tate, block, sub, n):
        self.maze_map=make_maze(yoko, tate, sub, n) #迷宮のリストの作成(0=道, 1=壁)
        for x, ele_list in enumerate(self.maze_map):
            for y, ele_num in enumerate(ele_list):
                if ele_num == 1: #要素が1であったら
                    self.maze_map[x][y] = Wall(block, x, y, n) #要素をWallオブジェクトに変更
                else:
                    self.maze_map[x][y] = Road(block,x, y, n) #1以外(0)ならば要素をRoadオブジェクトに変更
        Goal(block,self) #Goalオブジェクトを設置 <児玉>
        if n == 0: # メインフロアだったら <児玉>
            for i in range(SUB_FLOOR_LEN): # 規定数Holeオブジェクトを設置 <児玉>
                Hole(block, self)


    def show_maze(self, player_obj, block, screen_obj, enemy_lst): #迷宮の表示
        screen_obj.sfc.fill((0,0,0)) #ウィンドウを黒で塗りつぶし
        x, y = player_obj.x, player_obj.y #プレイヤーのx座標とy座標を取得
        kankaku_x = (screen_obj.rct.right/block) #表示するx方向のマス数
        kankaku_y = (screen_obj.rct.bottom/block) #表示するy方向のマス数
        high_x = int(x+kankaku_x//2) #表示させるx座標の最大値
        high_y = int(y+kankaku_y//2) #表示させるy座標の最大値
        low_x = int(x-kankaku_x//2) #表示させるx座標の最小値
        low_y = int(y-kankaku_y//2) #表示させるy座標の最小値
        for i,x in enumerate(range(low_x,high_x+1)):
            for j,y in enumerate(range(low_y,high_y+1)):
                if x>=0 and y>=0 and x<len(self.maze_map) and y<len(self.maze_map[0]):#x座標とy座標が迷宮のリスト内にあれば
                    obj=self.maze_map[x][y] 
                    obj.rct.center=block//2+block*i, block//2+block*j #表示させるマスの座標(ピクセル単位)を設定
                    obj.blit(screen_obj) #マスの表示
                    for enemy in enemy_lst: #全ての敵の中に
                        if enemy.x == x and enemy.y ==y: #表示させたマスと同じ座標を持つ敵がいれば
                            enemy.rct.center = obj.rct.center #マスの座標(ピクセル単位)を敵にコピー
                            enemy.blit(screen_obj) #敵を表示
                

class Wall: #壁

    def __init__(self, block, x, y, n):
        if n == 0: color = "#b0ca71" # フロアによって色（画像）を変更 <児玉>
        else: color = "#765c47"
        self.x, self.y = x, y #x座標とy座標を設定
        self.sfc = pg.Surface((block, block)) #Surfaceオブジェクトを作成
        pg.draw.rect(self.sfc, color, (0, 0, block, block)) #Surfaceオブジェクトに灰色の正方形を描き込む
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #Screenオブジェクトに壁を描画


class Road:#道

    def __init__(self, block, x, y, n):
        if n == 0: color = "#fff1cf" # フロアによって色（画像）を変更 <児玉>
        else: color = "#3f312b"
        self.x, self.y = x, y #x座標とy座標を設定
        self.sfc = pg.Surface((block, block)) #Surfaceオブジェクトを作成
        pg.draw.rect(self.sfc, color, (0, 0, block, block)) #Surfaceオブジェクトに白色の正方形を描き込む
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct)#Screenオブジェクトに道を描画


class Goal: #ゴール
    color = (255, 0, 255) # 色を固定（子クラスHoleと色が異なるため__init__の外） <児玉>

    def __init__(self,block,maze_obj):
        while True:#ループ処理(初期座標の決定)
            self.x = random.randint(0,len(maze_obj.maze_map)-1) #x座標ランダムに設定
            self.y = random.randint(0,len(maze_obj.maze_map[0])-1) #y座標ランダムに設定
            if isinstance(maze_obj.maze_map[self.x][self.y],Road): #初期座標が道であり
                if self.x != 1 and self.y != 1: #初期座標がプレイヤーの初期座標で無ければ
                    maze_obj.maze_map[self.x][self.y]=self #道をゴールに変更
                    break #ループを脱出
        self.sfc = pg.Surface((block, block)) #1マス分のSurfaceオブジェクトを作成
        pg.draw.rect(self.sfc, self.color, (0, 0, block, block)) #Surfaceオブジェクトに紫色の正方形を描画
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #ゴールの描画

class Hole(Goal):
    color = "#fff1cf" # 色を固定（親クラスGoalと色が異なるため__init__の外） <児玉>
    af_color = "#765c47"  # 変更後の色 <矢島>

    def __init__(self, block, maze_obj):
        self.block = block #インスタンス変数に1マスの大きさを保持(色の変更に用いるため) <矢島>
        super().__init__(block, maze_obj) # オーバーライド <児玉>

    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) # 穴の描画 <児玉>
    
    def chenge_color(self): #色の変更 <矢島>
        pg.draw.rect(self.sfc, self.af_color, (0 ,0, self.block,self.block)) #Surfaceオブジェクトを新しい色の正方形で塗りつぶす <矢島>


class Player: #プレイヤー

    key_delta = {pg.K_UP:[0, -1],
                 pg.K_DOWN:[0, 1],
                 pg.K_LEFT:[-1, 0],
                 pg.K_RIGHT:[1, 0]} #押下キーに対する座標遷移のdict

    def __init__(self,block,screen_obj):
        self.x , self.y = 1, 1 #迷宮の左上にプレイヤーを配置
        self.block = block #1マスの大きさ
        self.sfc = pg.Surface((block, block)) # 1マス分の大きさのSurfaceオブジェクトを作成
        pg.draw.circle(self.sfc, (0, 0, 255), (block/2, block/2), block/2) #Surfaceオブジェクトに青色の丸を表示
        self.sfc.set_colorkey((0, 0, 0)) #丸の背景を黒色に設定
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
        self.rct.center = block/2+block*(screen_obj.rct.right/block//2), block/2+block*(screen_obj.rct.bottom/block//2) #画面の真ん中にプレイヤーを設置
    
    def blit(self,screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #プレイヤーの描画
    
    def update_xy(self, maze_obj, screen_obj, enemy_lst,block): #プレイヤーの座標を更新
        pressed = pg.key.get_pressed() #押下キーを取得
        x, y = self.x, self.y #現在の座標を取得
        for delta in __class__.key_delta:
            if pressed[delta]:
                x += __class__.key_delta[delta][0]
                y += __class__.key_delta[delta][1]#押下キーに対応して座標を変更
        if isinstance(maze_obj.maze_map[x][y], Hole):# 移動先のマスがゴールだったら  <児玉>
            self.hold_x, self.hold_y = x, y #座標を保持しておく <児玉>
            self.x, self.y = x, y #座標の更新を確定 <児玉>
            maze_obj.maze_map[x][y].chenge_color()
            maze_obj.show_maze(self, block, screen_obj, enemy_lst) #迷宮の描画(プレイヤーではなく迷宮を動かすことによって移動させるため)  <児玉>
            self.blit(screen_obj) #プレイヤーを描画  <児玉>
            pg.display.update() #画面の更新  <児玉>
            time.sleep(1)
            maze_obj.maze_map[x][y] = Road(block, x, y, 0)  # 穴をRoadオブジェクトに変更（一度入った穴を消滅させるため）<児玉>
            return "hole" # play_game()に戻る
        elif isinstance(maze_obj.maze_map[x][y], Goal):#移動先のマスがゴールだったら
            self.x, self.y = x, y #座標の更新を確定
            maze_obj.show_maze(self, block, screen_obj, enemy_lst) #迷宮の描画(プレイヤーではなく迷宮を動かすことによって移動させるため)
            self.blit(screen_obj) #プレイヤーを描画
            pg.display.update() #画面の更新
            time.sleep(1) #ゴールしたことが確認できるための休止期間(1秒)
            return "goal" # play_game()に戻る <児玉>
        elif isinstance(maze_obj.maze_map[x][y], Road): #移動先が道だったら
            self.x, self.y = x, y #座標の更新を確定
            for enemy in enemy_lst:
                enemy.update_xy(maze_obj) #全ての敵を移動させる

        #移動先がゴール又は道でなかった場合、座標の変更を破棄する
    
    def colliderect(self, obj_lst,screen_obj): #衝突判定
        for obj in obj_lst: #list内の全てのオブジェクトに対して
            if self.rct.colliderect(obj.rct): #プレイヤーが衝突していれば
                obj.blit(screen_obj) #衝突相手を描画
                pg.display.update() #画面の更新
                time.sleep(1) #確認用の待機時間
                return True #bool値を返す(ゲームを終了させる)
    

class Enemy: #敵オブジェクト

    def __init__(self,block,maze_obj,player_obj):
        self.sfc = pg.Surface((block, block)) #1マス分のSurfaceオブジェクトを作成
        pg.draw.circle(self.sfc, (255, 0, 0), (block/2, block/2), block/2) #Surfaceオブジェクト内に赤色の円を描画
        self.sfc.set_colorkey((0, 0, 0)) #円の背景を黒に設定
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
        while True: #ループ処理(初期座標の設定)
            self.x = random.randint(0,len(maze_obj.maze_map)-1) #x座標ランダムに設定
            self.y = random.randint(0,len(maze_obj.maze_map[0])-1) #y座標をランダムに設定
            if isinstance(maze_obj.maze_map[self.x][self.y],Road): #初期値が道であり
                if self.x != player_obj.x and self.y != player_obj.y: #プレイヤーの初期座標で無ければ
                    break #ループを脱出
    
    def blit(self,screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #敵を描画
    
    def update_xy(self,maze_obj):
        while True: #ループ処理(座標の移動)
            next_x = self.x+random.randint(-1,1) #x座標を現在から-1から+1の間で変更
            next_y = self.y+random.randint(-1,1) #y座標を現在から-1から+1の間で変更
            if (not isinstance(maze_obj.maze_map[next_x][next_y],Wall)) and (type(maze_obj.maze_map[next_x][next_y]) != Goal): #移動先が壁でもゴールでも無ければ
                self.x, self.y = next_x, next_y #変更を確定
                break #ループを脱出
    

def play_game(floor, maze, screen, floor_type):
    # mount_mazeに現在のいるエリアを格納する <児玉>
    if floor_type == "main":
        mount_maze = maze[0]
        sub_maze = maze[1:]
    if floor_type == "sub":
        mount_maze = maze

    player = Player(WINDOW_BLOCK,screen) #プレイヤーの作成
    enemies = [Enemy(WINDOW_BLOCK,mount_maze,player) for _ in range(NUM_ENEMY)] #敵を格納したlistオブジェクトの作成
    mount_maze.show_maze(player, WINDOW_BLOCK, screen, enemies) #迷宮・敵の描画
    player.blit(screen) #プレイヤーの描画

    #ループ処理
    while True:
        pg.display.update() #画面の更新
        mount_maze.show_maze(player,WINDOW_BLOCK,screen,enemies) #迷宮・敵の描画
        player.blit(screen) #プレイヤーの描画
        for event in pg.event.get(): #イベントの取得
            if event.type == pg.QUIT: #ウィンドウの×ボタンが押されたら
                pg.quit() #pygemeの終了
                sys.exit() #プログラムの終了
            if event.type == pg.KEYDOWN: #キーが押されたら
                pos = player.update_xy(mount_maze, screen, enemies, WINDOW_BLOCK) #プレイヤー・敵の座標の更新
                if pos == "goal": return # ゴールしていれば → メインフロアならmain()に戻る、地下フロアなら一つ上のplay_game()に戻る <児玉>
                if pos == "hole": # 穴を踏んでいれば <児玉>
                    play_game(floor, sub_maze.pop(), screen, "sub") # 地下のマップを1つpop()し、floor_typeをsubに切り替え、play_gameを再帰呼び出しする <児玉>
        if player.colliderect(enemies,screen): #敵とプレイヤーが衝突していれば
            pg.quit() #pygemeの終了 <児玉>
            sys.exit() #プログラムの終了 <児玉>


def main(): #メイン関数

    #オブジェクトの作成
    screen = Screen("test", (WIDTH, HEIGHT)) #スクリーンの作成

    # 迷宮の作成
    # メインフロア1つと地下フロア規定数を保持する各階層を格納した2次元リストを作成 <児玉>
    # メイン/地下 は Mazeクラス内で作り分け
    '''下図イメージ
    [[ 1-メイン, 1-地下1 , 1-地下2, 1-地下3 ],
     [ 2-メイン, 2-地下1 , 2-地下2, 2-地下3 ],
     [ 3-メイン, 3-地下1 , 3-地下2, 3-地下3 ]]    '''    
    all_maze_lst = [[Maze(MAZE_X,MAZE_Y,WINDOW_BLOCK, SUB_FLOOR_LEN, i) for i in range(SUB_FLOOR_LEN+1)] for j in range(MAIN_FLOOR_LEN)]

    # フロア（階層）を回す <児玉>
    for i, floor_maze_lst in enumerate(all_maze_lst):
        floor = i+1 # 階層を進める　 <児玉>
        play_game(floor, floor_maze_lst, screen, "main") # play_gameを呼び出し、プレイを開始する　 <児玉>


if __name__ == "__main__":
    pg.init() #pygameを初期化
    main() #ゲームの実行
    pg.quit() #pygemeの終了
    sys.exit() #プログラムの終了