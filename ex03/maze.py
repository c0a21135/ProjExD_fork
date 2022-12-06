import tkinter as tk
from maze_maker import make_maze,show_maze


def key_down(event):
    global key
    key=event.keysym

def key_up(event):
    global key
    key=""

def main_proc():
    global mx, my
    if key=="Up" and maze[mx][my-1]==0:
        my-=1
    elif key=="Down" and maze[mx][my+1]==0:
        my+=1
    elif key=="Left" and maze[mx-1][my]==0:
        mx-=1
    elif key=="Right" and maze[mx+1][my]==0:
        mx+=1
    cx=mx*100+50
    cy=my*100+50
    canvas.coords("koukaton_1",cx,cy)
    root.after(300,main_proc)



if __name__=="__main__":
    mx=1
    my=1
    key=""
    maze=make_maze(15,9)

    root=tk.Tk()
    root.title("迷えるこうかとん")
    canvas=tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.pack()
    show_maze(canvas,maze)
    koukaton=tk.PhotoImage(file="./fig/0.png")
    canvas.create_image(mx*100+50,mx*100+50,image=koukaton,tag="koukaton_1")
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    main_proc()
    print(maze)
    root.mainloop()