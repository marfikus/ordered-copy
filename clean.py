import shutil
import os


path = "test/to"

dir_list = os.listdir(path)

for i in dir_list:
    # print(i)
    obj = os.path.join(path, i)
    if os.path.isfile(obj):
        os.remove(obj)
    elif os.path.isdir(obj):
        shutil.rmtree(obj)
    else:
        print("Undefined object:", obj)

