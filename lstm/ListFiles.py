import os

class ListFiles:
    path_choose = None
    path_list = {}

    def __init__(self):
        pass

    def list_files(self, fold_path='./save'):
        index = 0
        self.path_list = {}
        for dirname, _, filenames in os.walk(fold_path):
            for filename in filenames:
                if filename.endswith(".h5"):
                    self.path_list[index] = (os.path.join(dirname, filename))
                    index += 1

    def choose_file(self, index):
        return self.path_list[index]

    def show_files(self):
        for item in self.path_list.items():
            print(item[0], '-', item[1])

