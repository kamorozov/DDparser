import os
import xlsxwriter
import xlrd

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
    return temp_section

# path = 'C:/Users/kamorozov/PycharmProjects/DDparser/1/'
path = str(input('Enter path to folder with files(using / for separation): '))
result_xlsx = path + 'DD_Summary.xlsx'

# open the file for reading
wbRD = xlrd.open_workbook('DD_Summary_Basic.xlsx')
sheets = wbRD.sheets()

# open the same file for writing (just don't write yet)
workbook = xlsxwriter.Workbook(result_xlsx)

# run through the sheets and store sheets in workbook
# this still doesn't write to the file yet
for sheet in sheets: # write data from old file
    newSheet = workbook.add_worksheet(sheet.name)
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            newSheet.write(row, col, sheet.cell(row, col).value)

# создаем список файлов для папки
list_of_files = []
list_of_file_names = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        list_of_files.append(os.path.join(path, file))
        list_of_file_names.append(file)
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
    r_BD = 1
    sheet_BD.write(0, c_BD, str(list_of_file_names[list_of_files.index(file)]))
    for i in range(0, len(BasicData)):
        sheet_BD.write(r_BD, c_BD, BasicData[i][1])
        r_BD += 1
    sheet_BD.write(len(BasicData) + 2, c_BD, len(TopSection) // 2 + len(BottomSection) // 2)
    sheet_BD.write(len(BasicData) + 3, c_BD, len(TopSection) // 2)
    sheet_BD.write(len(BasicData) + 4, c_BD, len(BottomSection) // 2)
    for i in range(len(TopSection[1]) - 1):
        sheet_BD.write(len(BasicData) + 5 + i, 0, 'x' + str(i + 1) + 'D')
        sheet_BD.write(len(BasicData) + 5 + i, c_BD, TopSection[1][i + 1])
    for i in range(len(BottomSection[-1]) - 1):
        sheet_BD.write(len(BasicData) + 4 + i + len(TopSection[1]), 0, 'x' + str(i + 1) + 'W')
        sheet_BD.write(len(BasicData) + 4 + i + len(TopSection[1]), c_BD, BottomSection[-1][i + 1])
    c_BD += 1

    # добавление информации на вкладку Top Section
    sheet_TS = workbook.get_worksheet_by_name('Top Section')
    r_TS = 2
    sheet_TS.write(0, c_TS, str(list_of_file_names[list_of_files.index(file)]))
    sheet_TS.write(1, c_TS, 'T, K')
    for t in range(1, len(TopSection[1])):
        sheet_TS.write(1, c_TS + t, 'x' + str(t))
    for i in range(1, len(TopSection), 2):
        for j in range(len(TopSection[i])):
            sheet_TS.write(r_TS, c_TS + j, TopSection[i][j])
        r_TS += 1
    c_TS += len(TopSection[1])

    # добавление информации на вкладку Bottom Section
    sheet_BS = workbook.get_worksheet_by_name('Bottom Section')
    r_BS = 2
    sheet_BS.write(0, c_BS, str(list_of_file_names[list_of_files.index(file)]))
    sheet_BS.write(1, c_BS, 'T, K')
    for t in range(1, len(BottomSection[1])):
        sheet_BS.write(1, c_BS + t, 'x' + str(t))
    for i in range(1, len(BottomSection), 2):
        for j in range(len(BottomSection[i])):
            sheet_BS.write(r_BS, c_BS + j, BottomSection[i][j])
        r_BS += 1
    c_BS += len(BottomSection[1])


print('All done!')
workbook.close()