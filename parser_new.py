import os
import xlsxwriter
import function as f




list_of_files = []
path = 'C:/Users/mrbon/PycharmProjects/DDparsertoxls/'
#path
for file in os.listdir(path):
    if file.endswith(".txt"):
        list_of_files.append(os.path.join(path, file))

for file in list_of_files:
    lists_of_data = f.lists_from_file(file)
    BasicData = lists_of_data[0]
    TopSection = f.section(lists_of_data[1])
    BottomSection = f.section(lists_of_data[2])
