import os

class NFMethods:

    def map_nf_path(self):

        user_path = os.path.expanduser('~')

        return f'{user_path}/NFe.conf'

    def write_conf(self, file_path, data):

        with open(file_path, 'w') as file:
            
            for key, value in data.items():

                file.write(f'{key}={value}\n')
