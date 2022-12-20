# 標準ライブラリのimport
import sys
import random

# 拡張モジュールのimport
import pygame as pg


class Screen: # スクリーン

    def __init__(self, title, width_height, bg_img): 
        pg.display.set_caption(title) #タイトルの設定
        self.scrn_sfc = pg.display.set_mode(width_height) #スクリーンのサイズを設定
        self.scrn_rct = self.scrn_sfc.get_rect() #スクリーンのrectオブジェクトを取得
        self.bg_sfc = pg.image.load(bg_img) #背景画像のsurfaceオブジェクトを取得
        self.bg_rct = self.bg_sfc.get_rect() #背景画像のrectオブジェクトを取得
    
    def blit(self): #背景画像の描画
        self.scrn_sfc.blit(self.bg_sfc, self.bg_rct) 


class Bird: #こうかとん

    key_delta = {pg.K_UP:(0, -1), pg.K_DOWN:(0, 1), pg.K_LEFT:(-1, 0), pg.K_RIGHT:(1, 0)} #押下キーによるこうかとんの進行方向のdict

    def __init__(self, img_path, magnification, x_y):
        self.tori_sfc = pg.image.load(img_path) #こうかとんの画像を取得
        self.tori_sfc = pg.transform.rotozoom(self.tori_sfc,
                                              0,
                                              magnification) #こうかとん画像の拡大
        self.tori_rct = self.tori_sfc.get_rect() #こうかとんのrectオブジェクトを取得
        self.tori_rct.center = x_y #こうかとんの座標を設定
    
    def blit(self, screen_obj): #こうかとんをスクリーンに描画
        screen_obj.scrn_sfc.blit(self.tori_sfc, self.tori_rct)
    
    def update(self, screen_obj): #こうかとんの位置更新
        pressed = pg.key.get_pressed() #押下中のキーを辞書形式で取得
        for delta in __class__.key_delta: #方向キー毎に
            if pressed[delta]: #方向キーが押されていたら
                x, y = __class__.key_delta[delta]
                self.tori_rct.move_ip(x, y) #対応した方向にこうかとんの位置を更新
            if check_bound(self.tori_rct, screen_obj.scrn_rct) != (+1, +1): #こうかとんが場外に出たら
                self.tori_rct.move_ip(-x, -y) #こうかとんの位置を元に戻す
        __class__.blit(self, screen_obj) #こうかとんの描画
    
    def take_over(self, x, y): #こうかとんの位置の引き継ぎ
        self.tori_rct.center = x, y


class Bomb: #爆弾

    def __init__(self, color, radius, velocity, screen_obj):#(self, 色, 半径, 速度のタプル(x方向,y方向), スクリーンオブジェクト)
        self.vx, self.vy = velocity #速度のタプルからx方向y方向を取り出す
        self.sfc = pg.Surface((radius*2, radius*2)) #surfaceオブジェクトを取得
        self.sfc.set_colorkey((0, 0, 0)) #背景を黒に設定
        pg.draw.circle(self.sfc, color, (10, 10), radius) #円をsurfaceオブジェクトに描画
        self.rct = self.sfc.get_rect() #rectオブジェクトを取得
        self.rct.center = random.randint(10,screen_obj.scrn_rct.right-10), random.randint(10,screen_obj.scrn_rct.bottom-10) #初期座標をランダムに設定
    
    def update(self, screen_obj): #位置の更新
        self.rct.move_ip(self.vx, self.vy) #位置を更新
        yoko, tate = check_bound(self.rct, screen_obj.scrn_rct) #更新位置がスクリーン外か判定(スクリーン内であったら1が、外であったら-1が返る)
        self.vx *= yoko #スクリーン外であったら速度を反転
        self.vy *= tate
        __class__.blit(self, screen_obj)#爆弾の描画
    
    def blit(self, screen_obj): #スクリーンに爆弾の描画
        screen_obj.scrn_sfc.blit(self.sfc, self.rct)


