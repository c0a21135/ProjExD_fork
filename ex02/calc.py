import tkinter as tk
import tkinter.messagebox as tkm
import math


def button_click(event):
    btn=event.widget
    num=btn["text"]
    if num=="=":
        calc()
    elif num=="BS":
        formula=input_text.get()
        input_text.delete(0,tk.END)
        input_text.insert(tk.END,formula[:-1])
    elif num=="C":
        input_text.delete(0,tk.END)
    else:
        ch_ope=check_ope(num)
        if ch_ope==True:
            input_text.insert(tk.END,num)

def check_ope(ope):
    if ope=="+" or ope=="÷" or ope=="×":
        try:
            formula=input_text.get()[-1]
        except:
            formula=""
        if formula in ["+","-","×","÷",""]:
            return False
        return True
    elif ope=="-":
        try:
            formula=input_text.get()[-1]
        except:
            formula=""
        if formula=="-":
            return False
        return True
    elif ope=="x!":
        fact()
        return False
    elif ope=="1/x":
        return False
    return True


def calc():
    formula=input_text.get()
    input_text.delete(0,tk.END)
    try:
        formula=formula.replace("×","*")
        formula=formula.replace("÷","/")
        ans=eval(formula)
        input_text.insert(tk.END,str(ans))
    except:
        input_text.insert(tk.END,"エラー")

def fact():
    formula=input_text.get()
    for ope in ["+","-","×","÷"]:
        formula=formula.replace(ope,",")
    formula_lst=formula.split(",")
    ans=math.factorial(float(formula_lst[-1]))
    del_num()
    input_text.insert(tk.END,str(ans))

def del_num():
    formula=input_text.get()
    for i,num in enumerate(reversed(formula)):
        if num in ["+","-","×","÷"]:
            input_text.delete(0,tk.END)
            input_text.insert(tk.END,formula[:-(i)])
            return True
    input_text.delete(0,tk.END)

def chenge_bg(event):
    event.widget["bg"]="#87CEEB"
def back_bg(event):
    event.widget["bg"]="SystemButtonFace"



root=tk.Tk()
root.title("calculate")

input_text=tk.Entry(width=12,font=("",40),justify=tk.RIGHT)
input_text.grid(row=0,column=0,columnspan=4)

button_labels=[["+","-","×","÷","="],["1/x","C","BS"],["x!","0","."]]
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