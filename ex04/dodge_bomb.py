import pygame as pg
import sys
import time

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))

    clock = pg.time.Clock()
    clock.tick(1000)

    bg_sfc = pg.image.load("./fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()
    bg_rct.center = 800, 450
    scrn_sfc.blit(bg_sfc, bg_rct)

    tori_sfc = pg.image.load("./fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    scrn_sfc.blit(tori_sfc, tori_rct)

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()