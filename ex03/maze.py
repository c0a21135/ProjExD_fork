import tkinter as tk


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
    cx=300
    cy=400
    key=""

    root=tk.Tk()
    root.title("maze")
    canvas=tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.pack()
    koukaton=tk.PhotoImage(file="./fig/0.png")
    canvas.create_image(cx,cy,image=koukaton,tag="koukaton_1")
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    main_proc()
    root.mainloop()