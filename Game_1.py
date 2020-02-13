# -*- coding: utf-8 -*-
import pygame
import sys


def ship(x, y):
    return


def return_of_the_chicken():
    """
    Add Documentation here
    """
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Game_1')
    pygame.display.set_icon(pygame.image.load(r'C:\PY\PR\img\game_icon_2.png'))
    pygame.mouse.set_visible(1)
    sp_tr = pygame.image.load(r'C:\PY\PR\img\SPnn.png')
    b_g = pygame.image.load(r'C:\PY\PR\img\bg_2.jpg')
    ls_g = pygame.image.load(r'C:\PY\PR\img\laser_g.png')

    p_x = 50
    p_y = 50
    width = 50
    hight = 50
    vel = 5
    run = True
    c_s = 0
    shot_delay = 0
    shot_amount = 8
    shots = []
    pygame.mouse.set_visible(False)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        #Player movent
        pos = pygame.mouse.get_pos()
        if keys[pygame.K_LEFT] and p_x > 4:
            p_x -= vel
        if keys[pygame.K_RIGHT] and p_x < 796 - width:
            p_x += vel
        if keys[pygame.K_UP] and p_y > 4:
            p_y -= vel
        if keys[pygame.K_DOWN] and p_y < 596 - hight:
            p_y += vel
        p_x = pos[0] - 25
        p_y = pos[1] - 20
        #Shots
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0] == 1) and shot_delay == 0:
            c_s = 22
            shot_delay = shot_amount
            shots.append([c_s, p_x + 23, p_y + 7])
        if c_s > 0:
            for i in range(len(shots)):
                shots[i][0] -= 1
                shots[i][2] -= 30
            c_s -= 1
        if shot_delay > 0:
            shot_delay -= 1
        try:
            if shots[0][0] == 0:
                shots = shots[1:]
        except:
            shots = []
        scr.fill((0, 0, 0))
        scr.blit(b_g, (0, 0))
        for i in shots:
            #pygame.draw.rect(scr, (50, 255, 50), (i[1], i[2], 4, hight))
            scr.blit(ls_g, (i[1] - 3, i[2]))
        #pygame.draw.rect(scr, (50, 255, 50), (s_x, s_y, 4, hight))
        scr.blit(sp_tr, (p_x, p_y))
        #pygame.draw.rect(scr, (170, 255, 1), (350, 50, 100, 30))
        pygame.display.update()
    pygame.quit()


def main():
    return_of_the_chicken()


if __name__ == '__main__':
    main()