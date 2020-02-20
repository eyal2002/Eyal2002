import pygame as pg
import socket
import select
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
    font = pg.font.Font('freesansbold.ttf', size)
    text = font.render(str(txt), True, white)
    scr.blit(text, (x, y))


def ser_comm(sock):
    data = 'none'
    rlist, wlist, xlist = select.select([sock], [sock], [])
    for current_socket in rlist:
        if current_socket is sock:
            data = sock.recv(1024).decode()
    return data


def stage_2_main():
    clock = pg.time.Clock()
    scr = pg.display.set_mode((800, 600))

    # variables
    done = False
    rect_custom = pg.Rect(530, 55, 250, 100)
    rect_game = pg.Rect(530, 185, 250, 100)
    rect_friends = pg.Rect(530, 315, 250, 100)
    rect_rules = pg.Rect(530, 445, 250, 100)

    # main while loop
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        scr.fill((30, 30, 30))
        print_txt(scr, 'Customization', rect_custom.x + 17, rect_custom.y + 35, 30)
        print_txt(scr, 'To Game Lobby', rect_game.x + 10, rect_game.y + 35, 30)
        print_txt(scr, 'Friends', rect_friends.x + 70, rect_friends.y + 35, 30)
        print_txt(scr, 'Rules and', rect_rules.x + 50, rect_rules.y + 15, 30)
        print_txt(scr, 'Instructions', rect_rules.x + 35, rect_rules.y + 55, 30)
        pg.draw.rect(scr, (200, 200, 200), rect_custom, 2)
        pg.draw.rect(scr, (200, 200, 200), rect_friends, 2)
        pg.draw.rect(scr, (200, 200, 200), rect_rules, 2)
        pg.draw.rect(scr, (200, 200, 200), rect_game, 2)
        pg.display.flip()
        clock.tick(30)


def main():
    # sock = socket.socket()
    # sock.connect((server_ip, 8820))
    # print(sock.recv(1024))
    stage_2_main()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
