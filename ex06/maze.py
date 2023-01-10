import sys
import random
import time

import pygame as pg

#ローカルモジュールのimport
from maze_maker import make_maze


class Screen: # スクリーン

    def __init__(self, title, width_height): 
        pg.display.set_caption(title) #タイトルの設定
        self.sfc = pg.display.set_mode(width_height) #スクリーンのサイズを設定
        self.rct = self.sfc.get_rect() #スクリーンのrectオブジェクトを取得
    

class Maze:#迷宮

    def __init__(self, yoko, tate, block):
        self.maze_map=make_maze(yoko, tate) #迷宮のリストの作成(0=道, 1=壁)
        for x, ele_list in enumerate(self.maze_map):
            for y, ele_num in enumerate(ele_list):
                if ele_num == 1: #要素が1であったら
                    self.maze_map[x][y] = Wall(block, x, y) #要素をWallオブジェクトに変更
                else:
                    self.maze_map[x][y] = Road(block,x, y) #1以外(0)ならば要素をRoadオブジェクトに変更
        Goal(block,self) #Goalオブジェクトを設置

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

    def __init__(self, block, x, y):
        self.x, self.y = x, y #x座標とy座標を設定
        self.sfc = pg.Surface((block, block)) #Surfaceオブジェクトを作成
        pg.draw.rect(self.sfc, (144, 144, 144), (0, 0, block, block)) #Surfaceオブジェクトに灰色の正方形を描き込む
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #Screenオブジェクトに壁を描画


class Road:#道

    def __init__(self, block, x, y):
        self.x, self.y = x, y #x座標とy座標を設定
        self.sfc = pg.Surface((block, block)) #Surfaceオブジェクトを作成
        pg.draw.rect(self.sfc, (255, 255, 255), (0, 0, block, block)) #Surfaceオブジェクトに白色の正方形を描き込む
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct)#Screenオブジェクトに道を描画



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
        if isinstance(maze_obj.maze_map[x][y], Goal):#移動先のマスがゴールだったら
            self.x, self.y = x, y #座標の更新を確定
            maze_obj.show_maze(self, block, screen_obj, enemy_lst) #迷宮の描画(プレイヤーではなく迷宮を動かすことによって移動させるため)
            self.blit(screen_obj) #プレイヤーを描画
            pg.display.update() #画面の更新
            time.sleep(1) #ゴールしたことが確認できるための休止期間(1秒)
            pg.quit() #pygemeの終了
            sys.exit() #プログラムの終了
        if isinstance(maze_obj.maze_map[x][y], Road): #移動先が道だったら
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
            if isinstance(maze_obj.maze_map[next_x][next_y],Road): #移動先が道であったら
                self.x, self.y = next_x, next_y #変更を確定
                break #ループを脱出
    

class Goal: #ゴール

    def __init__(self,block,maze_obj):
        while True:#ループ処理(初期座標の決定)
            self.x = random.randint(0,len(maze_obj.maze_map)-1) #x座標ランダムに設定
            self.y = random.randint(0,len(maze_obj.maze_map[0])-1) #y座標ランダムに設定
            if isinstance(maze_obj.maze_map[self.x][self.y],Road): #初期座標が道であり
                if self.x != 1 and self.y != 1: #初期座標がプレイヤーの初期座標で無ければ
                    maze_obj.maze_map[self.x][self.y]=self #道をゴールに変更
                    break #ループを脱出
        self.sfc = pg.Surface((block, block)) #1マス分のSurfaceオブジェクトを作成
        pg.draw.rect(self.sfc, (255, 0, 255), (0, 0, block, block)) #Surfaceオブジェクトに紫色の正方形を描画
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #ゴールの描画


def main(): #メイン関数

    #定数の設定
    WIDTH = 1600 #ウィンドウの横幅
    HEIGHT = 900 #ウィンドウの縦幅
    MAZE_X, MAZE_Y = 100, 100 #迷宮のマスの数
    WINDOW_BLOCK = 20 #1マスの大きさ
    NUM_ENEMY = 200 #敵の数

    #オブジェクトの作成
    screen = Screen("test", (WIDTH, HEIGHT)) #スクリーンの作成
    maze = Maze(MAZE_X, MAZE_Y, WINDOW_BLOCK) #迷宮の作成
    player = Player(WINDOW_BLOCK,screen) #プレイヤーの作成
    enemies = [Enemy(WINDOW_BLOCK,maze,player) for _ in range(NUM_ENEMY)] #敵を格納したlistオブジェクトの作成
    maze.show_maze(player, WINDOW_BLOCK, screen, enemies) #迷宮・敵の描画
    player.blit(screen) #プレイヤーの描画

    #ループ処理
    while True:
        pg.display.update() #画面の更新
        maze.show_maze(player,WINDOW_BLOCK,screen,enemies) #迷宮・敵の描画
        player.blit(screen) #プレイヤーの描画
        for event in pg.event.get(): #イベントの取得
            if event.type == pg.QUIT: #ウィンドウの×ボタンが押されたら
                return #main関数の脱出(ゲームの終了)
            if event.type == pg.KEYDOWN: #キーが押されたら
                player.update_xy(maze, screen, enemies, WINDOW_BLOCK) #プレイヤー・敵の座標の更新
        if player.colliderect(enemies,screen): #敵とプレイヤーが衝突していれば
            return #main関数の脱出(ゲームの終了)


if __name__ == "__main__":
    pg.init() #pygameを初期化
    main() #ゲームの実行
    pg.quit() #pygemeの終了
    sys.exit() #プログラムの終了