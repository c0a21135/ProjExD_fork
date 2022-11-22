from random import randint

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
    ua=input()
    if ua in na:
        print("正解！！！")
    else:
        print("出直してこい")
if __name__=="__main__":
    nq,na=shutudai()
    kaitou(nq,na)
