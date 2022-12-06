import tkinter as tk
from maze_maker import make_maze


def key_down(event): #キー押下時の操作
    global key
    key=event.keysym #グローバル変数keyを現在押下中のキーに変更



def key_up(event): #キー開放時の操作
    global key
    key="" #グローバルkeyを初期値に変更



def show_maze(canvas, maze_lst): #迷路の表示
    color = ["white", "gray","orange","SkyBlue"] #スタート地点,ゴール地点の色を追加
    for x in range(len(maze_lst)):
        for y in range(len(maze_lst[x])):
            canvas.create_rectangle(x*100, y*100, x*100+100, y*100+100, fill=color[maze_lst[x][y]])



def main_proc(): #リアルタイム処理
    global mx, my, koukaton

    #押下されたキーによる条件分岐
    if key=="Up" and maze[mx][my-1]!=1: #上キー押下時かつ上のマスが壁でないとき
        my-=1
    elif key=="Down" and maze[mx][my+1]!=1: #下キー押下時かつ上のマスが壁でないとき
        my+=1
    elif key=="Left" and maze[mx-1][my]!=1: #左キー押下時かつ上のマスが壁でないとき
        mx-=1
    elif key=="Right" and maze[mx+1][my]!=1: #右キー押下時かつ上のマスが壁でないとき
        mx+=1
    elif key=="a": #aキー押下時オートモード実行
        auto_maze()
    elif key == "i": #i キー押下時初期化
        init_maze()
    elif key in [str(i) for i in range(10)]: #数字キーが押されたとき
        canvas.delete("koukaton") #現在のこうかとんを消去
        koukaton=int(key)
        canvas.create_image(mx*100+50,my*100+50,image=koukaton_lst[koukaton],tag="koukaton") #数字キーに対応したこうかとんの表示

    #こうかとんの位置を変更        
    cx=mx*100+50 #x座標を計算
    cy=my*100+50 #y座標を計算
    canvas.coords("koukaton",cx,cy) #こうかとんの位置を更新
    root.after(100,main_proc) #0.1秒後に再度リアルタイム処理関数を実行



def auto_maze(): #左手の法則によるゴール探索
    global mx, my, dir

    # 左手法のアルゴリズム
    # 左隣に壁がある && 前に壁がある => 右回転
    # 左隣に壁がある && 前に壁がない => 前進
    # 左隣に壁がない => 左回転して前進

    #変数の設定
    dir_x=[1,0,-1,0] #方向に対するx座標の変化
    dir_y=[0,1,0,-1] #方向に対するy座標の変化
    left_dir=(dir+3)%4 #現在の方向に対する左の方向
    next_x=mx+dir_x[dir] #前方向のx座標
    next_y=my+dir_y[dir] #前方向のy座標
    left_x=mx+dir_x[left_dir] #左手方向のx座標
    left_y=my+dir_y[left_dir] #左手方向のy座標

    #移動
    if maze[left_x][left_y]==1: #左手方向が壁であったら
        if maze[next_x][next_y]==1: #前方向が壁であったら
            dir=(dir+1)%4 #右回転
        else:
            mx+=dir_x[dir] #前進
            my+=dir_y[dir]
    else:
        dir=left_dir #左手方向に回転
        mx, my = left_x, left_y #左手方向に前進
    if maze[mx][my]!=3: #現在位置がゴールでなかったら
        root.after(100,auto_maze) #0.1秒後にもう一度自身を呼び出す




def init_maze(): #初期化関数
    global mx, my, key, dir, koukaton
    mx=1 #こうかとんのxマス
    my=1 #こうかとんのyマス
    key="" #現在押されているキー
    dir=0 #現在向いている方向
    koukaton=0 #こうかとんの画像判別
    canvas.delete("koukaton") #現在のこうかとんを消去
    canvas.create_image(mx*100+50,my*100+50,image=koukaton_lst[koukaton],tag="koukaton") #初期設定のこうかとんを表示


if __name__=="__main__": #メイン関数

    #変数の設定
    mx=1 #こうかとんのxマス
    my=1 #こうかとんのyマス
    key="" #現在押されているキー
    maze_x=15 #迷路のx方向
    maze_y=9 #迷路のy方向
    dir=0 #現在の向いている方向
    koukaton=0 #こうかとんの画像判別
    maze=make_maze(maze_x,maze_y) #迷路の作成（2次元リスト x*y）
    maze[1][1]=2 #スタート地点の設置
    maze[maze_x-2][maze_y-2]=3 #ゴール地点の設置

    #GUIの表示
    root=tk.Tk()
    root.title("迷えるこうかとん")
    canvas=tk.Canvas(root,width=1500,height=900,bg="black") #キャンバスの作成
    canvas.pack()
    show_maze(canvas,maze) #迷路を作成
    koukaton_lst=[tk.PhotoImage(file=f"./fig/0.png"), #こうかとんの画像のリスト
                  tk.PhotoImage(file=f"./fig/1.png"),
                  tk.PhotoImage(file=f"./fig/2.png"),
                  tk.PhotoImage(file=f"./fig/3.png"),
                  tk.PhotoImage(file=f"./fig/4.png"),
                  tk.PhotoImage(file=f"./fig/5.png"),
                  tk.PhotoImage(file=f"./fig/6.png"),
                  tk.PhotoImage(file=f"./fig/7.png"),
                  tk.PhotoImage(file=f"./fig/8.png"),
                  tk.PhotoImage(file=f"./fig/9.png")]
    canvas.create_image(mx*100+50,my*100+50,image=koukaton_lst[koukaton],tag="koukaton") #画像の配置
    root.bind("<KeyPress>",key_down) #キー押下時の操作
    root.bind("<KeyRelease>",key_up) #キー開放時の操作
    main_proc() #リアルタイム処理
    root.mainloop() #GUI表示