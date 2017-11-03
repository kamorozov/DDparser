import os
import xlsxwriter

# преобразование файла в список
def lists_from_file(FileName):
    TextFile = open(FileName, 'r')
    templines = TextFile.read().rsplit('\n')
    while '' in templines:
        templines.remove('')
    lines = []
    for i in range(len(templines)):
        line_temp = templines[i].split(': ')
        if len(line_temp) == 2:
            line = [line_temp[0], line_temp[1]]
            lines.append(line)
        elif len(line_temp) == 3:
            line = [line_temp[0], line_temp[1], line_temp[2]]
            lines.append(line)
        else:
            lines.append(templines[i])

    BasicData = lines[:lines.index('Top section')]
    tempBasicData = BasicData[6].split()
    tempBasicData.insert(0, str(tempBasicData[0] + ' ' + tempBasicData[1] + ' ' + tempBasicData[2]))
    while len(tempBasicData) > 2:
        tempBasicData.pop(1)
    BasicData.insert(6, tempBasicData)
    BasicData.pop(7)

    Topsection = lines[lines.index('Top section') + 1: lines.index('Bottom section')]
    Bottomsection = lines[lines.index('Bottom section') + 1:]
    TextFile.close()
    return BasicData, Topsection, Bottomsection


# списки информаци
def section(name_of_Section):
    for i in range(1, len(name_of_Section), 2):
        y = name_of_Section[i][1]
        y_list = y.split()
        y_list.pop(-1)
        name_of_Section[i].insert(1, y_list)
        name_of_Section[i].pop(0)
        name_of_Section[i].pop(1)
        name_of_Section[i][0].insert(0, name_of_Section[i][1])
        name_of_Section[i].pop(1)
    temp_section = []
    for j in range(1, len(name_of_Section), 2):
        temp_section.append(name_of_Section[j - 1])
        temp_section.append(name_of_Section[j][0])
    if len(temp_section) > 0:
        if temp_section[1][0] > temp_section[-1][0]:
            temp2_section = []
            for k in range(1, len(temp_section) // 2, 2):
                temp2_section.append(temp_section[k - 1])
                temp2_section.append(temp_section[-k])
            return temp2_section
        else:
            return temp_section
    else:
        return temp_section

# максимальное количество тарелокв для записи
def max_tays(Section, var_max_trays, NameOfBook, NameOfSheet):
    if len(Section) // 2 > var_max_trays:
        for i in range(len(Section) // 2):
            sheet = NameOfBook.get_worksheet_by_name(NameOfSheet)
            sheet.write(i + 2, 0, 'Tray# ' + str(i + 1))
        var_max_trays = len(Section) // 2


# Обработка пути к паке с файлами
temp_path = str(input('Enter path to folder with files: '))
if temp_path.find('\\') > -1:
    s = temp_path.split('\\')
    path = '/'.join(s)
else:
    path = temp_path

if path[:-1] is not '/':
    path += '/'

# создание таблицы excel
result_xlsx = path + 'DD_Summary.xlsx'

workbook = xlsxwriter.Workbook(result_xlsx)
sh_BD = workbook.add_worksheet('Basic Data')
sh_TS = workbook.add_worksheet('Top Section')
sh_BS = workbook.add_worksheet('Bottom Section')
max_trays_top = 0
max_trays_bottom = 0

# создаем список файлов для папки
list_of_files = []
list_of_file_names = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        list_of_files.append(os.path.join(path, file))
        list_of_file_names.append(file[:-4])

# заполнение файла
c_BD = 1
c_TS = 1
c_BS = 1
for file in list_of_files:
    lists_of_data = lists_from_file(file)
    BasicData = lists_of_data[0]
    TopSection = section(lists_of_data[1])
    BottomSection = section(lists_of_data[2])

    # добавление информации на вкладку Basic Data
    sheet_BD = workbook.get_worksheet_by_name('Basic Data')
    # записали название строк
    for i in range(len(BasicData)):
        sh_BD.write(1 + i, 0, BasicData[i][0])
    sh_BD.write(len(BasicData) + 2, 0, 'Real total trays number')
    sh_BD.write(len(BasicData) + 3, 0, 'Real top section trays number')
    sh_BD.write(len(BasicData) + 4, 0, 'Real bottom section trays number')
    r_BD = 1
    sheet_BD.write(0, c_BD, str(list_of_file_names[list_of_files.index(file)][:-4]))
    for i in range(0, len(BasicData)):
        try:
            sheet_BD.write_number(r_BD, c_BD, float(BasicData[i][1]))
        except:
            sheet_BD.write(r_BD, c_BD, BasicData[i][1])
        r_BD += 1
    sheet_BD.write_number(len(BasicData) + 2, c_BD, len(TopSection) // 2 + len(BottomSection) // 2)
    sheet_BD.write_number(len(BasicData) + 3,  c_BD, len(TopSection) // 2)
    sheet_BD.write_number(len(BasicData) + 4, c_BD, len(BottomSection) // 2)
    if len(TopSection) > 0:
        for i in range(len(TopSection[1]) - 1):
            sheet_BD.write(len(BasicData) + 5 + i, 0, 'x' + str(i + 1) + 'D')
            sheet_BD.write_number(len(BasicData) + 5 + i, c_BD, float(TopSection[1][i + 1]))
    if len(BottomSection) > 0:
        for i in range(len(BottomSection[-1]) - 1):
            if len(TopSection) > 0:
                sheet_BD.write(len(BasicData) + 4 + i + len(TopSection[1]), 0, 'x' + str(i + 1) + 'W')
                sheet_BD.write_number(len(BasicData) + 4 + i + len(TopSection[1]), c_BD,float(BottomSection[-1][i + 1]))
            else:
                sheet_BD.write(len(BasicData) + 9 + i , 0, 'x' + str(i + 1) + 'W')
                sheet_BD.write_number(len(BasicData) + 9 + i , c_BD, float(BottomSection[-1][i + 1]))
    c_BD += 1

    # добавление информации на вкладку Top Section
    sheet_TS = workbook.get_worksheet_by_name('Top Section')
    r_TS = 2
    sheet_TS.write(0, c_TS, str(list_of_file_names[list_of_files.index(file)][:-4]))
    sheet_TS.write(1, c_TS, 'T, K')
    if len(TopSection) > 0:
        for x in range(1, len(TopSection[1])):
            sheet_TS.write(1, c_TS + x, 'x' + str(x))
        for i in range(1, len(TopSection), 2):
            for j in range(len(TopSection[i])):
                sheet_TS.write_number(r_TS, c_TS + j, float(TopSection[i][j]))
            r_TS += 1
        c_TS += len(TopSection[1])
    max_tays(TopSection, max_trays_top, workbook, 'Top Section')

    # добавление информации на вкладку Bottom Section
    sheet_BS = workbook.get_worksheet_by_name('Bottom Section')
    r_BS = 2
    sheet_BS.write(0, c_BS, str(list_of_file_names[list_of_files.index(file)][:-4]))
    sheet_BS.write(1, c_BS, 'T, K')
    for x in range(1, len(BottomSection[1])):
        sheet_BS.write(1, c_BS + x, 'x' + str(x))
    for i in range(1, len(BottomSection), 2):
        for j in range(len(BottomSection[i])):
            sheet_BS.write_number(r_BS, c_BS + j, float(BottomSection[i][j]))
        r_BS += 1
    c_BS += len(BottomSection[1])
    max_tays(BottomSection, max_trays_bottom, workbook, 'Bottom Section')

print('All done!')
workbook.close()
