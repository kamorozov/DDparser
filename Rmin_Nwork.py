import xlsxwriter as xlsw

def x_eq(y, mixture):
    eq_file = open('equation.txt', 'r', encoding='utf8')


def y_eq(x, mixture):
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

print('Перед тем как начать сделайте файл в блокноте в котором будут следующий колонки в следующем порядке: \n'
      '№ точки, Схема, x1F, , x1D, F, D, смесь. Разделить столбцы табуляцией.')

temp_path = input('Enter file(если файл вне директории то с полным путем): ')
if temp_path.find('\\') > -1:
    s = temp_path.split('\\')
    path = '/'.join(s)
    Path = path[:path.rfind('/') + 1]
    File = path[path.rfind('/') + 1:]
else:
    Path = temp_path[:temp_path.rfind('/') + 1]
    File = temp_path[temp_path.rfind('/') + 1:]

TextFile = open(Path + File, 'r')
temp_lines = TextFile.read().split()

dots = []
for j in range(0, len(temp_lines), 7):
    dots.append((int(temp_lines[j]), int(temp_lines[j + 1]), float(ch_comma_to_dot(temp_lines[j + 2])),
                 float(ch_comma_to_dot(temp_lines[j + 3])), float(ch_comma_to_dot(temp_lines[j + 4])),
                 float(ch_comma_to_dot(temp_lines[j + 5])), temp_lines[j + 6]))

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
