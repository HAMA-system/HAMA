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

# def get_singleline_data(file, sheet, cell):