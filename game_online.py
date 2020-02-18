# -*- coding: utf-8 -*-
import pygame as pg
import socket
# import sys
# import random
# C:\PY\PR\game_online.py


def sock_setup(other_ip):
    """
    Creates a connection from two different users
    :param other_ip:
    :return my_sock:
    """
    if input('client - c / server - s\n') == 'c':
        print(other_ip)
        # server_ip = other_ip
        # server_ip = '172.20.5.12'
        server_ip = '127.0.0.1'
        my_sock = socket.socket()
        my_sock.connect((server_ip, 8820))
        return my_sock
    else:
        ser_sock = socket.socket()
        # ser_sock.bind(('192.168.1.22', 8820))
        ser_sock.bind(('127.0.0.1', 8820))
        ser_sock.listen(10)
        (my_sock, client_address) = ser_sock.accept()

        return my_sock


def game_on():
    """
    Checks if the player closed the game.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True


def print_txt(scr, txt, x, y):
    """
    Prints your score to the screen
    :param scr - enables the function to print to the game screen
    :param txt - the players score to build
    :param x - points to where is the text x posision is
    :param y - points to where is the text y posision is
    :return:
    """
    white = (255, 255, 255)
    pg.display.set_caption('Show Text')
    font = pg.font.Font('freesansbold.ttf', 16)
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
                sh_ht_bx = pg.Rect(shot[1], shot[2], 8, 50)
                if en_hi_bx.colliderect(sh_ht_bx) == 1:
                    # scr.blit(boom, (enemy[1] - 20, enemy[2] - 20))
                    shots.remove(shot)
                    # pg.mixer.music.load(r'C:\PY\PR\sound\explosion.mp3')
                    # pg.mixer.music.play(0)
                    enemy[0] -= dmg
                    sc_ta += 1
    return sc_ta


def get_pos():
    """
    Returns the position of the mouse courser.
    """
    pos = pg.mouse.get_pos()
    return pos[0] - 25, pos[1] - 13


def return_of_the_chicken(sock):
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
    pg.display.set_icon(pg.image.load(r'C:\PY\PR\img\SP_tr.png'))
    pg.mouse.set_visible(1)

    # Images
    sp_tr = pg.image.load(r'C:\PY\PR\img\SPnn.png')
    b_g = pg.image.load(r'C:\PY\PR\img\bg_2.jpg')
    enemy = pg.image.load(r'C:\PY\PR\img\en_1.png')
    boom = pg.image.load(r'C:\PY\PR\img\boom.png')
    ls_g = pg.image.load(r'C:\PY\PR\img\laser_g.png')
    ls_r = pg.image.load(r'C:\PY\PR\img\laser_r.png')
    ls_b = pg.image.load(r'C:\PY\PR\img\laser_b.png')
    ls_o = pg.image.load(r'C:\PY\PR\img\laser_o.png')
    ls = [ls_g, ls_r, ls_b, ls_o]

    pg.mouse.set_visible(False)

    # Varibles
    run = True
    c_s = 0
    shot_delay = 0
    shot_amount = 8
    shots = []
    dmg = 10
    enemies = [[1000, 350, 160, 44, 32]]
    sh_lv = 11
    score = 0

    # ==============================================================================================================
    # Main Game function
    # ==============================================================================================================

    while run:
        clock.tick(60)
        if not game_on():
            sock.send(b'exit')
            break

        # get the position
        pos = get_pos()

        # Shots
        if pg.mouse.get_pressed()[0] == 1 and shot_delay == 0:
            c_s = 22
            shot_delay = shot_amount
            if sh_lv < 4:
                shots.append([c_s, pos[0] + 21, pos[1]])
                # pg.mixer.music.load(r'C:\PY\PR\sound\ls_sound.mp3')
                # pg.mixer.music.play(0)
            elif sh_lv < 8:
                shots.append([c_s, pos[0] + 13, pos[1]])
                shots.append([c_s, pos[0] + 29, pos[1]])
                # pg.mixer.music.load(r'C:\PY\PR\sound\ls_sound.mp3')
                # pg.mixer.music.play(0)
            else:
                shots.append([c_s, pos[0] + 21, pos[1]])
                shots.append([c_s, pos[0] + 39, pos[1]])
                shots.append([c_s, pos[0] + 3, pos[1]])
                # pg.mixer.music.load(r'C:\PY\PR\sound\ls_sound.mp3')
                # pg.mixer.music.play(0)

        if c_s > 0:
            for shot in shots:
                shot[0] -= 1
                shot[2] -= 30
            c_s -= 1

        if shot_delay > 0:
            shot_delay -= 1

        # print(shots)
        # print(pos)

        to_remove = []
        # print(shots)
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
        # print('=================================')
        # print(shots)

        scr.fill((0, 0, 0))
        scr.blit(b_g, (0, 0))

        # builds your shots
        for i in shots:
            scr.blit(ls[sh_lv % 4], (i[1], i[2]))

        # organize the data

        # my shots data organizer
        shot_send = ''.join(['{0} {1} {2},'.format(sh_lv, sh[1], sh[2]) for sh in shots])[:-1]
        if shot_send == '':
            shot_send = 'empty'

        # my position data organizer
        pos_send = '{0} {1}'.format(pos[0], pos[1])

        # final preparation for transmission
        data = '{0}:{1}'.format(pos_send, shot_send)

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

        # handles and print the other players shots
        if shot_send != 'empty':
            shot_send = shot_send.split(',')
            shot_send = [i.split() for i in shot_send]
            for i in shot_send:
                scr.blit(ls[int(i[0]) % 4], (int(i[1]), int(i[2])))

        for i in enemies:
            if i[0] > 0:
                scr.blit(enemy, (i[1], i[2]))

        # builds your and the other players ship
        scr.blit(sp_tr, pos)
        pos_send = pos_send.split()
        pos_send = (int(pos_send[0]), int(pos_send[1]))
        scr.blit(sp_tr, pos_send)

        score += en_hit(shots, enemies, boom, scr, dmg)
        print_txt(scr, score, 0, 0)
        pg.display.update()

    pg.quit()


def main():
    """
    Add Documentation here
    """
    return_of_the_chicken(sock_setup('172.20.0.30'))


if __name__ == '__main__':
    main()
