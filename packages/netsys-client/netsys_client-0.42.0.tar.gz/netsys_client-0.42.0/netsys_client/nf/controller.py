from . import NFMethods

class NFController(NFMethods):
    
    def __init__(self, data):

        self._data = data
        self._file_path = self.map_nf_path()

    def execute(self):

        input('teste:')

        self.write_conf(self._file_path, self._data)