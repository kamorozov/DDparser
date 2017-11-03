import xlsxwriter
import Rmin_Nmin_bin_DD as RN
import matplotlib.pyplot as plt

# temp_path = input('Enter file(если файл вне директории то с полным путем): ')
temp_path = 'C:/Users/mrbon/Downloads/Telegram Desktop/2 col 5 sheme.txt'
if temp_path.find('\\') > -1:
    s = temp_path.split('\\')
    path = '/'.join(s)
else:
    Path = temp_path[:temp_path.rfind('/') + 1]
    File = temp_path[temp_path.rfind('/') + 1:]

TextFile = open(Path + File, 'r')
templines = TextFile.read().split()
for i in range(6):
    templines.pop(0)
dots = []
for j in range(0,len(templines),6):
    dots.append((int(templines[j]), int(templines[j + 1]), templines[j + 2], float(RN.ch_comma_to_dot(templines[j + 3])), float(RN.ch_comma_to_dot(templines[j + 4])), float(RN.ch_comma_to_dot(templines[j + 5]))))

print(dots)

result_xlsx = Path + 'DD_Summary ' + File[:File.rfind('.')] + '.xlsx'
workbook = xlsxwriter.Workbook(result_xlsx)
sheet = workbook.add_worksheet('Rmin Rwork Nwork')
title = ('№ точки', 'Схема', 'x1F', 'Rmin', 'Rwork', 'Nwork', 'смесь')
for name in title:
    sheet.write(0, title.index(name), name)
row = 1
col = 0
for dot in dots:
    RminRN = RN.Rmin_Nmin(dot[2], dot[3], dot[4], dot[5])
    sheet.write(row + dots.index(dot), 0, dot[0])
    sheet.write(row + dots.index(dot), 1, dot[1])
    sheet.write(row + dots.index(dot), 2, dot[3])
    sheet.write(row + dots.index(dot), 3, RminRN[0])
    sheet.write(row + dots.index(dot), 4, RminRN[1])
    sheet.write(row + dots.index(dot), 5, RminRN[2])
    sheet.write(row + dots.index(dot), 6, dot[2])
print('All DOOONE')
workbook.close()
