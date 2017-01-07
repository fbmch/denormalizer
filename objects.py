
from collections import UserList, UserDict, defaultdict


class BaseSheet(UserDict):

    def __init__(self, name, id_manager, _dict):
        UserDict.__init__(self, _dict)
        self.name = name
        self.id_manager = id_manager

    def table(self):
        titles = [ self.id_manager.title ] + self.titles
        _table = [ titles ]
        for k in sorted(self):
            _table.append( [ self.id_manager.reconstruct(k) ] + self[k] )
        return _table 


class Sheet(BaseSheet):
    """
        A denormalized sheet
        keys are unique identifiers, values are remaining attributes
        Be sure to understand what ID manager does 
    """
    INDEX_TITLES = 0
    OFFSET_ROWS = 1
    INDEX_ID = 0
    OFFSET_COLUMNS = INDEX_ID + 1

    def __init__(self, name, data, id_manager):
        """
            discard first column
        """
        self.titles = [ '{}_{}'.format(name, title) for title in data[Sheet.INDEX_TITLES][Sheet.OFFSET_COLUMNS:] ]
        
        d = defaultdict(list)

        for l in data[Sheet.OFFSET_ROWS:]:
            _id = id_manager.extract(l[Sheet.INDEX_ID])
            d[_id] += l[Sheet.OFFSET_COLUMNS:]
    
        BaseSheet.__init__(self, name, id_manager, d)

        len_values = dict((k, len(v)) for k,v in self.items())
        len_row_max = max(len_values.values())
        number_titles_old = len(self.titles) 
        number_titles_new = int( len_row_max / number_titles_old )
        for i in range(2, 1 + number_titles_new ):

            self.titles += [ '{}_{}'.format(title, i) for title in self.titles[:number_titles_old] ]

        for k, v in len_values.items():
            if v != len_row_max:
                self[k] += ( len_row_max - v ) * ['']


class Sheets(BaseSheet):

    def __init__(self, name, sheets, id_manager):
        d = dict(sheets[0]) 
              
        self.titles = sheets[0].titles

        for sheet in sheets[1:]:

            for k in set(d).difference(sheet.keys()):
                d[k] += len(sheet.titles) * ['']

            for k, v in sheet.items():

                if k not in d.keys():
                    d[k] = len(self.titles) * [''] + v

                else:
                    d[k] += v
          
          

            self.titles += sheet.titles 
           
  
        BaseSheet.__init__(self, name, id_manager, d)



