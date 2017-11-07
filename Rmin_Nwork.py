import xlsxwriter
import Rmin_Nmin_bin_DD as RN
import matplotlib.pyplot as plt
print('Перед тем как начать сделайте файл в блокноте в котором будут следующий колонки в следующем порядке: \n'
      '№ точки, Схема, x1F, , x1D, F, D, смесь.')

# temp_path = input('Enter file(если файл вне директории то с полным путем): ')
temp_path = 'Test files/2 col 5 sheme.txt'
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
for j in range(0,len(temp_lines),7):
    dots.append((int(temp_lines[j]), int(temp_lines[j + 1]), float(RN.ch_comma_to_dot(temp_lines[j + 2])),
                 float(RN.ch_comma_to_dot(temp_lines[j + 3])), float(RN.ch_comma_to_dot(temp_lines[j + 4])),
                 float(RN.ch_comma_to_dot(temp_lines[j + 5])), temp_lines[j + 6]))

print(dots)

result_xlsx = Path + 'DD_Summary ' + File[:File.rfind('.')] + '.xlsx'
workbook = xlsxwriter.Workbook(result_xlsx)
sheet = workbook.add_worksheet('Rmin Rwork Nwork')
gr_sheet = workbook.add_worksheet('Graphics')
title = ('№ точки', 'Схема', 'x1F','F', 'D', 'B', 'Rmin', 'Vmin','Rwork', 'Dwork', 'Vwork', 'Nwork', 'смесь')
for name in title:
    sheet.write(0, title.index(name), name)
row = 1
col = 0
for dot in dots:
    RminRN = RN.Rmin_Nmin(dot[6], dot[2], dot[3], dot[4])
    sheet.write(row + dots.index(dot), 0, dot[0])
    sheet.write(row + dots.index(dot), 1, dot[1])
    sheet.write(row + dots.index(dot), 2, dot[2])
    sheet.write(row + dots.index(dot), 3, dot[4])
    sheet.write(row + dots.index(dot), 4, dot[5])
    sheet.write(row + dots.index(dot), 5, dot[4] - dot[5])
    sheet.write(row + dots.index(dot), 6, RminRN[0])
    sheet.write(row + dots.index(dot), 7, dot[5] * (RminRN[0] + 1))
    sheet.write(row + dots.index(dot), 8, RminRN[1])
    sheet.write(row + dots.index(dot), 9, RminRN[2])
    sheet.write(row + dots.index(dot), 10, RminRN[2] * (RminRN[1] + 1))
    sheet.write(row + dots.index(dot), 11, RminRN[3])
    sheet.write(row + dots.index(dot), 12, dot[-1])
#    RN.save_graph(dot[6], dot[2], dot[3], dot[4])
#    fig_file = Path + str(dot[0]) + '_' + str(dot[1]) + '.png'
#    plt.savefig(fig_file, dpi = 150)




print('All DOOONE')
workbook.close()
