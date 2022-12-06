import os


class Reader:
    def __init__(self, start_dir):
        self.files = []
        self.__search_files(start_dir)

    def __search_files(self, search_dir):
        os.chdir(search_dir)
        for file in os.listdir():
            os.chdir(search_dir)
            p = search_dir + '\\' + file
            if file in ['temp', 'cache'] or file.startswith('.'):
                pass
            elif os.path.isfile(p):
                if file.endswith(".php"):
                    self.files.append(p)
            elif os.path.isdir(p):
                self.__search_files(p)

    def get_files(self):
        return self.files
