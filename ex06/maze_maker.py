import random


def make_maze(yoko, tate):
    XP = [ 0, 1, 0, -1]
    YP = [-1, 0, 1,  0]

    maze_lst = [[1 for i in range(tate)] for j in range(yoko)]  #大きさがtate*yokoの「1」の2次元リスト
    for maze_yoko in range(1, len(maze_lst)-1): #壁ではない部分を0にする
        for cell in range(1, len(maze_lst[0])-1):
            maze_lst[maze_yoko][cell] = 0
    for y in range(2, tate-2, 2): #迷路を作る
        for x in range(2, yoko-2, 2):
            maze_lst[x][y] = 1
            if x > 2:
                rnd = random.randint(0, 2)
            else:
                rnd = random.randint(0, 3)
            maze_lst[x+YP[rnd]][y+XP[rnd]] = 1
    return maze_lst


# ダンジョンを生成する関数 <山本>
def create_dungeon(yoko, tate): 
    """迷路を基に小部屋有りダンジョンを生成する関数"""
    maze_lst = make_maze(yoko, tate) #基となる迷路を生成 <山本>
    dungeon = [[1 for i in range(tate*3)] for j in range(yoko*3)] #迷路の縦横3倍の大きさのダンジョン用リスト <山本>

    for y in range(1, yoko-1):
        for x in range(1, tate-1):
            dx, dy = x*3+1, y*3+1 # ダンジョンリスト用の移動距離 <山本>
            if maze_lst[y][x] == 0: # もし迷路が道ならば <山本>
                if random.randint(0, 99) < 20: #20％の確率で部屋を生成する <山本>
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0 #周囲の3マスを道にする <山本>
                else: # 部屋が生成されなかったとき通路を作る <山本>
                    dungeon[dy][dx] = 0
                    if maze_lst[y-1][x] == 0: #上方向に道が続いていたらダンジョンリスト内でも上方向に道を伸ばす <山本>
                        dungeon[dy-1][dx] = 0
                    if maze_lst[y+1][x] == 0: #下方向に道が続いていたら <山本>
                        dungeon[dy+1][dx] = 0
                    if maze_lst[y][x-1] == 0: #左方向に道が続いていたら <山本>
                        dungeon[dy][dx-1] = 0
                    if maze_lst[y][x+1] == 0: #右方向に道が続いていたら <山本>
                        dungeon[dy][dx+1] = 0        
    return dungeon


def show_maze(canvas, maze_lst):
    color = ["white", "gray"]
    for x in range(len(maze_lst)):
        for y in range(len(maze_lst[x])):
            canvas.create_rectangle(x*100, y*100, x*100+100, y*100+100, fill=color[maze_lst[x][y]])


#2次元リストを渡すとCUIで迷路を表示
def print_maze(maze_lst):
    maze_lst = [list(x) for x in zip(*maze_lst)] #転置
    for i in maze_lst:
        for j in i:
            if j == 1:
                j = "■"
            else:
                j = "□"
            print(j,end="")
        print()


#maze_makerテスト用
if __name__ == "__main__":
    maze = make_maze(15,9)
    print_maze(maze)

    print()

    dmaze = create_dungeon(15, 6)
    print_maze(dmaze)