class Bomb_List(list): #爆弾を格納するlistオブジェクト

    def __init__(self,bomb_num, color, radius, velocity, screen_obj):
        super().__init__(self) #listオブジェクトのイニシャライザを実行
        #Bonbクラス用の値をインスタンス変数に設定
        self.color = color 
        self.radius = radius
        self.velocity = velocity
        self.screen_obj = screen_obj
        #list内にbomb_numの個数分Bombオブジェクトを追加
        for _ in range(bomb_num): 
            self.append(Bomb(color, radius, velocity, screen_obj))
    
    def plus_bomb(self, bomb_num): #爆弾の追加
        for _ in range(bomb_num): #list内にbomb_numの個数分Bombオブジェクトを追加
            self.append(Bomb(self.color, self.radius, self.velocity, self.screen_obj))
    
    def blit(self): #爆弾の描画
        for bomb_obj in self:
            bomb_obj.blit(self.screen_obj)

    def update(self): #爆弾の位置を更新
        for bomb_obj in self:
            bomb_obj.update(self.screen_obj)
    
    def colliderect(self, obj_rct, mode=0): #衝突判定(mode=0：爆弾が消失, mode=1：爆弾が反射)
        for i, bomb_obj in enumerate(self): #全ての爆弾に対して
            if obj_rct.colliderect(bomb_obj.rct): #ぶつかっていたら
                if mode ==0:
                    self.pop(i) #爆弾を消去
                if mode ==1:
                    bomb_obj.vx *= -1 #爆弾を反射
                    bomb_obj.vy *= -1 #爆弾を反射
                return True


class Shot(Bomb): #こうかとんが発射する弾(Bombオブジェクトを継承)

    key_delta = {pg.K_UP:(0, -1), pg.K_DOWN:(0, 1), pg.K_LEFT:(-1, 0), pg.K_RIGHT:(1, 0)} #押下キーによる弾の進行方向のdict

    def __init__(self, color, radius, screen_obj, tori_rct):

        #押下中のキーに基づいた進行方向の決定
        pressed = pg.key.get_pressed() #押下中のキーの取得
        vx, vy = 0, 0
        for delta in __class__.key_delta:
            if pressed[delta]:
                dx, dy = __class__.key_delta[delta]
                vx += dx
                vy += dy
        if (vx, vy) == (0, 0): #動いていない場合
            vx, vy = -1, -1 #左上方向に設定
        velocity = (vx, vy)
        super().__init__(color, radius, velocity, screen_obj) #設定した速度に基づいてBombオブジェクトのイニシャライザを参照
        self.rct.center = tori_rct.x, tori_rct.y #初期位置をこうかとんの位置に変更


class Shot_List(list): #こうかとんが発射した弾を格納するlistオブジェクト

    def __init__(self, color, radius, screen_obj):
        super().__init__(self) #listオブジェクトのイニシャライザを参照
        #Shotオブジェクトの生成に用いる引数をインスタンス変数に格納
        self.color = color
        self.radius = radius
        self.screen_obj = screen_obj

    def  puls_shot(self, tori_rct): #弾の追加
        if len(self)<=5: #現在の発射している弾が5個以下だったら
            pressed = pg.key.get_pressed() #押下中のキーを取得
            if pressed[pg.K_SPACE]: #スペースキーが押されていたら
                self.append(Shot(self.color, self.radius, self.screen_obj, tori_rct)) #Shotオブジェクトを追加
    
    def blit(self): #弾の描画
        for shot_obj in self:
            shot_obj.blit(self.screen_obj)

    def update(self): #弾の位置の更新
        for bomb_obj in self:
            bomb_obj.update(self.screen_obj)


