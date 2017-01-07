
import xlrd

class Xlrd:


    def load(filename):
        
        book = xlrd.open_workbook(filename)

        return [ (sheet.name, sheet._cell_values) for sheet in book.sheets() ]
   

