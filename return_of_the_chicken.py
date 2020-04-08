import pygame as pg
import socket
import select
import random

# server_ip = socket.gethostbyname(socket.gethostname())
server_ip = '192.168.1.22'

# ============================================================================================================
# main function for all stages
# ============================================================================================================


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


# ============================================================================================================
# first stage - log in or sign up.
# ============================================================================================================
def stage_1(sock):
    """
    :Param sock - the games socket - the one that is with communication with the server
    The first stage of the game lets the player to sign in or sing up.
    Establishes a the connection with the server
    """
    # prints the game intro a few seconds.
    scr = pg.display.set_mode((1064, 600))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    scr.fill((0, 0, 0))
    op_scr = pg.image.load(r'C:\PR\img\icon_5.jpg')
    scr.blit(op_scr, (0, 0))
    pg.display.update()
    clock.tick(0.5)

    # sets the display and variables for the process.
    bg = pg.image.load(r'C:\PR\img\bg_6.jpg')
    scr = pg.display.set_mode((640, 480))
    input_box_name = pg.Rect(100, 100, 240, 32)
    input_box_pass = pg.Rect(140, 230, 240, 32)
    button_login = pg.Rect(165, 349, 83, 40)
    button_signup = pg.Rect(385, 349, 96, 40)
    button_see_pass = pg.Rect(100, 230, 32, 32)
    color_inactive = (240, 240, 255)
    color_active = (170, 170, 255)
    active_name = False
    active_pass = False
    text_name = ''
    text_pass = ''
    con_pass = True
    done = False

    # main function for the first stage.
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box_name.collidepoint(event.pos[0], event.pos[1]):
                    # Toggle the active variable.
                    active_name = not active_name
                    active_pass = False
                elif input_box_pass.collidepoint(event.pos[0], event.pos[1]):
                    # Toggle the active variable.
                    active_pass = not active_pass
                    active_name = False

                # Checks if a button is pressed and if so directs to the correct response
                elif button_login.collidepoint(event.pos[0], event.pos[1]):
                    print(text_name + ' ' + text_pass)
                    # sends said information to the correct function
                    # login(text_name, text_pass, sock)
                    sock.send(b'lo si:' + text_name.encode() + b' ' + text_pass.encode())
                    data = sock.recv(1024).decode()
                    if data == 'success':
                        done = True
                    text_name = ''
                    text_pass = ''

                elif button_signup.collidepoint(event.pos[0], event.pos[1]):
                    print(text_name + ' ' + text_pass)
                    # sends said information to the correct function
                    sock.send(b'lo su:' + text_name.encode() + b' ' + text_pass.encode())
                    data = sock.recv(1024).decode()
                    if data == 'success':
                        done = True
                    text_name = ''
                    text_pass = ''

                elif button_see_pass.collidepoint(event.pos[0], event.pos[1]):
                    con_pass = not con_pass

                else:
                    active_name = False
                    active_pass = False

            #
            if event.type == pg.KEYDOWN:
                if (active_name or active_pass) and event.key == pg.K_TAB:
                    active_name = not active_name
                    active_pass = not active_pass
                elif active_name:
                    if event.key == pg.K_BACKSPACE:
                        text_name = text_name[:-1]
                    elif event.unicode not in [' ', ':', '\n', pg.K_RETURN, chr(13)] and len(text_pass) <= 25:
                        text_name += event.unicode

                elif active_pass:
                    if event.key == pg.K_BACKSPACE:
                        text_pass = text_pass[:-1]
                    elif event.unicode not in [' ', ':', '\n', pg.K_RETURN, chr(13)] and len(text_pass) <= 35:
                        text_pass += event.unicode

        # Change the current color of the input box.
        color_name = color_active if active_name else color_inactive
        color_pass = color_active if active_pass else color_inactive

        scr.fill((0, 0, 0))
        scr.blit(bg, (0, 0))

        # Password text
        # Render the current text.
        txt_surface = font.render(text_name, True, color_name)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box_name.w = width
        # draws a line under the text for better visibility
        pg.draw.line(scr, (170, 170, 170), (100, 116), (100 + max(200, txt_surface.get_width() + 10), 116), 32)
        # Blit the text.
        scr.blit(txt_surface, (input_box_name.x + 5, input_box_name.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(scr, color_name, input_box_name, 2)

        # Password text
        # Render the current text.
        txt_surface = font.render(len(text_pass)*'*' if con_pass else text_pass, True, color_pass)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box_pass.w = width
        # draws a line under the text for better visibility
        pg.draw.line(scr, (170, 170, 170), (140, 246), (140 + max(200, txt_surface.get_width() + 10), 246), 32)
        # Blit the text.
        scr.blit(txt_surface, (input_box_pass.x + 5, input_box_pass.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(scr, color_pass, input_box_pass, 2)

        # draws the text for the input boxes
        print_txt(scr, 'User Name:', 100, 70, 18)
        print_txt(scr, 'Password:', 100, 200, 18)
        print_txt(scr, 'Log In', 180, 360, 18)
        print_txt(scr, 'Sign Up', 400, 360, 18)
        print_txt(scr, chr(164), 106, 231, 35)
        pg.draw.rect(scr, (255, 255, 255), button_login, 2)
        pg.draw.rect(scr, (255, 255, 255), button_signup, 2)
        pg.draw.rect(scr, color_inactive if con_pass else color_active, button_see_pass, 2)

        pg.display.flip()
        clock.tick(60)


# ============================================================================================================
# second stage - lobby of the game.
# ============================================================================================================

def pop_up(scr, txt, pop_type):
    """
    creates a pop up window with a special message
    """
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


def stage_2_rules():
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))

    # variables
    done = False
    page = 1
    bg = pg.image.load(r'C:\PR\img\bg_7.jpg')

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.Rect(0, 0, 80, 40).collidepoint(event.pos[0], event.pos[1]):
                    done = True

        # prints a return sign
        pg.draw.line(scr, (120, 120, 120), (0, 20), (80, 20), 40)
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(0, 0, 80, 40), 5)
        print_txt(scr, 'Return', 7, 12, 20)

        pg.draw.line(scr, (120, 120, 120), (310, 570), (390, 570), 40)
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(310, 550, 80, 40), 5)
        print_txt(scr, 'Next', 332, 562, 16)

        pg.draw.line(scr, (120, 120, 120), (410, 570), (490, 570), 40)
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(410, 550, 80, 40), 5)
        print_txt(scr, 'Previous', 415, 562, 16)
        pg.display.flip()
        clock.tick(60)

        def stage_2_game():
            clock = pg.time.Clock()
            scr = pg.display.set_mode((800, 600))

            # variables
            done = False
            popup_active = False
            wait = True
            rect_find_game = pg.Rect(390, 50, 250, 100)
            rect_wait = pg.Rect(350, 300, 330, 100)
            rect_cancel = pg.Rect(570, 330, 94, 40)
            bg = pg.image.load(r'C:\PR\img\bg_7.jpg')
            send = pg.image.load(r'C:\PR\img\send.png')

            # need to build a function that get text from the server and convert it to a list.
            friends = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd',
                       'e']

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

                        if pg.Rect(0, 0, 80, 40).collidepoint(event.pos[0], event.pos[1]):
                            done = True

                        if rect_find_game.collidepoint(event.pos[0], event.pos[1]):
                            print('random allay')
                            wait = True

                        if wait and rect_cancel.collidepoint(event.pos[0], event.pos[1]):
                            wait = False

                        for i in range(90, 90 + len(friends) * 26, 26):
                            if pg.Rect(195, i, 32, 22).collidepoint(event.pos[0], event.pos[1]):
                                active_sh = int((i - 90) / 26)
                                print(active_sh)

                scr.blit(bg, (0, 0))

                # draws the find a random allay button
                pg.draw.line(scr, (70, 70, 70), (390, 100), (640, 100), 100)
                pg.draw.rect(scr, (200, 200, 200), rect_find_game, 4)
                print_txt(scr, 'Find a Random Allay', 400, 90, 23)

                # prints a return sign
                pg.draw.line(scr, (120, 120, 120), (0, 20), (80, 20), 40)
                pg.draw.rect(scr, (200, 200, 200), pg.Rect(0, 0, 80, 40), 5)
                print_txt(scr, 'Return', 7, 12, 20)

                # draws  the wait sign and the cancel button
                if wait:
                    pg.draw.line(scr, (100, 100, 100), (350, 350), (680, 350), 100)
                    pg.draw.rect(scr, (200, 200, 200), rect_wait, 4)
                    print_txt(scr, 'Pleas wait', 360, 340, 23)
                    pg.draw.line(scr, (140, 140, 140), (570, 350), (664, 350), 40)
                    pg.draw.rect(scr, (230, 230, 230), rect_cancel, 4)
                    print_txt(scr, 'cancel', 580, 340, 23)

                # makes the structure of the friends list
                print_txt(scr, 'Active Allies', 38, 58, 20)
                pg.draw.rect(scr, (200, 200, 200), (30, 50, 200, 506), 4)
                pg.draw.line(scr, (200, 200, 200), (30, 85), (230, 85), 4)

                # prints an builds the friends and the grid.
                base_height = 91
                for friend in friends:
                    if base_height <= 550:
                        print_txt(scr, friend, 39, base_height, 18)
                        pg.draw.line(scr, (200, 200, 200), (30, base_height + 22), (230, base_height + 22), 4)
                        scr.blit(send, (195, base_height - 1))
                        base_height += 26

                pg.display.flip()
                clock.tick(60)


