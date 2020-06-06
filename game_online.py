# -*- coding: utf-8 -*-
import pygame as pg
import socket
import random
# import sys
# import random
# C:\PR\game_online.py


def sock_setup(other_ip):
    """
    Creates a connection from two different users
    :param other_ip:
    :return my_sock:
    """
    if input('client - c / server - s\n') == 'c':
        print(other_ip)
        # server_ip = other_ip
        # server_ip = '172.20.5.33'
        # server_ip = '127.0.0.1'
        # server_ip = '172.20.5.13'
        server_ip = '192.168.1.34'
        my_sock = socket.socket()
        my_sock.connect((server_ip, 8820))
        return [my_sock, 2, 3, 4, 5, False]
    else:
        ser_sock = socket.socket()
        ser_sock.bind((socket.gethostbyname(socket.gethostname()), 8820))
        ser_sock.listen(10)
        (my_sock, client_address) = ser_sock.accept()

        # [the socket that is connected to the other player, your ship, his ship, your shot, his shot, if host]
        return [my_sock, 3, 2, 5, 4, True]


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
    sc_ta = 0
    try:
        pass
    except IndexError:
        print(boom, scr)
    for enemy in enemies:
        en_hi_bx = pg.Rect(enemy[1], enemy[2], enemy[3], enemy[4])
        for shot in shots:
            if enemy[0] > 0:
                sh_ht_bx = pg.Rect(int(shot[1]), int(shot[2]), 8, 50)
                if en_hi_bx.colliderect(sh_ht_bx) == 1:
                    # scr.blit(boom, (enemy[1] - 20, enemy[2] - 20))
                    shots.remove(shot)
                    # pg.mixer.music.load(r'C:\PR\sound\explosion.mp3')
                    # pg.mixer.music.play(0)
                    enemy[0] -= int(dmg)
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


