from . import NFMethods

class NFController(NFMethods):
    
    def __init__(self, data):

        self._data = data
        self._file_path = self.map_nf_path()
        self._ini = self.generate_ini(self._data)

    def execute(self):

        self.write_ini(self._file_path, self._ini)