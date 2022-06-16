import os
from linkData import 링크

def replace():
    path = 링크[3] + 'test1'
    new_folder = 'test'
    dpath = 링크[3] + new_folder
    if new_folder not in os.listdir(링크[3]):
        os.mkdir(링크[3] + new_folder)
    for f in os.listdir(path):
        os.replace(path + '/' + f, dpath + '/' + f)
if __name__ == '__main__':
    replace()