def stage_2_friends():
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))

    # variables
    done = False
    font = pg.font.Font(None, 32)
    active = False
    text_friend = ''
    input_box = pg.Rect(400, 100, 340, 32)
    color_inactive = (120, 120, 255)
    color_active = (90, 90, 255)
    bg = pg.image.load(r'C:\PR\img\bg_7.jpg')
    search = pg.image.load(r'C:\PR\img\search.png')

    # need to build a function that get text from the server and convert it to a list.
    friends = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.Rect(0, 0, 80, 40).collidepoint(event.pos[0], event.pos[1]):
                    done = True
                if pg.Rect(750, 100, 32, 32).collidepoint(event.pos[0], event.pos[1]):
                    print('search')
                if input_box.collidepoint(event.pos[0], event.pos[1]):
                    active = not active
                else:
                    active = False

            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_BACKSPACE:
                        text_friend = text_friend[:-1]
                    elif event.unicode not in [' ', ':', '\n', pg.K_RETURN, chr(13)]:
                        text_friend += event.unicode

        scr.blit(bg, (0, 0))
        # prints a return sign
        pg.draw.line(scr, (120, 120, 120), (0, 20), (80, 20), 40)
        pg.draw.rect(scr, (200, 200, 200), pg.Rect(0, 0, 80, 40), 5)
        print_txt(scr, 'Return', 7, 12, 20)

        print_txt(scr, 'My Friends', 38, 58, 20)
        pg.draw.rect(scr, (200, 200, 200), (30, 50, 200, 506), 4)
        pg.draw.line(scr, (200, 200, 200), (30, 85), (230, 85), 4)

        txt_surface = font.render(text_friend, True, color_active if active else color_inactive)
        # Resize the box if the text is too long.
        width = max(340, txt_surface.get_width() + 10)
        input_box.w = width
        pg.draw.line(scr, (170, 170, 170), (400, 116), (400 + max(340, txt_surface.get_width() + 10), 116), 32)
        # Blit the text.
        scr.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(scr, color_active if active else color_inactive, input_box, 2)

        # Blit the search icon
        scr.blit(search, (750, 100))

        base_height = 91

        # prints an builds the friends and the grid.
        for friend in friends:
            if base_height <= 550:
                print_txt(scr, friend, 39, base_height, 18)
                pg.draw.line(scr, (200, 200, 200), (30, base_height + 22), (230, base_height + 22), 4)
                base_height += 26

        pg.display.flip()
        clock.tick(60)


def stage_2_main(sock):
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
        data = ser_comm(sock)
        if 'pop' in data:
            pass
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
                    stage_2_friends()

                elif rect_rules.collidepoint(event.pos[0], event.pos[1]):
                    stage_2_rules()

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


# ============================================================================================================
# Main function, operates, call and coordinates all of functions.
# ============================================================================================================
def main():
    """
    main function, calls the needed functions in order to anabel a correct run of the game
    """
    sock = socket.socket()
    sock.connect((server_ip, 8820))
    # print(sock.recv(1024))
    # stage_1(sock)
    stage_2_main(sock)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
