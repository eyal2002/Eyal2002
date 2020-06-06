# -*- coding: utf-8 -*-
import pygame as pg
# import sys
import random

global en_blue, en_red, en_vader, en_army, en_super, en_big


def game_on():
    """
    Checks if the player closed the game.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True


def print_txt(scr, txt, x, y, size):
    """
    Prints your score to the screen
    :param scr - enables the function to print to the game screen
    :param txt - the players score to build
    :param x - points to where is the text x poisson is
    :param y - points to where is the text y poisson is
    :param size - the size of the font
    :return:
    """
    white = (255, 255, 255)
    pg.display.set_caption('Show Text')
    font = pg.font.Font('freesansbold.ttf', size)
    text = font.render(str(txt), True, white)
    scr.blit(text, (x, y))


def en_hit(shots, enemies, boom, scr, dmg):
    """
    Checks if any shots hit an enemy
    """
    # print(boom)
    # print(scr)
    sc_ta = 0
    for enemy in enemies:
        en_hi_bx = pg.Rect(enemy[1], enemy[2], enemy[3], enemy[4])
        for shot in shots:
            if enemy[0] > 0:
                sh_ht_bx = pg.Rect(shot[1], shot[2], 8, 50)
                if en_hi_bx.colliderect(sh_ht_bx) == 1:
                    # scr.blit(boom, (enemy[1] - 20, enemy[2] - 20))
                    shots.remove(shot)
                    # pygame.mixer.music.load(r'C:\PR\sound\explosion.mp3')
                    # pygame.mixer.music.play(0)
                    enemy[0] -= dmg
                    sc_ta += 1
    return sc_ta


def dup_en(en):
    """
    creates a duplicate of a type of an enemy.
    """
    to_ret = [en[0], random.randint(10, 750), -20, en[3], en[4], (0, 50), en[6], en[7], en[8]]
    to_ret[5] = to_ret[1], 60
    return to_ret


def get_pos():
    """
    Returns the position of the mouse courser.
    """
    pos = pg.mouse.get_pos()
    return pos[0] - 25, pos[1] - 13


def new_level_enemy(lv):
    """
    this function sets the enemy for the current level
    """
    en_list = []


def return_of_the_chicken():
    """
    main game function
    """
    # Game setup
    pg.init()
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))
    pg.display.set_caption('Game_2')
    pg.display.set_icon(pg.image.load(r'C:\PR\img\SP_tr.png'))
    pg.mouse.set_visible(1)

    # Images
    # sp_tr = pg.image.load(r'C:\PR\img\SP_1.png')
    sp_tr = pg.image.load(r'C:\PR\img\SP_7.png')
    b_g = pg.image.load(r'C:\PR\img\bg_2.jpg')
    boom = pg.image.load(r'C:\PR\img\boom.png')
    ls_g = pg.image.load(r'C:\PR\img\laser_g.png')
    ls_r = pg.image.load(r'C:\PR\img\laser_r.png')
    ls_b = pg.image.load(r'C:\PR\img\laser_b.png')
    ls_o = pg.image.load(r'C:\PR\img\laser_o.png')
    ls = [ls_g, ls_r, ls_b, ls_o]
    ls_tp = pg.image.load(r'C:\PR\img\laser_ro.png')

    pg.mouse.set_visible(False)

    # Variables
    run = True
    c_s = 0
    shot_delay = 0
    shots = []  # [how long dose the shot have left, x, y]
    enemy_shots = []  # [how long dose the shot have left, x, y]
    shot_amount = 20  # define how many frames need to pass between shots
    shot_sp = 10  # define how many pixel each shoot passes each frame
    dmg = 10  # define how much damage is dalt to each enemy
    max_hp = 300  # define the max amount of health the user have
    hp = max_hp
    sh_lv = 1  # define how many shots can be fired at each time
    score = 0
    lv = 1
    overheat = 0

    # enemies [0-hp points, 1-x,2-y, 3-length, 4-height, 5-(x, y) heading, 6-speed, 7-shot chance,8-png scr]
    en_blue = [30, 350, 160, 90, 75, (0, 0), 4, 5, pg.image.load(r'C:\PR\img\chick_blue.png')]
    en_red = [60, 350, 160, 90, 75, (0, 0), 4, 5, pg.image.load(r'C:\PR\img\chick_red.png')]
    en_vader = [4000, 350, 160, 115, 105, (0, 0), 4, 20, pg.image.load(r'C:\PR\img\chick_vader.png')]
    en_army = [1000, 350, 160, 130, 130, (0, 0), 4, 10, pg.image.load(r'C:\PR\img\chick_army.png')]
    en_super = [1000, 350, 160, 130, 125, (0, 0), 4, 70, pg.image.load(r'C:\PR\img\chick_super.png')]
    en_big = [1000, 350, 160, 105, 100, (0, 0), 4, 15, pg.image.load(r'C:\PR\img\chick_big.png')]


    # shots of an enemy
    esh_egg = pg.image.load(r'C:\PR\img\egg.png')
    # enemies = [dup_en(en_blue), dup_en(en_red), dup_en(en_army), dup_en(en_big), dup_en(en_vader), dup_en(en_super)]
    enemies = [dup_en(en_blue), dup_en(en_red)]

    # ==============================================================================================================
    # ==============================================================================================================

    # Main Game function
    while run:
        clock.tick(60)
        run = game_on()

        # get the position
        pos = get_pos()

        # Shots
        if pg.mouse.get_pressed()[0] == 1:
            overheat += 1
            if shot_delay == 0 and overheat in range(0, 600):
                c_s = int(600/shot_sp) + 1
                shot_delay = shot_amount
                if sh_lv == 1:
                    shots.append([c_s, pos[0] + 21, pos[1]])
                elif sh_lv == 2:
                    shots.append([c_s, pos[0] + 13, pos[1]])
                    shots.append([c_s, pos[0] + 29, pos[1]])
                else:
                    shots.append([c_s, pos[0] + 21, pos[1]])
                    shots.append([c_s, pos[0] + 39, pos[1]])
                    shots.append([c_s, pos[0] + 3, pos[1]])
                # pygame.mixer.music.load(r'C:\PR\sound\ls_sound.mp3')
                # pygame.mixer.music.play(0)
            if overheat == 600:
                overheat = -600
            if overheat < 0:
                overheat += 1
        else:
            if overheat in range(0, 600):
                overheat -= 4
            else:
                overheat += 3

        if c_s > 0:
            for shot in shots:
                shot[0] -= 1
                shot[2] -= shot_sp
            c_s -= 1

        if shot_delay > 0:
            shot_delay -= 1

        # remove all the shots that ended their time and or space
        to_remove = []
        try:
            for shot in shots:
                if shot[0] <= 0 or shot[2] < -30:
                    to_remove.append(shot)
                else:
                    break
            for rem in to_remove:
                shots.remove(rem)
        except IndexError:
            shots = []

        # remove all the enemy shots that ended their time and or space
        to_remove = []
        try:
            for shot in enemy_shots:
                if shot[2] > 600:
                    to_remove.append(shot)
                else:
                    break
            for rem in to_remove:
                enemy_shots.remove(rem)
        except IndexError:
            shots = []

        # enemies movement
        for i in enemies:
            vec = (i[5][0] - i[1], i[5][1] - i[2])
            if vec == (0, 0):
                i[5] = random.randint(10, 750), random.randint(5, 400)
            else:
                try:
                    ratio = min(abs(round(i[6]/((vec[0]**2 + vec[1]**2)**0.5), 3)), 1)
                    vec = (i[1] + round(vec[0]*ratio), i[2] + round(vec[1]*ratio))
                except ZeroDivisionError:
                    pass
                i[1], i[2] = vec

        scr.fill((0, 0, 0))
        scr.blit(b_g, (0, 0))

        # Build the game grid

        for i in shots:
            scr.blit(ls_tp, (i[1], i[2]))

        for i in enemy_shots:
            scr.blit(i[0], (i[1], i[2]))
            i[2] += 3

        for i in enemies:
            if i[0] > 0:
                scr.blit(i[8], (i[1], i[2]))
                if random.randint(1, 1001) < i[7]:
                    enemy_shots.append([esh_egg, i[1] + 50, i[2] + 100])
            else:
                enemies.remove(i)

        if len(enemies) == 0:
            enemies = [dup_en(en_blue), dup_en(en_blue), dup_en(en_blue), dup_en(en_blue)]
            lv += 1
            hp = max_hp
            shot_amount -= 1
            dmg += 5
            shot_sp += 2

        for i in enemy_shots:
            if pg.Rect(pos[0], pos[1], 50, 40).colliderect(pg.Rect(i[1], i[2], 30, 40)):
                hp -= 50
                enemy_shots.remove(i)

        for i in enemies:
            if pg.Rect(pos[0], pos[1], 50, 40).colliderect(pg.Rect(i[1], i[2], i[3], i[4])):
                hp -= 2

        scr.blit(sp_tr, pos)

        # game hud draws

        # score for
        score += en_hit(shots, enemies, boom, scr, dmg) * dmg
        print_txt(scr, score, 10, 150, 16)

        # overheat indicator
        for i in range(abs(int(overheat/60))):
            pg.draw.line(scr, (230, 200, 200), (5 + i*12, max(0, 12 - i*3)), (5 + i*12, 20), 5)

        # levels of equipment and next upgrade cost
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(310, 0, 180, 40), 4)
        print_txt(scr, 'SP      rpm      AM      dmg', 320, 5, 13)
        print_txt(scr, str(int((shot_sp - 8)/2)), 327, 25, 13)
        print_txt(scr, str(21 - shot_amount), 370, 25, 13)
        print_txt(scr, str(sh_lv), 418, 25, 13)
        print_txt(scr, str(int((dmg - 5)/5)), 463, 25, 13)

        # HP bar
        pg.draw.line(scr, (150, 150, 150), (40, 576), (300, 576), 12)
        if hp > 0:
            pg.draw.line(scr, (100, 250, 100), (44, 576), (44 + int(252*hp/max_hp), 576), 8)
        pg.draw.line(scr, (150, 250, 150), (7, 576), (33, 576), 8)
        pg.draw.line(scr, (150, 250, 150), (20, 563), (20, 589), 8)

        # the current level the player is on
        pg.draw.line(scr, (120, 120, 120), (740, 15), (800, 15), 30)
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(740, 0, 60, 30), 5)
        print_txt(scr, 'LV. {}'.format(lv), 745, 10, 13)

        pg.display.update()

    pg.quit()


def main():
    """
    Add Documentation here
    """

    return_of_the_chicken()


if __name__ == '__main__':
    main()
