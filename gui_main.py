import pygame as pg
import socket
import select
import random
server_ip = socket.gethostbyname(socket.gethostname())


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
    font = pg.font.Font(None, round(size*1.5))
    text = font.render(str(txt), True, white)
    scr.blit(text, (x, y))


def pop_up(scr, txt, pop_type):
    # draws the black square
    pg.draw.line(scr, (90, 90, 90), (200, 190), (600, 190), 200)
    # draws one side of the X
    pg.draw.line(scr, (200, 30, 30), (575, 115), (590, 100), 2)
    # draws one side of the X
    pg.draw.line(scr, (200, 30, 30), (575, 100), (590, 115), 2)
    # surrounds
    pg.draw.rect(scr, (255, 255, 255), pg.Rect(200, 90, 400, 200), 4)
    # accept
    pg.draw.rect(scr, (255, 255, 255), pg.Rect(290, 250, 90, 26), 4)
    # decline
    pg.draw.rect(scr, (255, 255, 255), pg.Rect(420, 250, 90, 26), 4)
    print_txt(scr, 'Accept', 304, 253, 18)
    print_txt(scr, 'Decline', 430, 254, 18)
    print_txt(scr, txt, 240, 130, 35)
    if pop_type == 'match':
        print_txt(scr, 'Invited you to a  match.', 240, 170, 24)
    elif pop_type == 'friend':
        print_txt(scr, 'Sent a friend request.', 240, 170, 24)


def ser_comm(sock):
    data = 'none'
    rlist, wlist, xlist = select.select([sock], [sock], [])
    for current_socket in rlist:
        if current_socket is sock:
            data = sock.recv(1024).decode()
    return data


def stage_2_custom():
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))

    # variables
    done = False
    active_sp = 1
    active_sh = 1
    bg = pg.image.load(r'C:\PR\img\bg_7.jpg')
    dice = pg.image.load(r'C:\PR\img\dice.png')
    sp_all = [pg.image.load(r'C:\PR\img\sp_{0}.png'.format(i)) for i in range(1, 8)]
    sh_all = [pg.image.load(r'C:\PR\img\laser_{0}.png'.format(i)) for i in ['b', 'g', 'o', 'r', 'y', 'f', 'ro']]

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.Rect(0, 0, 80, 40).collidepoint(event.pos[0], event.pos[1]):
                    done = True
                x, y = (20, 100)
                for sp in sp_all:
                    if pg.Rect(x, y, 78, 78).collidepoint(event.pos[0], event.pos[1]):
                        active_sp = (x + 78) / 98
                    x += 98
                if pg.Rect(x, y, 78, 78).collidepoint(event.pos[0], event.pos[1]):
                    active_sp = random.randint(1, 7)

                x, y = (20, 300)
                for sh in sh_all:
                    if pg.Rect(x, y, 78, 78).collidepoint(event.pos[0], event.pos[1]):
                        active_sh = (x + 78) / 98
                    x += 98
                if pg.Rect(x, y, 78, 78).collidepoint(event.pos[0], event.pos[1]):
                    active_sh = random.randint(1, 7)

        scr.fill((0, 0, 0))
        scr.blit(bg, (0, 0))
        # builds all of the different spaceships you can choose from
        x, y = (20, 100)
        for sp in sp_all:
            pg.draw.line(scr, (120, 120, 120), (x, y + 39), (x + 78, y + 39), 78)
            pg.draw.rect(scr, (110, 90, 255) if active_sp == (x + 78)/98 else (255, 255, 255), pg.Rect(x, y, 78, 78), 4)
            scr.blit(sp, (x + 15, y + 13))
            x += 98
        pg.draw.line(scr, (255, 255, 255), (x, y + 39), (x + 78, y + 39), 78)
        pg.draw.rect(scr, (150, 150, 255), pg.Rect(x, y, 78, 78), 4)
        scr.blit(dice, (x + 13, y + 13))

        # builds all of the different shots you can choose from
        x, y = (20, 300)
        for sh in sh_all:
            pg.draw.line(scr, (120, 120, 120), (x, y + 39), (x + 78, y + 39), 78)
            pg.draw.rect(scr, (110, 90, 255) if active_sh == (x + 78)/98 else (255, 255, 255), pg.Rect(x, y, 78, 78), 4)
            scr.blit(sh, (x + 36, y + 13))
            x += 98
        pg.draw.line(scr, (255, 255, 255), (x, y + 39), (x + 78, y + 39), 78)
        pg.draw.rect(scr, (150, 150, 255), pg.Rect(x, y, 78, 78), 4)
        scr.blit(dice, (x + 13, y + 13))

        # prints a return sign
        pg.draw.line(scr, (120, 120, 120), (0, 20), (80, 20), 40)
        pg.draw.rect(scr, (0, 0, 0), pg.Rect(0, 0, 80, 40), 5)
        print_txt(scr, 'Return', 7, 12, 20)
        pg.display.flip()
        clock.tick(60)


