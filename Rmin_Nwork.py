import xlsxwriter as xlsw

def x_eq(y, mixture):
    yx = eval(equations_yx.get(mixture))
    return yx


def y_eq(x, mixture):
    xy = eval(equations_xy.get(mixture))
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
    x_pr = x_eq(0.9999, mix)
    x_last = 0
    while x > x_1w:
        x = x_eq(y, mix)
        x_last = x
        if round(x_last, 3) > round(x_pr, 3):
            N = -1
            break
        else:
            if round(x_last, 3) == round(x_pr, 3):
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

print('Перед тем как начать сделайте файл в блокноте в котором будут следующий колонки в следующем порядке: \n'
      '№ точки, Схема, x1F, , x1D, F, D, смесь. Разделить столбцы табуляцией. \n'
      'Список имеющихся систем:')
for mix in equations_xy:
    print(mix, end=' ')
print()

temp_path = input('Укажите файл (если файл вне директории то с полным путем): ')
if temp_path.find('\\') > -1:
    s = temp_path.split('\\')
    path = '/'.join(s)
    Path = path[:path.rfind('/') + 1]
    File = path[path.rfind('/') + 1:]
else:
    Path = temp_path[:temp_path.rfind('/') + 1]
    File = temp_path[temp_path.rfind('/') + 1:]

TextFile = open(Path + File, 'r')
temp_lines = TextFile.readlines()

dots = []
for temp_line in temp_lines:
    temp_line = temp_line.split()
    dots.append((int(temp_line[0]), int(temp_line[1]), float(ch_comma_to_dot(temp_line[2])),
                 float(ch_comma_to_dot(temp_line[3])), float(ch_comma_to_dot(temp_line[4])),
                 float(ch_comma_to_dot(temp_line[5])), temp_line[6]))

result_xlsx = Path + 'DD_Summary ' + File[:File.rfind('.')] + '.xlsx'
workbook = xlsw.Workbook(result_xlsx)
sheet = workbook.add_worksheet('Data')
title = ('№ точки', 'Схема', 'x1F', 'F', 'D', 'B', 'Rmin', 'Vmin', 'Rwork', 'Dwork', 'Vwork', 'Nwork', 'смесь')

for name in title:
    sheet.write(0, title.index(name), name)

row = 1
col = 0
for dot in dots:
    print(dots.index(dot) + 1)
    RminRN = Rmin_Nmin(dot[6], dot[2], dot[3], dot[4])
    sheet.write(row + dots.index(dot), 0, dot[0])
    sheet.write(row + dots.index(dot), 1, dot[1])
    sheet.write_number(row + dots.index(dot), 2, dot[2])
    sheet.write_number(row + dots.index(dot), 3, dot[4])
    sheet.write_number(row + dots.index(dot), 4, dot[5])
    sheet.write_number(row + dots.index(dot), 5, dot[4] - dot[5])
    sheet.write_number(row + dots.index(dot), 6, RminRN[0])
    sheet.write_number(row + dots.index(dot), 7, dot[5] * (RminRN[0] + 1))
    sheet.write_number(row + dots.index(dot), 8, RminRN[1])
    sheet.write_number(row + dots.index(dot), 9, RminRN[2])
    sheet.write_number(row + dots.index(dot), 10, RminRN[2] * (RminRN[1] + 1))
    sheet.write(row + dots.index(dot), 11, RminRN[3])
    sheet.write(row + dots.index(dot), 12, dot[-1])

print('All done!')
workbook.close()
