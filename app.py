from pathlib import Path

import xxlsx

from objects import Sheet, Sheets

from id_manager import IDManager

def main(excelfile):

    path = Path(excelfile)   
 
    sheets = xxlsx.Xlsx.load(str(path))

    x_sheets = []

    for name, data in sheets:

        print(name)

        x_sheets.append( Sheet(name, data, IDManager) )
   

    x = Sheets('', x_sheets, IDManager)

    filename = str(path.with_name('denormalized_' + path.name)) 

    xxlsx.Xlsx.dump(filename, x.table())

    print('Done, check', filename)



if __name__=='__main__':

    import importlib

    if importlib.util.find_spec('openpyxl') is None:
        raise RuntimeError('Run sudo pip3 install openpyxl')

    import argparse

    parser = argparse.ArgumentParser(description='denormalize xcel table with uid in the first column across multiple sheets')

    parser.add_argument('excelfile', metavar='xlsx', type=str, help='excel file to be denormaized')
    args = parser.parse_args()
    print(args)
    main(args.excelfile)
