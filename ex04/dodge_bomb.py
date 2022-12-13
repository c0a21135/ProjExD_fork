import pygame as pg
import sys
import random

def main():
    WIDTH=1600
    HEIGHT=900
    vx, vy=1, 1

    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((WIDTH, HEIGHT))

    clock = pg.time.Clock()
    clock.tick(10)

    bg_sfc = pg.image.load("./fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()
    scrn_sfc.blit(bg_sfc, bg_rct)

    tori_sfc = pg.image.load("./fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    scrn_sfc.blit(tori_sfc, tori_rct)

    bomb_sfc_lst=[0,0,0]
    for i in range(len(bomb_sfc_lst)):
        draw_sfc = pg.Surface((20, 20))
        draw_sfc.set_colorkey((0,0,0))
        pg.draw.circle(draw_sfc,(255,0,0),(10, 10),10)
        bomb_rct = draw_sfc.get_rect()
        bomb_rct.center= random.randint(10,WIDTH-10), random.randint(10,HEIGHT-10)
        bomb_sfc_lst[i] = [draw_sfc,bomb_rct,[vx,vy]]
    print(bomb_sfc_lst)
    for bomb_sfc in bomb_sfc_lst:
        scrn_sfc.blit(bomb_sfc[0], bomb_sfc[1])

    while True:
        pg.display.update()
        pg.event.pump()
        pressed = pg.key.get_pressed()
        scrn_sfc.blit(bg_sfc, bg_rct)
        scrn_sfc.blit(tori_sfc, tori_rct)
        for bomb_sfc in bomb_sfc_lst:
            if 0>bomb_sfc[1].x+bomb_sfc[2][0] or bomb_sfc[1].x+bomb_sfc[2][0]>WIDTH:
                print(bomb_sfc[1].x,bomb_sfc[2][0])
                bomb_sfc[2][0]*=-1
            # else:
            #     bomb_sfc[2][0]+=1
            if 0>bomb_sfc[1].y+bomb_sfc[2][1] or bomb_sfc[1].y+bomb_sfc[2][1]>HEIGHT:
                bomb_sfc[2][1]*=-1
            # else:
            #     bomb_sfc[2][1]+=1
            bomb_sfc[1].move_ip(bomb_sfc[2][0], bomb_sfc[2][1])
            scrn_sfc.blit(bomb_sfc[0], bomb_sfc[1])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if pressed[pg.K_UP] and tori_rct.y-1>=0:
                tori_rct.move_ip(0, -1)
            if pressed[pg.K_DOWN] and tori_rct.y+1<=HEIGHT:
                tori_rct.move_ip(0, 1)
            if pressed[pg.K_LEFT] and tori_rct.x-1>=0:
                tori_rct.move_ip(-1, 0)
            if pressed[pg.K_RIGHT] and tori_rct.x+1<=WIDTH:
                tori_rct.move_ip(1, 0)
        for bomb_fanc in bomb_sfc_lst:
            if tori_rct.colliderect(bomb_fanc[1]):
                return
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()