import tkinter as tk
import tkinter.messagebox as tkm


def button_click(num):
    tkm.showinfo("押すな",f"{num}のボタンが押されました。")

root=tk.Tk()
root.title("calculate")
button_9=tk.Button(root,text="9",font=("",30),width=4,height=2,command=lambda:button_click(9))
button_9.grid(row=0,column=0)
button_8=tk.Button(root,text="8",font=("",30),width=4,height=2,command=lambda:button_click(8))
button_8.grid(row=0,column=1)
button_7=tk.Button(root,text="7",font=("",30),width=4,height=2,command=lambda:button_click(7))
button_7.grid(row=0,column=2)
button_6=tk.Button(root,text="6",font=("",30),width=4,height=2,command=lambda:button_click(6))
button_6.grid(row=1,column=0)
button_5=tk.Button(root,text="5",font=("",30),width=4,height=2,command=lambda:button_click(5))
button_5.grid(row=1,column=1)
button_4=tk.Button(root,text="4",font=("",30),width=4,height=2,command=lambda:button_click(4))
button_4.grid(row=1,column=2)
button_3=tk.Button(root,text="3",font=("",30),width=4,height=2,command=lambda:button_click(3))
button_3.grid(row=2,column=0)
button_2=tk.Button(root,text="2",font=("",30),width=4,height=2,command=lambda:button_click(2))
button_2.grid(row=2,column=1)
button_1=tk.Button(root,text="1",font=("",30),width=4,height=2,command=lambda:button_click(1))
button_1.grid(row=2,column=2)
button_0=tk.Button(root,text="0",font=("",30),width=4,height=2,command=lambda:button_click(0))
button_0.grid(row=3,column=0)
root.mainloop()