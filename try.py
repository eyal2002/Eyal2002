import random


def names():
    name_list = []
    name = 'blank'
    while name != 'exit':
        name_list.append(name)
        name = input('enter a name:  ')
    return name_list[1:]


def main():
    # name_list = ['eyal', 'nahom', 'halifa', 'zoe', 'gai', 'lozon', 'noya', 'ben zvi', 'yonatan', 'itamar', 'gidi']
    # print(name_list)
    name_list = names()
    random.shuffle(name_list)
    print(name_list)
    print('\n\n')
    for i in range(int(len(name_list) / 2)):
        if len(name_list) == 3:
            print(name_list)
        else:
            print(name_list[:2])
            name_list = name_list[2:]


if __name__ == '__main__':
    main()
