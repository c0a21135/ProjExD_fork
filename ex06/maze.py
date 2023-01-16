import sys
import random
import time

import pygame as pg

#ローカルモジュールのimport
from maze_maker import create_dungeon


#定数の設定
WIDTH = 1500 #ウィンドウの横幅 <矢島>
HEIGHT = 900 #ウィンドウの縦幅 <矢島>
MAZE_X, MAZE_Y = 50, 50 #迷宮のマスの数 <矢島>
WINDOW_BLOCK = 60 #1マスの大きさ <矢島>
NUM_ENEMY = 50 #敵の数 <矢島>
MAIN_FLOOR_LEN = 3 # フロアの数（階層数） <児玉>
HOOL_NUM = 100 # 穴の数 <児玉>
COMMAND = ["[A]ttack", "[I]tems", "[M]agic", "[R]un"] #Playerのコマンドのリスト <貞野>

class Screen: # スクリーン <矢島>

    def __init__(self, title, width_height): 
        pg.display.set_caption(title) #タイトルの設定 <矢島>
        self.sfc = pg.display.set_mode(width_height) #スクリーンのサイズを設定 <矢島>
        self.rct = self.sfc.get_rect() #スクリーンのrectオブジェクトを取得 <矢島>
    

class Maze:#迷宮 <矢島> <改訂 児玉>

    def __init__(self, yoko, tate, block, floor):
        self.maze_map=create_dungeon(yoko, tate) #迷宮のリストの作成(0=道, 1=壁) <矢島>
        for x, ele_list in enumerate(self.maze_map):
            for y, ele_num in enumerate(ele_list):
                if ele_num == 1: #要素が1であったら <矢島>
                    self.maze_map[x][y] = Wall(block, x, y, floor) #要素をWallオブジェクトに変更 <矢島>
                else:
                    self.maze_map[x][y] = Road(block,x, y, floor) #1以外(0)ならば要素をRoadオブジェクトに変更 <矢島>
        Goal(block,self) #Goalオブジェクトを設置 <児玉>
        if floor == 0: # メインフロアだったら <児玉>
            for _ in range(HOOL_NUM): # 規定数Holeオブジェクトを設置 <児玉>
                Hole(block, self)


    def show_maze(self, player_obj, block, screen_obj, enemy_lst): #迷宮の表示 <矢島>
        screen_obj.sfc.fill((0,0,0)) #ウィンドウを黒で塗りつぶし <矢島>
        x, y = player_obj.x, player_obj.y #プレイヤーのx座標とy座標を取得 <矢島>
        kankaku_x = (screen_obj.rct.right/block) #表示するx方向のマス数 <矢島>
        kankaku_y = (screen_obj.rct.bottom/block) #表示するy方向のマス数 <矢島>
        high_x = int(x+kankaku_x//2) #表示させるx座標の最大値 <矢島>
        high_y = int(y+kankaku_y//2) #表示させるy座標の最大値 <矢島>
        low_x = int(x-kankaku_x//2) #表示させるx座標の最小値 <矢島>
        low_y = int(y-kankaku_y//2) #表示させるy座標の最小値 <矢島>
        for i,x in enumerate(range(low_x,high_x+1)):
            for j,y in enumerate(range(low_y,high_y+1)):
                if x>=0 and y>=0 and x<len(self.maze_map) and y<len(self.maze_map[0]):#x座標とy座標が迷宮のリスト内にあれば <矢島>
                    obj=self.maze_map[x][y] 
                    obj.rct.center=block//2+block*i, block//2+block*j #表示させるマスの座標(ピクセル単位)を設定 <矢島>
                    obj.blit(screen_obj) #マスの表示 <矢島>
                    for enemy in enemy_lst: #全ての敵の中に <矢島>
                        if enemy.x == x and enemy.y ==y: #表示させたマスと同じ座標を持つ敵がいれば <矢島>
                            enemy.rct.center = obj.rct.center #マスの座標(ピクセル単位)を敵にコピー <矢島>
                            enemy.blit(screen_obj) #敵を表示 <矢島>
                

class Wall: #壁 <矢島> <改訂 児玉>

    def __init__(self, block, x, y, floor):
        if floor == 0: color = "#b0ca71" # フロアによって色（画像）を変更 <児玉>
        else: color = "#765c47"
        self.x, self.y = x, y #x座標とy座標を設定 <矢島>
        self.sfc = pg.Surface((block, block)) #Surfaceオブジェクトを作成 <矢島>
        pg.draw.rect(self.sfc, color, (0, 0, block, block)) #Surfaceオブジェクトに灰色の正方形を描き込む <矢島>
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得 <矢島>
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #Screenオブジェクトに壁を描画 <矢島>


class Road:#道

    def __init__(self, block, x, y, floor):
        if floor == 0: color = "#fff1cf" # フロアによって色（画像）を変更 <児玉>
        else: color = "#3f312b"
        self.x, self.y = x, y #x座標とy座標を設定 <矢島>
        self.sfc = pg.Surface((block, block)) #Surfaceオブジェクトを作成 <矢島>
        pg.draw.rect(self.sfc, color, (0, 0, block, block)) #Surfaceオブジェクトに白色の正方形を描き込む <矢島>
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得 <矢島>
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct)#Screenオブジェクトに道を描画 <矢島>


class Goal: #ゴール
    color = (255, 0, 255) # 色を固定（子クラスHoleと色が異なるため__init__の外） <児玉>

    def __init__(self,block,maze_obj):
        while True:#ループ処理(初期座標の決定) <矢島>
            self.x = random.randint(0,len(maze_obj.maze_map)-1) #x座標ランダムに設定 <矢島>
            self.y = random.randint(0,len(maze_obj.maze_map[0])-1) #y座標ランダムに設定 <矢島>
            if isinstance(maze_obj.maze_map[self.x][self.y],Road): #初期座標が道であり <矢島>
                if self.x != 1 and self.y != 1: #初期座標がプレイヤーの初期座標で無ければ <矢島>
                    maze_obj.maze_map[self.x][self.y]=self #道をゴールに変更 <矢島>
                    break #ループを脱出 <矢島>
        self.sfc = pg.Surface((block, block)) #1マス分のSurfaceオブジェクトを作成 <矢島>
        pg.draw.rect(self.sfc, self.color, (0, 0, block, block)) #Surfaceオブジェクトに紫色の正方形を描画 <矢島>
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得 <矢島>
    
    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #ゴールの描画 <矢島>

class Hole(Goal): #落とし穴
    #color = (0,0,0) #デバック用(黒色)
    color = "#fff1cf" # 色を固定（親クラスGoalと色が異なるため__init__の外）(Roadと同じ色) <児玉>
    af_color = "#765c47"  # 変更後の色 <矢島>

    def __init__(self, block, maze_obj):
        self.block = block #インスタンス変数に1マスの大きさを保持(色の変更に用いるため) <矢島>
        super().__init__(block, maze_obj) # オーバーライド <児玉>

    def blit(self, screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) # 穴の描画 <児玉>
    
    def chenge_color(self): #色の変更 <矢島>
        pg.draw.rect(self.sfc, self.af_color, (0 ,0, self.block,self.block)) #Surfaceオブジェクトを新しい色の正方形で塗りつぶす <矢島>


class Player: #プレイヤー <矢島> <改訂 児玉>

    key_delta = {pg.K_UP:[0, -1],
                 pg.K_DOWN:[0, 1],
                 pg.K_LEFT:[-1, 0],
                 pg.K_RIGHT:[1, 0]} #押下キーに対する座標遷移のdict <矢島>

    def __init__(self,block,screen_obj):
        self.x , self.y = 4, 4 #迷宮の左上にプレイヤーを配置 <矢島>
        self.block = block #1マスの大きさ <矢島>
        self.sfc = pg.Surface((block, block)) # 1マス分の大きさのSurfaceオブジェクトを作成 <矢島>
        pg.draw.circle(self.sfc, (0, 0, 255), (block/2, block/2), block/2) #Surfaceオブジェクトに青色の丸を表示 <矢島>
        self.sfc.set_colorkey((0, 0, 0)) #丸の背景を黒色に設定 <矢島>
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得 <矢島>
        self.rct.center = block/2+block*(screen_obj.rct.right/block//2), block/2+block*(screen_obj.rct.bottom/block//2) #画面の真ん中にプレイヤーを設置 <矢島>
    
    def blit(self,screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #プレイヤーの描画 <矢島>
    
    def update_xy(self, maze_obj, screen_obj, enemy_lst,block): #プレイヤーの座標を更新 <矢島>
        pressed = pg.key.get_pressed() #押下キーを取得 <矢島>
        x, y = self.x, self.y #現在の座標を取得 <矢島>
        for delta in __class__.key_delta:
            if pressed[delta]:
                x += __class__.key_delta[delta][0]
                y += __class__.key_delta[delta][1]#押下キーに対応して座標を変更 <矢島>
        
        # 移動先による条件分岐
        if isinstance(maze_obj.maze_map[x][y], Hole):# 移動先のマスがゴールだったら  <児玉>
            self.hold_x, self.hold_y = x, y #座標を保持しておく <児玉>
            self.x, self.y = x, y #座標の更新を確定 <児玉>
            maze_obj.maze_map[x][y].chenge_color()
            maze_obj.show_maze(self, block, screen_obj, enemy_lst) #迷宮の描画(プレイヤーではなく迷宮を動かすことによって移動させるため)  <児玉>
            self.blit(screen_obj) #プレイヤーを描画  <児玉>
            pg.display.update() #画面の更新  <児玉>
            under_maze=Maze(MAZE_X,MAZE_Y,WINDOW_BLOCK, 1) #遷移先の迷宮を作成 <矢島>
            time.sleep(1) # 動作の停止(穴に落ちたことを表示するため) <矢島>
            maze_obj.maze_map[x][y] = Road(block, x, y, 0)  # 穴をRoadオブジェクトに変更（一度入った穴を消滅させるため）<児玉>
            return under_maze # play_game()に戻る <矢島>

        elif isinstance(maze_obj.maze_map[x][y], Goal):#移動先のマスがゴールだったら <矢島>
            self.x, self.y = x, y #座標の更新を確定 <矢島>
            maze_obj.show_maze(self, block, screen_obj, enemy_lst) #迷宮の描画(プレイヤーではなく迷宮を動かすことによって移動させるため) <矢島>
            self.blit(screen_obj) #プレイヤーを描画 <矢島>
            pg.display.update() #画面の更新 <矢島>
            time.sleep(1) #ゴールしたことが確認できるための休止期間(1秒) <矢島>
            return "goal" # play_game()に戻る <児玉>

        elif isinstance(maze_obj.maze_map[x][y], Road): #移動先が道だったら <矢島>
            self.x, self.y = x, y #座標の更新を確定 <矢島>
            for enemy in enemy_lst:
                enemy.update_xy(maze_obj) #全ての敵を移動させる <矢島>

        #移動先がゴール又は道でなかった場合、座標の変更を破棄する
    
    def colliderect(self, obj_lst,screen_obj): #衝突判定 <矢島>
        for i,obj in enumerate(obj_lst): #list内の全てのオブジェクトに対して <矢島> <追加　貞野>
            if self.rct.colliderect(obj.rct): #プレイヤーが衝突していれば <矢島>
                obj.blit(screen_obj) #衝突相手を描画 <矢島>
                obj_lst.pop(i) #衝突相手が戦闘画面後に残らないようにリストから除く <貞野>
                pg.display.update() #画面の更新 <矢島>
                time.sleep(1) #確認用の待機時間 <矢島>
                return True #bool値を返す <矢島>
    

class Enemy: #敵オブジェクト <矢島>

    def __init__(self,block,maze_obj,player_obj):
        self.sfc = pg.Surface((block, block)) #1マス分のSurfaceオブジェクトを作成 <矢島>
        pg.draw.circle(self.sfc, (255, 0, 0), (block/2, block/2), block/2) #Surfaceオブジェクト内に赤色の円を描画 <矢島>
        self.sfc.set_colorkey((0, 0, 0)) #円の背景を黒に設定 <矢島>
        self.rct = self.sfc.get_rect() #rectオブジェクトの取得 <矢島>
        while True: #ループ処理(初期座標の設定) <矢島>
            self.x = random.randint(0,len(maze_obj.maze_map)-1) #x座標ランダムに設定 <矢島>
            self.y = random.randint(0,len(maze_obj.maze_map[0])-1) #y座標をランダムに設定 <矢島>
            if isinstance(maze_obj.maze_map[self.x][self.y],Road): #初期値が道であり <矢島>
                if self.x != player_obj.x and self.y != player_obj.y: #プレイヤーの初期座標で無ければ <矢島>
                    break #ループを脱出 <矢島>
    
    def blit(self,screen_obj):
        screen_obj.sfc.blit(self.sfc, self.rct) #敵を描画 <矢島>
    
    def update_xy(self,maze_obj):
        while True: #ループ処理(座標の移動)
            next_x = self.x+random.randint(-1,1) #x座標を現在から-1から+1の間で変更 <矢島>
            next_y = self.y+random.randint(-1,1) #y座標を現在から-1から+1の間で変更 <矢島>
            if (not isinstance(maze_obj.maze_map[next_x][next_y],Wall)) and (type(maze_obj.maze_map[next_x][next_y]) != Goal): #移動先が壁でもゴールでも無ければ (Road or Hole) <矢島>
                self.x, self.y = next_x, next_y #変更を確定 <矢島>
                break #ループを脱出 <矢島>


class Battle: #バトル画面オブジェクト <貞野>
    enemy_img = [pg.image.load("fig/dragon.png"), pg.image.load("fig/ha-pi.png")]
    def __init__(self):
        self.btlbg_sfc = pg.image.load("fig/btlbg.png") #背景画像のSurface <貞野>
        self.effect_attack_sfc = pg.image.load("fig/zangeki.png")  #斬撃エフェクトのSurface <貞野>
        self.effect_magic_sfc = pg.image.load("fig/magic.png") #魔法エフェクトのSurface <貞野>
        self.enemy_sfc = random.choices(Battle.enemy_img, k = 1, weights=[1,3]) #敵エネミーの選択、enemy_imgに画像を追加し、weights=の数値設定に値を追加すれば、出現率の変更が多少可能
        self.enemy_sfc = self.enemy_sfc[0] #敵エネミー（ドラゴン）のSurface <貞野>
        self.enemy_sfc = pg.transform.scale(self.enemy_sfc,  (900, 675))#画像の大きさを(900, 675)に変更 <貞野>
        self.enemy_rct = self.enemy_sfc.get_rect() #rectオブジェクトの取得 <貞野>
        self.enemy_rct.center = (WIDTH/2-self.enemy_sfc.get_width()/2, HEIGHT-self.enemy_sfc.get_height()) #エネミーをウィンドウの中心に <貞野>
        self.player_dmg = 0 #プレイヤーの与えるダメージ　Playerにレベルを追加して攻撃能力が変わる場合はPlayerなどに管理させてください <貞野>
        self.enemy_dmg = 0 #エネミーの与えるダメージ　Enemyにレベルを追加して攻撃能力が変わる場合はEnemyなどに管理させてください <貞野>
        self.enemy_step = 0 #エネルギーが攻撃をする際に画像位置を動かす為の変数 Enemyよって動く幅が変わる場合はEnemyオブジェクトに管理させてください <貞野>
        self.enemy_blink = 0 #エネミーが攻撃を受ける際の点滅を表現するための変数 Enemyなどによって変化させる場合Enemyオブジェクトに管理させてください <貞野>
        self.dmg_effect = 0 #プレイヤーがダメージを受けた際に背景を動かすための変数 Enemyなどによって背景が動かすのを変更する場合Enemyオブジェクトに管理させてください <貞野>
        self.enemy_life = random.randint(1500,3000) #エネミーの体力 Enemyなどによって体力が変わる場合はEnemyオブジェクトに管理させてください <貞野>
        self.turn = 0 #プレイヤーやエネミーがどの行動を行うか判定に使う変数 <貞野>
        self.tmr = 0 #時間経過ごとにどの描画をするか判定に使う変数 <貞野>
        self.message = [""]*10 #Playerと敵エネミーの行動リスト <貞野>
        self.font = pg.font.Font(None, 30) #fontの描画に使うSurface <貞野>

    def blit(self,screen_obj, sfc ,x_y): #<貞野>
        screen_obj.sfc.blit(sfc, x_y) #戦闘画面の描画 <貞野>

    def set_message(self,msg): #<貞野>
        #引数：Playerもしくは敵エネミーの行動
        for i,message in enumerate(self.message):
            #messageが空なら追加しそこで終了 <貞野>
            if message == "":
                self.message[i] = msg
                return
        #空でない場合、上に一つメッセージをずらし、最後に新しいメッサージを追加 <貞野>
        for i in range(len(self.message)-1):
            self.message[i] = self.message[i+1]
        self.message[-1] = msg

    def draw_text(self,screen_obj,txt, x, y, color): #<貞野>
        #渡された文字列から新しいFontSurfaceを作成 <貞野>
        """
        txt :描画する文字列 <貞野>
        x   :横の描画開始位置 <貞野>
        y   :縦の描画開始位置 <貞野>
        color :色 <貞野>
        """
        txt_font = self.font.render(txt, True, color) #引数：txtでcolorの色の文字列のSurfaceを作成 <貞野>
        __class__.blit(self, screen_obj, txt_font, [x, y]) #文字列を描画 <貞野>

    def draw_battle(self,screen_obj):
        #プレイヤーの攻撃やエネミーの攻撃による描画 <貞野>
        #背景を揺らす為の変数 <貞野>
        bx = 0
        by = 0

        if self.dmg_effect > 0: #敵エネミーの行動をする際に背景を上下させるために描画位置を更新 <貞野>
            #dmg_effectの数値分の処理回数だけ背景の位置を変更する <貞野>
            self.dmg_effect -= 1
            bx = random.randint(-20, 20)
            by = random.randint(-10, 10)
        __class__.blit(self, screen_obj,self.btlbg_sfc,[bx,by]) #背景画像を描画 <貞野>
        if self.enemy_blink%2 == 0: #偶然の場合はエネミーの画像を描画 <貞野>
            __class__.blit(self, screen_obj, self.enemy_sfc, [self.enemy_rct.centerx, self.enemy_rct.centery+self.enemy_step]) #エネミーの画像を描画 <貞野>
        if self.enemy_blink > 0: #奇数の場合はカウントだけ更新し、攻撃を受けた際に点滅しているように描画 <貞野>
            self.enemy_blink -= 1
        for i, message in enumerate(self.message): #プレイヤーと敵エネミーの行動を位置をずらしながら描画　<貞野>
            __class__.draw_text(self,screen_obj,message, WIDTH-200, 100+i*50, (255,255,255))

    def battle_command(self,screen_obj): #プレイヤーのコマンドを位置をずらしながら描画　<貞野>
        for i,command in enumerate(COMMAND):
            __class__.draw_text(self,screen_obj, command, 20, HEIGHT/2+60*i,  (255,255,255))

    def battle(self,screen_obj): #<貞野>
        __class__.draw_battle(self,screen_obj) #戦闘画面の描画と更新 <貞野>
        self.tmr += 1 #それぞれの行動ごとの描画するタイミングを更新
        key = pg.key.get_pressed() #押下キーを取得 <貞野>

        if self.turn == 0: # 戦闘開始
            if self.tmr == 1: __class__.set_message(self,"Encounter!") #描画するメッセージを追加 <貞野>
            if self.tmr == 6:
                self.turn = 1 #プレイヤー入力待ちに変更 <貞野>
                self.tmr = 0 #時間経過をリセット <貞野>

        elif self.turn == 1: # プレイヤー入力待ち <貞野>
            if self.tmr == 1: __class__.set_message(self,"Your turn.") #描画するメッセージを追加 <貞野>
            __class__.battle_command(self,screen_obj) #コマンドを描画 <貞野>
            if key[pg.K_a] == True or key[pg.K_SPACE] == True: #aキーかSPACEキーが押された場合、斬撃エフェクトでプレイヤーが行動<貞野>
                self.turn = 2 #プレイヤーの行動に変更 <貞野>
                self.tmr = 0 #時間経過をリセット <貞野>
            if key[pg.K_m] == True: #mキーが押された場合、魔法エフェクトでプレイヤーが行動<貞野>
                self.turn = 3 #プレイヤーの行動に変更 <貞野>
                self.tmr = 0 #時間経過をリセット <貞野>

        elif self.turn == 2 or self.turn == 3: # プレイヤーの行動 <貞野>
            if self.tmr == 1: __class__.set_message(self,"You attack!") #描画するメッセージを追加 <貞野>
            if 2 <= self.tmr <= 6: #プレイヤーの攻撃の描画 <貞野>
                # プレイヤーの入力がaキーかSPACEキーの時、斬撃をエネミーの位置に描画 時間経過ごとに画像の位置を変更し、攻撃を表現 <貞野>
                if self.turn == 2: __class__.blit(self, screen_obj, self.effect_attack_sfc, [self.enemy_rct.centerx*2-self.tmr*(self.enemy_rct.centery/6), self.enemy_rct.centery+self.tmr*(self.enemy_rct.centery/6)])
                # プレイヤーの入力がmキーの時、魔法をエネミーの位置に描画 時間経過ごとに画像の位置を変更し、攻撃を表現 <貞野>
                if self.turn ==3: __class__.blit(self, screen_obj, self.effect_magic_sfc, [self.enemy_rct.centerx, self.tmr*20])
            if self.tmr == 7: #エネミーが攻撃を受けた際の描画 <貞野>
                self.enemy_blink = 5 #エネミーの点滅を追加 <貞野>
                if self.turn == 2:
                    # プレイヤーの入力がaキーかSPACEキーの時、700-900の間でプレイヤーの攻撃ダメージを更新　<貞野>
                    self.player_dmg = random.randint(700,900) #700-900の間で数値を更新 プレイヤーのステータスによって攻撃ダメージを変更する場合、書き換えてください <貞野>
                    __class__.set_message(self,f"{self.player_dmg} damage!") #描画するメッセージを追加 <貞野>
                if self.turn ==3:
                    # プレイヤーの入力がmキーの時、400-1200の間でプレイヤーの攻撃ダメージを更新　<貞野>
                    self.player_dmg = random.randint(400,1200) #400-1200の間で数値を更新 プレイヤーのステータスによって攻撃ダメージを変更する場合、書き換えてください <貞野>
                    __class__.set_message(self,f"{self.player_dmg} damage!") #描画するメッセージを追加 <貞野>
            if self.tmr == 16: #プレイヤーの行動終了
                self.enemy_life -= self.player_dmg #プレイヤーの攻撃ダメージ分のエネミーの体力を減らす。
                if self.enemy_life < 0:
                    #エネミーの体力が0以下になった場合戦闘を終了する
                    __class__.set_message(self,"You win!") #描画するメッセージを追加 <貞野>
                    __class__.draw_battle(self,screen_obj) #戦闘画面の描画 <貞野>
                    pg.display.update() #画面の更新 <貞野>
                    time.sleep(1) #確認用の待機時間 <貞野>
                    return 0 #迷路画面の描画を行うための数値を返す<貞野>

                else:
                    self.turn = 4 #エネミーの行動、エネミーの攻撃に変更
                    self.tmr = 0 #時間経過をリセット <貞野>

        elif self.turn == 4: # エネミーの行動、エネミーの攻撃 <貞野>
            if self.tmr == 1: __class__.set_message(self,"Enemy turn.") #描画するメッセージを追加 <貞野>
            if self.tmr == 5:
                __class__.set_message(self,"Enemy attack!") #描画するメッセージを追加 <貞野>
                self.enemy_step = 30 #エネミーの攻撃の際にエネミーの位置を変更するための移動数値 <貞野>
            if self.tmr == 9:
                #エネミーの攻撃ダメージの設定と背景画像を揺らす為の数値を更新し、エネミーの描画位置を戻す <貞野>
                self.enemy_dmg = random.randint(900,1100) #900-1100の間でエネミーのの攻撃ダメージを更新　<貞野>
                __class__.set_message(self,f"{self.enemy_dmg} damage!") #描画するメッセージを追加 <貞野>
                self.dmg_effect = 5 #背景画像を揺らす為の変数を設定　<貞野>
                self.enemy_step = 0 #エネミーの画像位置を戻す <貞野>
            if self.tmr == 20: #エネミーの行動、エネミーの攻撃の終了 <貞野>
                self.turn = 1 #プレイヤー入力待ちに変更 <貞野>
                self.tmr = 0 #時間経過をリセット <貞野>
        return 1 #戦闘画面の続行のため、戦闘画面の描画を行うための変数を返す <貞野>


def play_game(maze, screen): #<児玉> <改訂 矢島> <追加　貞野>
    mode = 0 #迷路画面の描画と戦闘画面の描画を切り替える変数 <貞野>
    # mount_mazeに現在のいるエリアを格納する <児玉>
    mount_maze = maze #引数の迷路を現在の迷路に設定 <矢島>

    player = Player(WINDOW_BLOCK,screen) #プレイヤーの作成 <矢島>
    enemies = [Enemy(WINDOW_BLOCK,mount_maze,player) for _ in range(NUM_ENEMY)] #敵を格納したlistオブジェクトの作成 <矢島>
    mount_maze.show_maze(player, WINDOW_BLOCK, screen, enemies) #迷宮・敵の描画 <矢島>
    player.blit(screen) #プレイヤーの描画 <矢島>
 
    #ループ処理 <矢島>
    while True:
        pg.display.update() #画面の更新 <矢島>
        if mode == 0: #迷路画面 <貞野>
            mount_maze.show_maze(player,WINDOW_BLOCK,screen,enemies) #迷宮・敵の描画 <矢島>
            player.blit(screen) #プレイヤーの描画 <矢島>
            for event in pg.event.get(): #イベントの取得 <矢島>
                if event.type == pg.QUIT: #ウィンドウの×ボタンが押されたら <矢島>
                    pg.quit() #pygemeの終了 <児玉>
                    sys.exit() #プログラムの終了 <児玉>
                if event.type == pg.KEYDOWN: #キーが押されたら <矢島>
                    pos = player.update_xy(mount_maze, screen, enemies, WINDOW_BLOCK) #プレイヤー・敵の座標の更新<矢島>
                    if pos == "goal": return # ゴールしていれば → メインフロアならmain()に戻る、地下フロアなら一つ上のplay_game()に戻る <児玉>
                    if isinstance(pos, Maze): # 穴を踏んでいれば <児玉>
                        maze=pos #生成した迷宮を受け取る<矢島>
                        play_game(maze, screen) # 生成した地下のマップを引数に与えながら、play_gameを再帰呼び出しする <児玉> <改訂 矢島>
            if player.colliderect(enemies,screen): #敵とプレイヤーが衝突していれば <矢島>
                battle = Battle() #敵と衝突した際にバトル画面のクラスを作成 <貞野>
                mode = 1 #戦闘画面を描画させるためモードを変更 <貞野>

        if mode ==1: #戦闘画面 <貞野>
            for event in pg.event.get(): #イベントの取得 <貞野>
                if event.type == pg.QUIT: #ウィンドウの×ボタンが押されたら <貞野>
                    pg.quit() #pygemeの終了 <貞野>
                    sys.exit() #プログラムの終了 <貞野>
            mode = battle.battle(screen) #Battleクラスのbattleメソッドで戦闘が続く場合は1を、戦闘が終了する場合は0を返す <貞野>


def main(): #メイン関数 <矢島> <改訂 児玉>

    screen = Screen("test", (WIDTH, HEIGHT)) #スクリーンの作成 <矢島>

    # 迷宮の作成
    # メインフロア変数の数分を格納したリストを作成 <児玉>
    '''下図イメージ
    [1階層-メイン, 2階層-メイン, 3階層-メイン, ... , n階層-メイン]    '''    
    maze_lst = [Maze(MAZE_X,MAZE_Y,WINDOW_BLOCK, 0) for _ in range(MAIN_FLOOR_LEN)]

    # フロア（階層）を回す <児玉>
    for maze in maze_lst:
        play_game(maze, screen) # play_gameを呼び出し、プレイを開始する <児玉>


if __name__ == "__main__":
    pg.init() #pygameを初期化
    main() #ゲームの実行
    pg.quit() #pygemeの終了
    sys.exit() #プログラムの終了