def return_of_the_chicken(info):
    """
    main game function
    """
    # ==============================================================================================================
    # Game setup
    # ==============================================================================================================
    pg.init()
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))
    pg.display.set_caption('Return Of The Chickens')
    pg.display.set_icon(pg.image.load(r'C:\PR\img\SP_tr.png'))
    pg.mouse.set_visible(1)

    sock, my_ship, allay_ship, my_ls, allay_ls, master = info

    # Images
    sp_tr = pg.image.load(r'C:\PR\img\SP_{}.png'.format(my_ship))
    sp_allay = pg.image.load(r'C:\PR\img\SP_{}.png'.format(allay_ship))
    b_g = pg.image.load(r'C:\PR\img\bg_2.jpg')
    boom = pg.image.load(r'C:\PR\img\boom.png')
    ls_my = pg.image.load(r'C:\PR\img\laser_{}.png'.format(my_ls))
    ls_allay = pg.image.load(r'C:\PR\img\laser_{}.png'.format(allay_ls))

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
    # Main Game function
    # ==============================================================================================================

    while run:
        clock.tick(60)
        if not game_on():
            sock.send(b'exit')
            sock.recv(1024)
            break

        # get the position
        pos = get_pos()

        # Shots
        if pg.mouse.get_pressed()[0] == 1:
            overheat += 1
            if shot_delay == 0 and overheat in range(0, 600):
                c_s = int(600 / shot_sp) + 1
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
        for enemy in enemies:
            vec = (enemy[5][0] - enemy[1], enemy[5][1] - enemy[2])
            if master and vec == (0, 0):
                enemy[5] = random.randint(10, 750), random.randint(5, 400)
            else:
                try:
                    ratio = min(abs(round(enemy[6] / ((vec[0] ** 2 + vec[1] ** 2) ** 0.5), 3)), 1)
                    vec = (enemy[1] + round(vec[0] * ratio), enemy[2] + round(vec[1] * ratio))
                except ZeroDivisionError:
                    vec = (enemy[1], enemy[2])
                enemy[1], enemy[2] = vec

        # Build the game grid
        scr.fill((0, 0, 0))
        scr.blit(b_g, (0, 0))

        # builds your shots
        for i in shots:
            scr.blit(ls_my, (i[1], i[2]))

        # organize the data
        # =============================================================================================================
        # =============================================================================================================

        # my shots data organizer
        shot_send = ''.join(['{0} {1} {2},'.format(dmg, sh[1], sh[2]) for sh in shots])[:-1]
        if shot_send == '':
            shot_send = 'empty'
        else:
            shot_send = shot_send

        # my position data organizer
        pos_send = '{0} {1}'.format(pos[0], pos[1])

        # enemy headings organizer
        if master and len(enemies) > 0:
            enemy_heading = ''.join(['{0} {1},'.format(eh[5][0], eh[5][1]) for eh in enemies])
            enemy_heading = enemy_heading[:-1]
        else:
            enemy_heading = 'empty'

        # final preparation for transmission
        data = '{0}:{1}:{2}:{3}'.format(pos_send, shot_send, score, enemy_heading)

        # sends and receives transmission
        sock.send(data.encode())
        data = sock.recv(1024).decode()

        # handles the received data
        if data == 'exit':
            break
        data = data.split(':')
        # print(data)
        pos_send = data[0]
        shot_send = data[1]
        allay_score = data[2]

        # sets the correct headings for the enemies
        if data[3] != 'empty' and len(enemies) > 0:
            enemy_heading = [(int(eh.split()[0]), int(eh.split()[1])) for eh in data[3].split(',')]
            for i in range(len(enemies)):
                try:
                    enemies[i][5] = enemy_heading[i]
                except IndexError:
                    pass

        # handles and print the other players shots
        if shot_send != 'empty':
            shot_send = shot_send.split(',')
            shot_send = [i.split() for i in shot_send]
            for shot in shot_send:
                scr.blit(ls_allay, (int(shot[1]), int(shot[2])))

        # =============================================================================================================
        # =============================================================================================================

        # checks if the player has been hit by an enemy or an enemy's shot
        for i in enemy_shots:
            if pg.Rect(pos[0], pos[1], 50, 40).colliderect(pg.Rect(i[1], i[2], 30, 40)):
                hp -= 50
                enemy_shots.remove(i)

        for i in enemies:
            if pg.Rect(pos[0], pos[1], 50, 40).colliderect(pg.Rect(i[1], i[2], i[3], i[4])):
                hp -= 2

        # Sets up a new levle
        if len(enemies) == 0:
            enemies = [dup_en(en_blue), dup_en(en_blue), dup_en(en_blue), dup_en(en_blue)]
            lv += 1
            hp = max_hp
            shot_amount -= 1
            dmg += 5
            shot_sp += 2

        # game hud draws

        # print my score
        score += en_hit(shots, enemies, boom, scr, dmg)
        if shot_send != 'empty':
            en_hit(shot_send, enemies, boom, scr, shot_send[0][0])
        print_txt(scr, score, 10, 150, 16)
        print_txt(scr, allay_score, 10, 170, 16)

        # checks if an enemy has been defeated

        for i in enemies:
            if i[0] > 0:
                scr.blit(i[8], (i[1], i[2]))
            else:
                enemies.remove(i)

        # overheat indicator
        for i in range(abs(int(overheat / 60))):
            pg.draw.line(scr, (230, 200, 200), (5 + i * 12, max(0, 12 - i * 3)), (5 + i * 12, 20), 5)

        # levels of equipment and next upgrade cost
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(310, 0, 180, 40), 4)
        print_txt(scr, 'SP      rpm      AM      dmg', 320, 5, 13)
        print_txt(scr, str(int((shot_sp - 8) / 2)), 327, 25, 13)
        print_txt(scr, str(21 - shot_amount), 370, 25, 13)
        print_txt(scr, str(sh_lv), 418, 25, 13)
        print_txt(scr, str(int((dmg - 5) / 5)), 463, 25, 13)

        # HP bar
        pg.draw.line(scr, (150, 150, 150), (40, 576), (300, 576), 12)
        if hp > 0:
            pg.draw.line(scr, (100, 250, 100), (44, 576), (44 + int(252 * hp / max_hp), 576), 8)
        pg.draw.line(scr, (150, 250, 150), (7, 576), (33, 576), 8)
        pg.draw.line(scr, (150, 250, 150), (20, 563), (20, 589), 8)

        # the current level the player is on
        pg.draw.line(scr, (120, 120, 120), (740, 15), (800, 15), 30)
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(740, 0, 60, 30), 5)
        print_txt(scr, 'LV. {}'.format(lv), 745, 10, 13)

        # builds your and the other players ship
        scr.blit(sp_tr, pos)
        pos_send = pos_send.split()
        pos_send = (int(pos_send[0]), int(pos_send[1]))
        scr.blit(sp_allay, pos_send)

        pg.display.update()

    pg.quit()


def main():
    """
    Add Documentation here
    """
    return_of_the_chicken(sock_setup('172.20.0.30'))


if __name__ == '__main__':
    main()
