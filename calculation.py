from for_bd import all_dish_for_one


def calculation(name_dish, count_people):
    return ''.join(f'{key} - {round(value * count_people, 2)}\n' for key, value in all_dish_for_one[name_dish].items())


if __name__ == '__main__':
    r = calculation('кура кусочками', 5)
    print(r, sep='\n')
