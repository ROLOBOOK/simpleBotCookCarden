from for_bd import all_dish_for_one


def get_portion(name_dish, count_people, children=False):

    return ''.join(f'{key} - {calculation(value, count_people, children)}\n' for key, value in all_dish_for_one[name_dish].items())


def calculation(value, count_people, children, ):
    result = value * count_people
    if children:
        result = result / 3 * 2

    return round(result, 1)


if __name__ == '__main__':
    r = calculation('кура кусочками', 5)
    print(r, sep='\n')
