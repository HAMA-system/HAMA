import openpyxl
import errorController

def load_xls(filename):
    try:
        xlsfile = openpyxl.load_workbook(filename, data_only=True)
        return xlsfile
    except:
        errorController.errorMsg(1)

def get_cell_data(file, sheetname ,cell):
    sheet = file.get_sheet_by_name(sheetname)
    return sheet[cell].value

def get_max_row(file, sheetname, column):
    i = row
    count = 0
    while True:
        cell = column + str(i)

        if get_cell_data(file, sheetname, cell) is None:
            return count
        else :
            count += 1
        i = i + 1

def get_singleline_data(file, sheetname, firstcell, lastcell):
    cell = firstcell
    data = []

    if firstcell[1:] != lastcell[1:]:
        if firstcell[1] >= 65 and firstcell[1] <= 90:
            if firstcell[2:] != lastcell[2:]:
                errorController.errorMsg(2)
        else:
            errorController.errorMsg(2)
        return data

    while cell!=lastcell:
        data.append(get_cell_data(file,sheetname,cell))
        cell = chr(ord(cell[:1])+1) + cell[1:]
    return data

def all_data_fetch(file, sheetname, firstcell, lastcell):
    fcell = firstcell
    lcell = lastcell

    data = []

    while get_cell_data(file, sheetname, fcell)!=None:
        data.append(get_singleline_data(file, sheetname, fcell, lcell))
        fcell = fcell[:1] + str(int(fcell[1:]) + 1)
        lcell = lcell[:1] + str(int(lcell[1:]) + 1)
        # print(fcell + ' ' + lcell)

    return data


def put_cell_data(file, sheetname, cell, text):
    # w = file.active
    s = file[sheetname]
    s[cell] = text

def save_xls(file):
    file.save("./data.xlsx")

def delete_completed_row(file, sheetname, firstcolumn, lastcolumn, row):
    i = row

    while True:
        firstcell = firstcolumn + str(i)
        lastcell = lastcolumn + str(i)
        cell = firstcell
        # print(str(i) + ': ' + firstcell + lastcell)

        if get_cell_data(file, sheetname, cell) is None:
            break

        if get_cell_data(file, sheetname, cell) == -1:
            print(i)
            while cell != lastcell:
                put_cell_data(file, sheetname, cell, ' ')
                cell = chr(ord(cell[:1]) + 1) + cell[1:]
            # print(str(i)+' deleted')
        i = i + 1

    # save_xls(file)
    # print("all -1 row is deleted")