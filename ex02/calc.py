import tkinter as tk
import tkinter.messagebox as tkm


def button_click(event):
    btn=event.widget
    num=btn["text"]
    if num=="=":
        formula=input_text.get()
        input_text.delete(0,tk.END)
        try:
            formula=formula.replace("×","*")
            formula=formula.replace("÷","/")
            ans=eval(formula)
            input_text.insert(tk.END,str(ans))
        except:
            input_text.insert(tk.END,"エラー")
    elif num=="BS":
        formula=input_text.get()
        input_text.delete(0,tk.END)
        input_text.insert(tk.END,formula[:-1])
    elif num=="C":
        input_text.delete(0,tk.END)
    else:
        if num=="+" or num=="÷" or num=="×":
            try:
                formula=input_text.get()[-1]
            except:
                formula=""
            if formula in ["+","-","×","÷",""]:
                pass
            else:
                input_text.insert(tk.END,(num))
        elif num=="-":
            try:
                formula=input_text.get()[-1]
            except:
                formula=""
            if formula=="-":
                pass
            else:
                input_text.insert(tk.END,num)    
        else:
            input_text.insert(tk.END,num)


def chenge_bg(event):
    event.widget["bg"]="#87CEEB"
def back_bg(event):
    event.widget["bg"]="SystemButtonFace"



root=tk.Tk()
root.title("calculate")

input_text=tk.Entry(width=12,font=("",40),justify=tk.RIGHT)
input_text.grid(row=0,column=0,columnspan=4)

button_labels=[["+","-","×","÷","="],["1/x","C","BS"],["+/-","0","."]]
for i in range(20):
    if i%4==3:
        bl=button_labels[0][i//4]
    elif i//4==0:
        bl=button_labels[1][i%4]
    elif i//4==4:
        bl=button_labels[2][i%4]
    else:
        bl=(4-i//4)*3-i%4
    button=tk.Button(root,text=str(bl),font=("",30),width=4,height=2)
    button.bind("<1>",button_click)
    button.bind("<Enter>",chenge_bg)
    button.bind("<Leave>",back_bg)    
    button.grid(row=1+i//4,column=i%4)
root.mainloop()