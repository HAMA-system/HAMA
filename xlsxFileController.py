import openpyxl
import errorController

def load_xls(filename):
    try:
        xlsfile = openpyxl.load_workbook(filename)
        return xlsfile
    except:
        errorController.errorMsg(1)

def get_cell_data(file, sheetname ,cell):
    sheet = file.get_sheet_by_name(sheetname)
    return sheet[cell].value

def get_singleline_data(file, sheetname, firstcell, lastcell):
    cell = firstcell
    data = []

    if firstcell[1:]!=lastcell[1:]:
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
        print(fcell + ' ' + lcell)

    return data