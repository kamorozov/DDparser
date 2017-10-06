import os
import xlsxwriter

list_of_files = []
path = 'C:/Users/kamorozov/PycharmProjects/DDparser/1/'
#path
for file in os.listdir(path):
    if file.endswith(".txt"):
        list_of_files.append(os.path.join(path, file))

for file in list_of_files:
    FileName = file
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


    # create excel file
    workbook = xlsxwriter.Workbook('DD_Summary.xlsx')

    def newsheet(NameOfData, NameOfBook, NameOfSheet, Step, index):
        sheet = NameOfBook.add_worksheet(NameOfSheet)
        row = 1
        col = 0
        for item in range(0, len(NameOfData), Step):
            if index != 'no':
                sheet.write(row, col, NameOfData[item][index])
                row += 1
            else:
                sheet.write(row, col, NameOfData[item])
                row += 1
        return print('File is created. Added sheet', NameOfSheet)

    newsheet(BasicData, workbook, 'Basic Data', 1, 0)
    newsheet(Topsection, workbook, 'Top Section', 2, 'no')
    newsheet(Bottomsection, workbook, 'Bottom Section', 2, 'no')

    # add information from files

    def addinfosheet(NameOfData, NameOfBook, NameOfSheet, Step, index, File):
        global list_of_files
        sheet = NameOfBook.get_worksheet_by_name(NameOfSheet)
        row = 1
        col = 1 + list_of_files.index(File)
        print(col)
        for item in range(0, len(NameOfData), Step):
            if index != 'no':
                sheet.write(row, col, NameOfData[item][index])
                row += 1

    addinfosheet(BasicData, workbook, 'Basic Data', 1, 1, FileName)

print('All done')
workbook.close()
