import os

class NFMethods:

    def map_nf_path(self):

        user_path = os.path.expanduser('~')

        return f'{user_path}/NFe.ini'

    def write_conf(self, file_path, file_dict):

        with open(file_path, 'w') as file:
            
            for key, value in file_dict.items():

                file.write(f'{key}={value}\n')
