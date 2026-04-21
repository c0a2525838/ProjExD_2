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
    """
    ゲームオーバー画面を表示する関数。

    Parameters
    ----------
    screen : pygame.Surface
        メイン画面の Surface。ここにゲームオーバー画面を描画する。

    Notes
    -----
    - 画面全体を黒い半透明の幕で覆う。
    - 「Game Over」の文字と泣いているこうかとん画像を左右に表示する。
    - 表示後、5秒間停止してから関数を終了する。
    """
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
    """
    Rect が画面内に収まっているかを判定する関数。

    Parameters
    ----------
    rct : pygame.Rect
        判定対象の Rect。

    Returns
    -------
    tuple[bool, bool]
        (横方向が画面内か, 縦方向が画面内か)
        True なら画面内、False なら画面外。
    """
    yoko = True
    tate = True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko, tate


def init_kk_images():
    """
    こうかとんの向きに応じた辞書として返す関数。

    Returns
    -------
    dict[tuple[int, int], pygame.Surface]
        移動方向 (dx, dy) をキー、対応する向きの画像を値とする辞書。
    """
    kk_left = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_right = pg.transform.flip(kk_left, True, False)
    kk_imgs = {}

    directions = [(0, 0), (0, -5), (0, 5), (-5, 0), (5, 0),
                  (-5, -5), (5, -5), (-5, 5), (5, 5)]

    for dx, dy in directions:
        if dx > 0:
            base, ref = kk_right, pg.math.Vector2(1, 0)
        else:
            base, ref = kk_left, pg.math.Vector2(-1, 0)

        if dx == 0 and dy == 0:
            angle = 0
        else:
            angle = ref.angle_to(pg.math.Vector2(dx, dy))

        kk_imgs[(dx, dy)] = pg.transform.rotozoom(base, -angle, 1.0)

    return kk_imgs


<<<<<<< HEAD
=======
#  爆弾の拡大と加速度
>>>>>>> ed7c62b9f731de9bdce2abdd0194ea5cb7917b58
def init_bomb_images():
    """
    爆弾のサイズ変化に対応した画像と加速度を生成する関数。

    Returns
    -------
    tuple[list[pygame.Surface], list[int]]
        - 爆弾画像（半径が徐々に大きくなる 10 種類）
        - 加速度値（1〜10 の整数）
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs


def chase_vector(org_rct: pg.Rect, dst_rct: pg.Rect, current_xy: tuple[float, float]):
    """
    追従型爆弾がこうかとんへ向かうための速度を計算する関数。

    Parameters
    ----------
    org_rct : pygame.Rect
        爆弾の現在位置。
    dst_rct : pygame.Rect
        こうかとんの位置。
    current_xy : tuple[float, float]
        現在の爆弾の速度。

    Returns
    -------
    tuple[float, float]
        新しい速度ベクトル（vx, vy）。
        プレイヤーが近すぎる場合は慣性を維持する。
    """
    dx = dst_rct.centerx - org_rct.centerx
    dy = dst_rct.centery - org_rct.centery

    dist = (dx**2 + dy**2) ** 0.5

    # 近すぎる場合は慣性を維持
    if dist < 300:
        return current_xy

    # ベクトルを √50 の大きさに正規化
    if dist != 0:
        scale = (50 ** 0.5) / dist
        vx = dx * scale
        vy = dy * scale
    else:
        vx, vy = 0, 0

    return (vx, vy)


def main():
    """
    「逃げろ！こうかとん」のメイン。
    -----
    - 背景、プレイヤー、爆弾を初期化する。
    - プレイヤーの移動、爆弾の追従、衝突判定を行う。
    - 爆弾は時間経過で大きくなり、加速度も増加する。
    - プレイヤーが爆弾に当たるとゲームオーバー画面を表示して終了する。
    """
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

<<<<<<< HEAD
    # プレイヤー画像
=======
    # こうかとん辞書
>>>>>>> ed7c62b9f731de9bdce2abdd0194ea5cb7917b58
    kk_imgs = init_kk_images()
    kk_rct = kk_imgs[(0, 0)].get_rect()
    kk_rct.center = 300, 200

    # 爆弾画像と加速度
    bb_imgs, bb_accs = init_bomb_images()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    # 爆弾の初期速度
    bomb_vx, bomb_vy = 5, 5

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

        # プレイヤーの向き画像
        mv = (sum_mv[0], sum_mv[1])
        kk_img = kk_imgs.get(mv, kk_imgs[(0, 0)])
        screen.blit(kk_img, kk_rct)

        # 爆弾の段階（0〜9）
        idx = min(tmr // 500, 9)

        # 爆弾のサイズ更新
        bb_img = bb_imgs[idx]
        center = bb_rct.center
        bb_rct = bb_img.get_rect(center=center)

        bomb_vx, bomb_vy = chase_vector(bb_rct, kk_rct, (bomb_vx, bomb_vy))

        avx = bomb_vx * bb_accs[idx]
        avy = bomb_vy * bb_accs[idx]

        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            bomb_vx *= -1
        if not tate:
            bomb_vy *= -1

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
