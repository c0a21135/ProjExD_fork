import pygame as pg
import sys
import random

def main(): #ゲーム全体の動作

    #変数の設定
    WIDTH=1600 #ウィンドウの横幅
    HEIGHT=900 #ウィンドウの縦幅
    vx, vy=1, 1 #爆弾のx方向、y方向の増減の初期値
    tori_num=0 #現在のこうかとんの画像番号
    add_time=10000 #爆弾を追加する時間
    bomb_num=5 #爆弾の数の初期値
    tori_sfc_lst=[0 for _ in range(10)] #こうかとんの画像を格納するリスト
    bomb_sfc_lst=[0 for _ in range(bomb_num)] #爆弾を格納するリストの設定

    #ウィンドウの作成
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((WIDTH, HEIGHT))

    #フレームレートの設定
    clock = pg.time.Clock()
    clock.tick(60)

    #背景の設定
    bg_sfc = pg.image.load("./fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()
    scrn_sfc.blit(bg_sfc, bg_rct)

    #こうかとんの画像を設定
    for i in range(10):
        tori_sfc_ele = pg.image.load(f"./fig/{i}.png") #こうかとんの画像読み込む
        tori_sfc_ele = pg.transform.rotozoom(tori_sfc_ele, 0, 2.0) #サイズの設定
        tori_rct_ele = tori_sfc_ele.get_rect() #rectオブジェクトの生成
        tori_rct_ele.center = 900, 400 #初期位置の設定
        tori_sfc_lst[i]=[tori_sfc_ele, tori_rct_ele] #リストに格納
    
    tori_sfc, tori_rct=tori_sfc_lst[tori_num][0], tori_sfc_lst[tori_num][1] #tori_numに設定されたこうかとんを現在のこうかとんとして呼び出し
    scrn_sfc.blit(tori_sfc, tori_rct) #こうかとんを描画

    #爆弾を設定
    for i in range(len(bomb_sfc_lst)):
        draw_sfc = pg.Surface((20, 20)) #surfaceオブジェクトの生成
        draw_sfc.set_colorkey((0,0,0)) #爆弾の背景の設定
        pg.draw.circle(draw_sfc,(255,0,0),(10, 10),10) #爆弾の生成
        bomb_rct = draw_sfc.get_rect() #rectオブジェクトの生成
        bomb_rct.center= random.randint(10,WIDTH-10), random.randint(10,HEIGHT-10) #初期位置をランダムに設定
        bomb_sfc_lst[i] = [draw_sfc,bomb_rct,[vx,vy]] #爆弾の情報をリストに追加([爆弾のsurfaceオブジェクト,爆弾のrectオブジェクト,[爆弾のx方向の増減値,爆弾のy方向の増減値]])
    
    #爆弾の描画
    for bomb_sfc in bomb_sfc_lst:
        scrn_sfc.blit(bomb_sfc[0], bomb_sfc[1])

    while True:
        pg.display.update() #画面を更新
        pg.event.pump() #おまじない
        pressed = pg.key.get_pressed() #押下中のキーを辞書形式で取得
        timer= pg.time.get_ticks() #現在のミリ秒を取得
        scrn_sfc.blit(bg_sfc, bg_rct) #背景を描画
        scrn_sfc.blit(tori_sfc, tori_rct) #こうかとんを描画

        #爆弾の位置を更新
        for bomb_sfc in bomb_sfc_lst:
            if 0>bomb_sfc[1].x+bomb_sfc[2][0] or bomb_sfc[1].x+bomb_sfc[2][0]>WIDTH: #爆弾のx方向の移動先が画面外であったら
                bomb_sfc[2][0]*=-1 #x方向の進行方向を反転
            if 0>bomb_sfc[1].y+bomb_sfc[2][1] or bomb_sfc[1].y+bomb_sfc[2][1]>HEIGHT: #爆弾のy方向の移動先が画面外であったら
                bomb_sfc[2][1]*=-1 #y方向の進行方向を反転
            bomb_sfc[1].move_ip(bomb_sfc[2][0], bomb_sfc[2][1]) #設定した進行方向に基づいて爆弾の位置を更新
            scrn_sfc.blit(bomb_sfc[0], bomb_sfc[1]) #爆弾を描画

        #イベント処理
        for event in pg.event.get(): #イベントを取得
            if event.type == pg.QUIT: #ウィンドウの×ボタンが押されたらゲームを終了する
                return
        
        #こうかとんの移動処理
        if pressed[pg.K_UP] and tori_rct.y-1>=0: #↑キーが押されていてこうかとんの上が画面外でなければ
            tori_rct.move_ip(0, -1) #こうかとんを上に移動
        if pressed[pg.K_DOWN] and tori_rct.y+1<HEIGHT-140:#↓キーが押されていてこうかとんの上が画面外でなければ
            tori_rct.move_ip(0, 1) #こうかとんを下に移動
        if pressed[pg.K_LEFT] and tori_rct.x-1>=0:#←キーが押されていてこうかとんの上が画面外でなければ
            tori_rct.move_ip(-1, 0) #こうかとんを左に移動
        if pressed[pg.K_RIGHT] and tori_rct.x+1<WIDTH-96:#→キーが押されていてこうかとんの上が画面外でなければ
            tori_rct.move_ip(1, 0) #こうかとんを右に移動
        
        #爆弾との衝突時の処理
        for bomb_sfc in bomb_sfc_lst: #全ての爆弾に対して
            if tori_rct.colliderect(bomb_sfc[1]): #こうかとんとぶつかっていたら
                tori_num+=1 #こうかとんを次の画像に更新
                bomb_sfc[2][0]*=-1 #爆弾を反射
                bomb_sfc[2][1]*=-1 #爆弾を反射
                if tori_num>=10: #次の爆弾がなければ
                    return #ゲームを終了
                else:
                    tori_sfc_lst[tori_num][1].center = tori_rct.x, tori_rct.y #次のこうかとんに現在のこうかとんの位置を引き継ぐ
                    tori_sfc, tori_rct=tori_sfc_lst[tori_num][0], tori_sfc_lst[tori_num][1] #こうかとんを次の画像に更新
        
        #時間ごとに爆弾を追加
        if timer%add_time==0:
            #爆弾の作成
            new_bomb=pg.Surface((20, 20))
            new_bomb.set_colorkey((0,0,0))
            pg.draw.circle(new_bomb,(255,0,0),(10, 10),10)
            new_bomb_rct = new_bomb.get_rect()
            new_bomb_rct.center= random.randint(10,WIDTH-10), random.randint(10,HEIGHT-10)
            #爆弾をリストに追加
            bomb_sfc_lst.append([new_bomb,new_bomb_rct,[vx,vy]])
            

if __name__ == "__main__":
    pg.init() #pygameを初期化
    main() #ゲームの実行
    pg.quit() #pygemeの終了
    sys.exit() #プログラムの終了