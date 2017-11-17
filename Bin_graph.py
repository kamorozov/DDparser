import matplotlib.pyplot as plt

def x_eq(y, mixture):
    yx = eval(equations_yx.get(mixture))
    return yx

def y_eq(x, mixture):
    xy = eval(equations_xy.get(mixture))
    return xy

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

eq_file = open('equation.txt', 'r')
equations_yx = {}
equations_xy = {}
for temp_line in eq_file:
    if temp_line[0] != '#':
        line = temp_line.split('\t')
        line[2] = line[2][:-1]
        eq = line[2].split(',')
        eq = '.'.join(eq)

        for i in range(2, 10):
            if eq.find('x' + str(i)) > -1:
                eq = eq[:eq.find('x' + str(i))] + ' * x ** ' + str(i) + eq[eq.find('x' + str(i)) + 2:]

        if eq.find('x +') > -1:
            eq = eq[:eq.find('x +')] + ' * x' + eq[eq.find('x +') + 1:]
        elif eq.find('x -') > -1:
            eq = eq[:eq.find('x -')] + ' * x' + eq[eq.find('x -') + 1:]
        elif eq[-1] == 'x':
            eq[-1] = ' * x'

        if line[1] == 'yx':
            while eq.find('x') > -1:
                eq = eq[:eq.find('x')] + 'y' + eq[eq.find('x') + 1:]

        line[2] = eq

        if line[1] == 'yx':
            equations_yx[line[0]] = line[2]
        else:
            equations_xy.update({line[0]: line[2]})

print('Список имеющихся систем:')
for mix in equations_xy:
    print(mix, end=' ')
print()
mix = input('Система: ')
x_1 = float(input('Исходный состав по первому компоненту: '))
x_1d = float(input('Состав дистилата по первому компоненту: '))
F = float(input('Поток исходный смеси: '))

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
plt.show()
