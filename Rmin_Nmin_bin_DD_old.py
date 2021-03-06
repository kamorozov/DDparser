import matplotlib.pyplot as plt

def x_eq(y, mixture):
    if mixture == 'bt':
        yx = 0.8551 * y ** 4 - 0.8917 * y ** 3 + 0.6754 * y ** 2 + 0.3567 * y + 0.0022
    elif mixture == 'te':
        yx = 0.6986 * y ** 4 - 1.067 * y ** 3 + 1.028 * y ** 2 + 0.3335 * y + 0.0031
    elif mixture == 'ea':
        yx = - 2.815 * y ** 5 + 7.403 * y ** 4 - 5.5997 * y ** 3 + 1.9874 * y ** 2 + 0.0262 * y + 0.0024
    return yx


def y_eq(x: object, mixture: object) -> object:
    if mixture == 'bt':
        xy = - 0.4191 * x ** 4 + 1.5087 * x ** 3 - 2.3858 * x ** 2 + 2.2951 * x + 0.0005
    elif mixture == 'te':
        xy = - 0.7937 * x ** 4 + 2.0119 * x ** 3 - 2.2674 * x ** 2 + 2.0401 * x + 0.0059
    elif mixture == 'ea':
        xy = 4.0475 * x ** 5 - 12.916 * x ** 4 + 16.378 * x ** 3 - 10.649 * x ** 2 + 4.1377 * x + 0.0052
    return xy


def ch_comma_to_dot(string):
    if string.find(',') > -1:
        number = float(string[:string.find(',')] + '.' + string[string.find(',') + 1:])
    else:
        number = float(string)
    return number


def ch_d_to_c(number):
    string = str(round(number, 4))
    answer = string[:string.find('.')] + ',' + string[string.find('.') + 1:]
    return answer


def Rmin_Nmin(mix, x_1, x_1d, F):
    x_1w = 1 - x_1d
    D_work = F * (x_1 - x_1w)/(x_1d - x_1w)
    f = F / D_work

    R_min = (x_1d - y_eq(x_1, mix)) / (y_eq(x_1, mix) - x_1)
    R = R_min * 1.3
    y = x_1d
    x = x_1d
    N = 0
    x_pr = 0
    x_last = 0
    while x > x_1w:
        x = x_eq(y, mix)
        x_last = x
        if round(x_last, 5) > round(x_pr, 5):
            N = -1
            break
        else:
            if round(x_last, 5) == round(x_pr, 5):
                break
            if x > x_1:
                y_work_up = R / (R + 1) * x + x_1d / (R + 1)
                y = y_work_up
            elif x < x_1:
                y_work_down = (R + f) / (R + 1) * x - (1 - f) / (R + 1) * x_1w
                y = y_work_down
            x_pr = x_last
            N += 1
    return R_min, R, D_work, N


def save_graph(mix, x_1, x_1d, F):
    x_1w = 1 - x_1d

    D_work = F * (x_1 - x_1w)/(x_1d - x_1w)
    f = F / D_work

    R_min = (x_1d - y_eq(x_1, mix)) / (y_eq(x_1, mix) - x_1)
    R = R_min * 1.3

    y = x_1d
    x = x_1d

    x_work = [x]
    y_work = [y]

    N = 0
    x_pr = 0
    x_last = 0

    while x > x_1w:
        x = x_eq(y, mix)
        x_work.append(x)
        y_work.append(y_eq(x, mix))
        x_last = x
        if round(x_last, 5) > round(x_pr, 5):
            N = -1
            break
        else:
            if round(x_last, 5) == round(x_pr, 5):
                break
            if x > x_1:
                y_work_up = R / (R + 1) * x + x_1d / (R + 1)
                y = y_work_up
                x_work.append(x)
                y_work.append(y)
            elif x < x_1:
                y_work_down = (R + f) / (R + 1) * x - (1 - f) / (R + 1) * x_1w
                y = y_work_down
                x_work.append(x)
                y_work.append(y)
            x_pr = x_last
            N +=1

    plt.plot(x_work, y_work)

    x = []
    y =[]
    for i in range(0, 101):
        x.append(i / 100)
        y_i = y_eq(i / 100, mix)
        y.append(y_i)
    plt.plot([0, 1], [0, 1])
    plt.plot(x, y)

    x_work_line = []
    y_work_line = []
    for j in range(int(x_1w * 1000), int(x_1d * 1000 + 1)):
        x_work_line.append(j / 1000)
        if j / 1000 <= x_1:
            y_work_down = (R + f) / (R + 1) * (j / 1000) - (1 - f) / (R + 1) * x_1w
            y_work_line.append(y_work_down)
        elif j / 1000 >= x_1:
            y_work_up = R / (R + 1) * (j / 1000) + x_1d / (R + 1)
            y_work_line.append(y_work_up)

    plt.plot(x_work_line, y_work_line)
    plt.axis([0, 1, 0, 1])
