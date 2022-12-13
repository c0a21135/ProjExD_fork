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
    clock.tick(1000)

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
        bomb_sfc_lst[i] = [draw_sfc,
                           [random.randint(10,WIDTH-10),random.randint(50,HEIGHT-50)]]
    print(bomb_sfc_lst)
    for bomb_sfc in bomb_sfc_lst:
        scrn_sfc.blit(bomb_sfc[0], tuple(bomb_sfc[1]))

    while True:
        pg.display.update()
        pg.event.pump()
        pressed = pg.key.get_pressed()
        scrn_sfc.blit(bg_sfc, bg_rct)
        scrn_sfc.blit(tori_sfc, tori_rct)
        for bomb_sfc in bomb_sfc_lst:
            bomb_sfc[1]=[bomb_sfc[1][0]+vx, bomb_sfc[1][1]+vy]    
            scrn_sfc.blit(bomb_sfc[0], tuple(bomb_sfc[1]))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if pressed[pg.K_UP]:
                tori_rct.move_ip(0, -1)
            if pressed[pg.K_DOWN]:
                tori_rct.move_ip(0, 1)
            if pressed[pg.K_LEFT]:
                tori_rct.move_ip(-1, 0)
            if pressed[pg.K_RIGHT]:
                tori_rct.move_ip(1, 0)
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()