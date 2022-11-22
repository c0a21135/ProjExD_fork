from random import randint
from datetime import datetime
def mkstr(anum,lnum):
    astr=""
    lstr=""
    for i in range(anum):
        astr+=chr(randint(65,90))
    nstr=astr
    for i in range(lnum):
        idx=randint(0,len(nstr)-1)
        lstr+=nstr[idx]
        nstr=nstr[:idx]+nstr[idx+1:]
    return astr,lstr,nstr

def questions(astr,lstr,nstr):
    print("対象文字:\n"+astr)
    print("欠損文字:\n"+lstr)
    print("表示文字:\n"+nstr)
    u_lnum=input("欠損文字はいくつあるでしょうか:")
    if str(lnum)!=u_lnum:
        return "不正解です。またチャレンジしてください。",False
    for i in range(lnum):
        u_lstr=input(f"{i+1}つ目の文字を入力してください")
        if u_lstr not in lstr or u_lstr==""or len(u_lstr)>1:
            return "不正解です。またチャレンジしてください。",False
        lstr=lstr.replace(u_lstr,"",1)
    return "正解です。",True

    


if __name__=="__main__":
    st=datetime.now()
    anum,lnum=randint(6,10),randint(1,5)
    flag=False
    while flag==False:
        astr,lstr,nstr=mkstr(anum,lnum)
        message,result=questions(astr,lstr,nstr)
        print(message)
        flag=result
    en=datetime.now()
    print(f"実行時間：{en-st}")