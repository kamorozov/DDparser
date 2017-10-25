import matplotlib.pyplot as plt

def x_eq(y):
    global mix
    mixture = mix
    if mixture == 'bt':
         x = 0.8551 * y ** 4 - 0.8917 * y ** 3 + 0.6754 * y ** 2 + 0.3567 * y + 0.0022
    elif mixture == 'te':
        x = 0.6986 * y ** 4 - 1.067 * y ** 3 + 1.028 * y ** 2 + 0.3335 * y + 0.0031
    elif mixture == 'ea':
        x = -6.2194 * y ** 6 + 16.525 * y ** 5 - 15.399 * y ** 4 + 6.9697 * y ** 3 - 1.1967 * y ** 2 + 0.3218 * y - 0.0004
    return x


def y_eq(x):
    global mix
    mixture = mix
    if mixture == 'bt':
        y = - 0.4191 * x ** 4 + 1.5087 * x ** 3 - 2.3858 * x ** 2 + 2.2951 * x + 0.0005
    elif mixture == 'te':
        y = - 0.7937 * x ** 4 + 2.0119 * x ** 3 - 2.2674 * x ** 2 + 2.0401 * x + 0.0059
    elif mixture == 'ea':
        y = -5.0929 * x ** 6 + 19.326 * x ** 5 - 30.215 * x ** 4 + 25.512 * x ** 3 - 12.88 *x **2 + 4.3483 * x + 0.0011
    return y


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


mix = input('смесь (bt, te, ea): ')
x_1_temp = input('количество первого компонента в питании(доли): ')
x_1 = ch_comma_to_dot(x_1_temp)
x_1d_temp = input('количество первого компонента в дистиллате(доли): ')
x_1d = ch_comma_to_dot(x_1d_temp)
F_temp = input('питание кмоль/ч: ')
F = ch_comma_to_dot(F_temp)
x_1w = 1 - x_1d
D = F * (x_1 - x_1w)/(x_1d - x_1w)
f = F / D
Rmin_ter = (1 - y_eq(x_1)) / (y_eq(x_1) - x_1)
Rmin = (x_1d - y_eq(x_1)) / (y_eq(x_1) - x_1)
R = Rmin * 1.3
y = x_1d
x = x_1d
x_work = [x]
y_work = [y]
N = 0
x_pr = 0
x_last = 0
while x > x_1w:
    x = x_eq(y)
    x_work.append(x)
    y_work.append(y_eq(x))
    x_last = x
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
#print(*(round(x, 4) for x in x_work))
#print(*(round(y, 4) for y in y_work))
print('Rmin (теоретическое) =', ch_d_to_c(Rmin_ter))
print('Rmin =', ch_d_to_c(Rmin))
print('R =', ch_d_to_c(R))
print('число тарело:', N)

x = [0]
y =[0]
for i in range(1, 100):
    x.append(i / 100)
    y_i = y_eq(i / 100)
    y.append(y_i)
plt.plot([0, 1], [0, 1])
x.append(1)
y.append(1)
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

