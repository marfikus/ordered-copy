
import os
import shutil


path1 = "file1.txt"
path2 = "file2.txt"
path3 = "f3.txt"

# mtime1 = os.path.getmtime(path1)
# mtime2 = os.path.getmtime(path2)
# mtime3 = os.path.getmtime(path3)
# print(mtime1)
# print(mtime2)
# print(mtime3)

# print(mtime2 > mtime1)


src = "test/from/dir1"
dst = "test/to/dir1"

try:
    shutil.copytree(src, dst, dirs_exist_ok=True)
    # shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))
except OSError as e:
    print(e)
