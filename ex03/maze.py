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
    global mx, my
    if key=="Up" and maze[mx][my-1]==0: #上キー押下時かつ上のマスが道であるとき
        my-=1
    elif key=="Down" and maze[mx][my+1]==0: #下キー押下時かつ上のマスが道であるとき
        my+=1
    elif key=="Left" and maze[mx-1][my]==0: #左キー押下時かつ上のマスが道であるとき
        mx-=1
    elif key=="Right" and maze[mx+1][my]==0: #右キー押下時かつ上のマスが道であるとき
        mx+=1
    cx=mx*100+50 #x座標を計算
    cy=my*100+50 #y座標を計算
    canvas.coords("koukaton_1",cx,cy) #こうかとんの位置を更新
    root.after(300,main_proc) #0.3秒後に再度リアルタイム処理関数を実行



if __name__=="__main__": #メイン関数
    #変数の設定
    mx=1 #こうかとんのxマス
    my=1 #こうかとんのyマス
    key="" #現在押されているキー
    maze_x=15 #迷路のx方向
    maze_y=9 #迷路のy方向
    maze=make_maze(maze_x,maze_y) #迷路の作成（2次元リスト x*y）
    maze[1][1]=2 #スタート地点の設置
    maze[maze_x-2][maze_y-2]=3 #ゴール地点の設置

    #GUIの表示
    root=tk.Tk()
    root.title("迷えるこうかとん")
    canvas=tk.Canvas(root,width=1500,height=900,bg="black") #キャンバスの作成
    canvas.pack()
    show_maze(canvas,maze) #迷路を作成
    koukaton=tk.PhotoImage(file="./fig/0.png") #画像用オブジェクトの作成
    canvas.create_image(mx*100+50,mx*100+50,image=koukaton,tag="koukaton_1") #画像の配置
    root.bind("<KeyPress>",key_down) #キー押下時の操作
    root.bind("<KeyRelease>",key_up) #キー開放時の操作
    main_proc() #リアルタイム処理
    root.mainloop() #GUI表示