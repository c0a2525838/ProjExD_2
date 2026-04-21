import os
import sys
import random
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP:    (0, -5),
    pg.K_DOWN:  (0, +5),
    pg.K_LEFT:  (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def game_over(screen):
    """ゲームオーバー画面を5秒表示する"""

    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.fill((0, 0, 0))
    blackout.set_alpha(200)
    font = pg.font.Font(None, 120)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    offset = 290  

    cry_left_rct = cry_img.get_rect(center=(text_rct.centerx - offset, text_rct.centery))
    cry_right_rct = cry_img.get_rect(center=(text_rct.centerx + offset, text_rct.centery))

    blackout.blit(text, text_rct)
    blackout.blit(cry_img, cry_left_rct)
    blackout.blit(cry_img, cry_right_rct)
    
    screen.blit(blackout, (0, 0))
    pg.display.update()    
    time.sleep(5)


def check_bound(rct: pg.Rect):
    yoko = True
    tate = True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko, tate


def init_bomb_images():
    """爆弾の大きさと加速度のリストを作成"""
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度 1〜10

    for r in range(1, 11):  # 半径1〜10倍
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # 爆弾の画像リストと加速度リスト
    bb_imgs, bb_accs = init_bomb_images()

    # 初期爆弾
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        kk_rct.move_ip(sum_mv)
        
        yoko, tate = check_bound(kk_rct)
        if not yoko:
            kk_rct.move_ip(-sum_mv[0], 0)
        if not tate:
            kk_rct.move_ip(0, -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        
        # 時間に応じて爆弾の段階
        idx = min(tmr // 500, 9)

        # 加速
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        # 拡大
        bb_img = bb_imgs[idx]
        bb_rct.width  = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        # 移動
        bb_rct.move_ip(avx, avy)

        # 反射
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bb_img, bb_rct)
        
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