def check_bound(obj_rct, scr_rct): #第一引数のrectオブジェクトが第二引数のスクリーンの場外かどうかを判定
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main(): #ゲーム全体の動作

    #変数の設定
    WIDTH=1600 #ウィンドウの横幅
    HEIGHT=900 #ウィンドウの縦幅
    VX, VY=1, 1 #爆弾のx方向、y方向の増減値
    ADD_TIME=2000 #爆弾を追加する時間(ミリ秒)
    BOMB_NUM=5 #爆弾の数の初期値
    ADD_BOMB_NUM=5 #追加される爆弾の数
    tori_num=0 #現在のこうかとんの画像番号
    tori_obj_lst=[0 for _ in range(10)] #こうかとんの画像を格納するリスト

    #初期設定
    screen=Screen("負けるな！こうかとん", (WIDTH, HEIGHT), "./fig/pg_bg.jpg") #スクリーンの作成
    screen.blit() #スクリーンの描画
    clock = pg.time.Clock() #Clockオブジェクトのインスタンスを作成
    clock.tick(60) #フレームレートの作成
    #こうかとんの画像をリストに格納
    for i in range(10):
        tori_obj = Bird(f"./fig/{i}.png", 2.0, (900, 400)) #こうかとんのオブジェクトを作成
        tori_obj_lst[i]=tori_obj #リストに格納
    tori_obj = tori_obj_lst[tori_num] #tori_numに設定されたこうかとんを現在のこうかとんとして呼び出し
    tori_obj.blit(screen) #こうかとんを描画
    #爆弾を設定
    bomb_obj_lst=Bomb_List(BOMB_NUM, (255, 0, 0), 10, (VX, VY), screen)
    #こうかとんが発射する弾の設定
    shot_obj_lst = Shot_List((0, 0, 255), 10, screen)

    #逐次処理
    while True:
        pg.display.update() #画面を更新
        timer= pg.time.get_ticks() #現在のミリ秒を取得
        screen.blit() #背景を描画
        shot_obj_lst.blit() #発射した弾を描画
        tori_obj.blit(screen) #こうかとんを描画
        bomb_obj_lst.update()#爆弾の位置を更新
        shot_obj_lst.update() #弾の位置を更新
        tori_obj.update(screen) #こうかとんの移動処理

        #イベント処理
        for event in pg.event.get(): #イベントを取得
            if event.type == pg.QUIT: #ウィンドウの×ボタンが押されたらゲームを終了する
                return
            if event.type == pg.KEYDOWN: #キーが押下されたら
                shot_obj_lst.puls_shot(tori_obj.tori_rct) #こうかとんが弾を発射(オブジェクト内で押下キーがスペースかどうか判断)
        
        #爆弾とこうかとんの衝突時の処理
        if bomb_obj_lst.colliderect(tori_obj.tori_rct, 1): #爆弾がこうかとんと衝突していれば(当たっていれば爆弾は反射)
            tori_num+=1 #こうかとんの番号を更新
            if tori_num >=10: #次のこうかとんがなければ
                return #ゲームを終了
            else:
                tori_obj_lst[tori_num].take_over(tori_obj.tori_rct.x, tori_obj.tori_rct.y) #次のこうかとんに現在のこうかとんの位置を引き継ぐ
                tori_obj = tori_obj_lst[tori_num] #こうかとんを次の画像に更新
        
        #こうかとんが発射した弾と爆弾との衝突判定
        for i,shot_obj in enumerate(shot_obj_lst): #それぞれの弾に対して
            if bomb_obj_lst.colliderect(shot_obj.rct, 0): #爆弾と当たっていれば(当たっていれば爆弾は消失)
                shot_obj_lst.pop(i) #弾を消去
     
        #時間ごとに爆弾を追加
        if timer%ADD_TIME==0: #時間ごとに爆弾
            bomb_obj_lst.plus_bomb(ADD_BOMB_NUM) #爆弾を追加
            

if __name__ == "__main__":
    pg.init() #pygameを初期化
    main() #ゲームの実行
    pg.quit() #pygemeの終了
    sys.exit() #プログラムの終了