from random import randint
from datetime import datetime

def main():
    nq,na=shutudai()
    kaitou(nq,na)

def shutudai():
    questions=[("サザエの旦那の名前は？",("マスオ","ますお")),
    ("カツオの妹の名前は？",("ワカメ","わかめ")),
    ("タラオはカツオから見てどんな関係？",("甥","おい","甥っ子","おいっこ"))]
    qnum=randint(0,len(questions)-1)
    return questions[qnum]

def kaitou(nq,na):
    print(nq)
    st=datetime.now()
    ua=input()
    en=datetime.now()
    if ua in na:
        print("正解！！！")
    else:
        print("出直してこい")
    print(f"所要時間:{en-st}")
if __name__=="__main__":
    nq,na=shutudai()
    kaitou(nq,na)
