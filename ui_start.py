import pygame as pg


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
    font = pg.font.Font('freesansbold.ttf', 18)
    text = font.render(str(txt), True, white)
    scr.blit(text, (x, y))


def log_in():
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box_name = pg.Rect(100, 100, 240, 32)
    input_box_pass = pg.Rect(100, 230, 240, 32)
    color_inactive = (200, 200, 255)
    color_active = (90, 90, 255)
    color_name = color_inactive
    color_pass = color_inactive
    active_name = False
    active_pass = False
    text_name = ''
    text_pass = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box_name.collidepoint(event.pos):
                    # Toggle the active variable.
                    active_name = not active_name
                    active_pass = False
                elif input_box_pass.collidepoint(event.pos):
                    # Toggle the active variable.
                    active_pass = not active_pass
                    active_name = False

                else:
                    active_name = False
                    active_pass = False

                # Change the current color of the input box.
                color_name = color_active if active_name else color_inactive
                color_pass = color_active if active_pass else color_inactive

            if event.type == pg.KEYDOWN:
                if (active_name or active_pass) and event.key == pg.K_RETURN:
                    print(text_name + ' ' + text_pass)
                    text_name = ''
                    text_pass = ''
                elif active_name:
                    if event.key == pg.K_BACKSPACE:
                        text_name = text_name[:-1]
                    else:
                        text_name += event.unicode

                elif active_pass:
                    if event.key == pg.K_BACKSPACE:
                        text_pass = text_pass[:-1]
                    else:
                        text_pass += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text_name, True, color_name)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box_name.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box_name.x + 5, input_box_name.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color_name, input_box_name, 2)

        # Render the current text.
        txt_surface = font.render(len(text_pass)*'*', True, color_pass)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box_pass.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box_pass.x + 5, input_box_pass.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color_pass, input_box_pass, 2)

        # draws the text for the input boxes
        print_txt(screen, 'User Name:', 100, 70)
        print_txt(screen, 'Password:', 100, 200)
        print_txt(screen, 'Log In', 180, 360)
        print_txt(screen, 'Sign Up', 400, 360)
        pg.draw.rect(screen, (255, 255, 255), (165, 349, 83, 40), 2)
        pg.draw.rect(screen, (255, 255, 255), (385, 349, 96, 40), 2)

        pg.display.flip()
        clock.tick(60)


def main():
    log_in()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
