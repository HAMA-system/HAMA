import openpyxl

def load_xls(filename):
    try:
        xlsfile = openpyxl.load_workbook(filename)
        return xlsfile
    except:
        print("can't open " + filename + " file")

def get_cell_data(filename, sheetname ,cell):
    sheet = filename.get_sheet_by_name(sheetname)
    return sheet[cell].value

def get_singleline_data(filename, sheetname, firstcell, lastcell):
    cell = firstcell
    data = []

    if firstcell[1:]!=lastcell[1:]:
        print("첫 셀과 마지막 셀이 같은 행에 있지 않음")
        return data

    while cell!=lastcell:
        data.append(get_cell_data(filename,sheetname,cell))
        cell = chr(ord(cell[:1])+1) + cell[1:]
    return data