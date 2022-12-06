import tkinter as tk
from maze_maker import make_maze,show_maze


def key_down(event):
    global key
    key=event.keysym

def key_up(event):
    global key
    key=""

def main_proc():
    global cx, cy
    if key=="Up":
        cy-=20
    elif key=="Down":
        cy+=20
    elif key=="Left":
        cx-=20
    elif key=="Right":
        cx+=20
    canvas.coords("koukaton_1",cx,cy)
    root.after(300,main_proc)



if __name__=="__main__":
    cx=150
    cy=150
    key=""
    maze=make_maze(15,9)

    root=tk.Tk()
    root.title("迷えるこうかとん")
    canvas=tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.pack()
    show_maze(canvas,maze)
    koukaton=tk.PhotoImage(file="./fig/0.png")
    canvas.create_image(cx,cy,image=koukaton,tag="koukaton_1")
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    main_proc()
    root.mainloop()