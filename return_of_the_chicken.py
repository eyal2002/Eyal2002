import pygame as pg
import socket

server_ip = socket.gethostbyname(socket.gethostname())

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
    color_inactive = (200, 200, 255)
    color_active = (130, 130, 255)
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
                    elif event.unicode not in [' ', ':', '\n', pg.K_RETURN, chr(13)]:
                        text_name += event.unicode

                elif active_pass:
                    if event.key == pg.K_BACKSPACE:
                        text_pass = text_pass[:-1]
                    elif event.unicode not in [' ', ':', '\n', pg.K_RETURN, chr(13)]:
                        text_pass += event.unicode

        # Change the current color of the input box.
        color_name = color_active if active_name else color_inactive
        color_pass = color_active if active_pass else color_inactive

        scr.fill((0, 0, 0))
        scr.blit(bg, (0, 0))
        # Render the current text.
        txt_surface = font.render(text_name, True, color_name)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box_name.w = width
        # Blit the text.
        scr.blit(txt_surface, (input_box_name.x + 5, input_box_name.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(scr, color_name, input_box_name, 2)

        # Render the current text.
        txt_surface = font.render(len(text_pass)*'*' if con_pass else text_pass, True, color_pass)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box_pass.w = width
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
# first stage - log in or sign up.
# ============================================================================================================
# ============================================================================================================
# Main function, operates, call and coordinates all of functions.
# ============================================================================================================
def main():
    """
    main function, calls the needed functions in order to anabel a correct run of the game
    """
    sock = socket.socket()
    # sock.connect((server_ip, 8820))
    # print(sock.recv(1024))
    stage_1(sock)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