def stage_2_main():
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))

    # variables
    done = False
    bg = pg.image.load(r'C:\PR\img\bg_5.jpg')
    refresh = pg.image.load(r'C:\PR\img\refresh.png')
    rect_custom = pg.Rect(530, 55, 250, 100)
    rect_game = pg.Rect(530, 185, 250, 100)
    rect_friends = pg.Rect(530, 315, 250, 100)
    rect_rules = pg.Rect(530, 445, 250, 100)
    friends_lobby = ['moshe_1', 'moshe_2']
    friends_mid_game = ['moshe_3', 'moshe_4']
    popup_active = False

    # main while loop
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.MOUSEBUTTONDOWN:
                if popup_active:
                    if pg.Rect(290, 250, 90, 26).collidepoint(event.pos[0], event.pos[1]):
                        print('accept')
                        # popup_active = False

                    if pg.Rect(420, 250, 90, 26).collidepoint(event.pos[0], event.pos[1]):
                        print('decline')
                        # popup_active = False

                    if pg.Rect(573, 98, 19, 19).collidepoint(event.pos[0], event.pos[1]):
                        print('exit popup')
                        # popup_active = False

                elif rect_custom.collidepoint(event.pos[0], event.pos[1]):
                    stage_2_custom()

                elif rect_game.collidepoint(event.pos[0], event.pos[1]):
                    print('game')

                elif rect_friends.collidepoint(event.pos[0], event.pos[1]):
                    print('friends')

                elif rect_rules.collidepoint(event.pos[0], event.pos[1]):
                    print('rules')

                elif pg.Rect(195, 52, 29, 29).collidepoint(event.pos[0], event.pos[1]):
                    print('refresh')

        scr.fill((0, 0, 0))
        scr.blit(bg, (0, 0))
        scr.blit(refresh, (197, 54))
        print_txt(scr, 'Customization', rect_custom.x + 17, rect_custom.y + 35, 30)
        print_txt(scr, 'To Game Lobby', rect_game.x + 10, rect_game.y + 35, 30)
        print_txt(scr, 'Friends', rect_friends.x + 70, rect_friends.y + 35, 30)
        print_txt(scr, 'Rules and', rect_rules.x + 50, rect_rules.y + 15, 30)
        print_txt(scr, 'Instructions', rect_rules.x + 35, rect_rules.y + 55, 30)
        print_txt(scr, 'Active Friends', 38, 58, 20)
        pg.draw.rect(scr, (200, 200, 200), rect_custom, 4)
        pg.draw.rect(scr, (200, 200, 200), rect_friends, 4)
        pg.draw.rect(scr, (200, 200, 200), rect_rules, 4)
        pg.draw.rect(scr, (200, 200, 200), rect_game, 4)
        pg.draw.rect(scr, (200, 200, 200), (30, 50, 200, 500), 4)
        pg.draw.line(scr, (200, 200, 200), (30, 85), (230, 85), 4)

        base_height = 111

        print_txt(scr, 'Friends In Lobby:', 39, 87, 18)
        pg.draw.line(scr, (200, 200, 200), (30, 107), (230, 107), 4)
        for friend in friends_lobby:
            if base_height <= 524:
                print_txt(scr, friend, 39, base_height, 18)
                pg.draw.line(scr, (200, 200, 200), (30, base_height + 22), (230, base_height + 22), 4)
                base_height += 26

        print_txt(scr, 'Friends In Game:', 39, base_height, 18)
        pg.draw.line(scr, (200, 200, 200), (30, base_height + 22), (230, base_height + 22), 4)
        base_height += 26
        for friend in friends_mid_game:
            if base_height <= 524:
                print_txt(scr, friend, 39, base_height, 18)
                pg.draw.line(scr, (200, 200, 200), (30, base_height + 22), (230, base_height + 22), 4)
                base_height += 26

        if popup_active:
            pop_up(scr, '', 'friend')

        pg.display.flip()
        clock.tick(30)


def main():
    # sock = socket.socket()
    # sock.connect((server_ip, 8820))
    # print(sock.recv(1024))
    stage_2_main()
    stage_2_custom()

if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
