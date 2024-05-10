
# import yadisk
import os
# import datetime
# from dateutil.tz import tzutc
import shutil
import my_input_data as mid
# import connect_data
# import posixpath
# import pickle

# tzutc = tzutc()
# local_db = {}
# file_name_local_db = "local_db"

    
def copy_with_replace_by_date(path_from, path_to, op_type, set_of_ignored_paths):
    status = "Ok"
    msg = ""
    copied_files = 0
    global task_errors
    
    if not os.path.exists(path_from):
        status = "Error!"
        msg = "Path 'from' not found: '{}'".format(path_from)
        return {"status": status, "msg": msg, "copied_files": copied_files}
        
    if path_from in set_of_ignored_paths:
        msg = "Path is ignored: '{}'".format(path_from)
        return {"status": status, "msg": msg, "copied_files": copied_files}
    
    if op_type == "ff":
        print("file-file")
        if not os.path.isfile(path_from):
            status = "Error!"
            msg = "Path 'from' is not a file: '{}'".format(path_from)
            return {"status": status, "msg": msg, "copied_files": copied_files}
            
        mtime_path_from = os.path.getmtime(path_from)
        # mtime_path_from = datetime.datetime.fromtimestamp(mtime_path_from)
        # mtime_path_from = mtime_path_from.astimezone(tzutc)
            
        # if check_file_in_local_db(path_from, mtime_path_from):
        #     msg = "File skipped: '{}'".format(path_from)
        #     return {"status": status, "msg": msg, "copied_files": copied_files}     
            
        f_path_from = os.path.split(path_from)[0]
        f_path_to, f_name_to = os.path.split(path_to)

        if os.path.exists(path_to):
            if not os.path.isfile(path_to):
                status = "Error!"
                msg = "Path 'to' is not a file: '{}'".format(path_to)
                return {"status": status, "msg": msg, "copied_files": copied_files}
            
            # mtime_path_to = y.get_meta(path_to, fields={"modified"})["modified"]
            # mtime_path_to = mtime_path_to.astimezone(tzutc)
            mtime_path_to = os.path.getmtime(path_to)
            # print(mtime_path_to)
            
            if mtime_path_from > mtime_path_to:
                print("file-file: rewrite")
                shutil.copy2(path_from, path_to)
                # y.upload(path_from, path_to, overwrite=True)
                copied_files += 1
                shutil.copystat(f_path_from, f_path_to)
                
            # write_file_to_local_db(path_from, mtime_path_from)
            # if 'local_db' is empty(lost or irrelevant), but files in 'path_to' is exists          
        else:
            if f_name_to == "": # for example, if path_to = 'dir1\dir2\'
                status = "Error!"
                msg = "Path 'to' is incorrect: '{}'".format(path_to)
                return {"status": status, "msg": msg, "copied_files": copied_files}
            
            if os.path.exists(f_path_to):
                if not os.path.isdir(f_path_to):
                    status = "Error!"
                    msg = "Path: '{0}' is not a directory to write file: '{1}'. \n(May be '{2}' it is already existing file?)".format(f_path_to, f_name_to, os.path.basename(f_path_to))
                    return {"status": status, "msg": msg, "copied_files": copied_files}
            else:
                print("Create path: ", f_path_to)
                # создаёт пустую копию дерева каталогов (вместе со stat, а файлы пропускаются):
                shutil.copytree(f_path_from, f_path_to, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))

                # os.makedirs(f_path_to)
                # y.mkdir(f_path_to)
                # make_dirs_yadisk(f_path_to)
                
            print("file-file: write")
            shutil.copy2(path_from, path_to)
            # shutil.copytree(path_from, path_to, dirs_exist_ok=True)
            # y.upload(path_from, path_to)
            copied_files += 1
            shutil.copystat(f_path_from, f_path_to)
            # write_file_to_local_db(path_from, mtime_path_from)
    
    elif op_type == "fd":
        print("file-dir")
        if not os.path.isfile(path_from):
            status = "Error!"
            msg = "Path 'from' is not a file: '{}'".format(path_from)
            return {"status": status, "msg": msg, "copied_files": copied_files}
            
        mtime_path_from = os.path.getmtime(path_from)
        # mtime_path_from = datetime.datetime.fromtimestamp(mtime_path_from)
        # mtime_path_from = mtime_path_from.astimezone(tzutc)
        
        # if check_file_in_local_db(path_from, mtime_path_from):
        #     msg = "File skipped: '{}'".format(path_from)
        #     return {"status": status, "msg": msg, "copied_files": copied_files}         
        
        file_name = os.path.basename(path_from)
        path_to_new = os.path.join(path_to, file_name)
        path_to_new = os.path.normpath(path_to_new)
        # print(path_to_new)
        
        f_path_from = os.path.split(path_from)[0]
        # print("f_path_from:", f_path_from)

        if os.path.exists(path_to):
            if not os.path.isdir(path_to):
                status = "Error!"
                msg = "Path 'to' is not a directory: '{}'".format(path_to)
                return {"status": status, "msg": msg, "copied_files": copied_files}
            
            if os.path.exists(path_to_new):
                if not os.path.isfile(path_to_new):
                    status = "Error!"
                    msg = "Path 'to' is not a file: '{}'".format(path_to_new)
                    return {"status": status, "msg": msg, "copied_files": copied_files}
            
                # mtime_path_to_new = y.get_meta(path_to_new, fields={"modified"})["modified"]
                # mtime_path_to_new = mtime_path_to_new.astimezone(tzutc)
                mtime_path_to_new = os.path.getmtime(path_to_new)
                
                if mtime_path_from > mtime_path_to_new:
                    print("file-dir: rewrite")
                    shutil.copy2(path_from, path_to_new)
                    # y.upload(path_from, path_to_new, overwrite=True, timeout=120.0)
                    copied_files += 1
                    # write_file_to_local_db(path_from, mtime_path_from)
                    shutil.copystat(f_path_from, path_to)
                    
                # write_file_to_local_db(path_from, mtime_path_from)
                # if 'local_db' is empty(lost or irrelevant), but files in 'path_to' is exists
            else:
                print("file-dir: write")
                shutil.copy2(path_from, path_to_new)
                # y.upload(path_from, path_to_new, timeout=120.0)
                copied_files += 1
                # write_file_to_local_db(path_from, mtime_path_from)
                shutil.copystat(f_path_from, path_to)
        else:
            # print("'path_to' not exists")
            print("Create path: ", path_to)

            print("f_path_from:", f_path_from)
            # создаёт пустую копию дерева каталогов (вместе со stat, а файлы пропускаются):
            shutil.copytree(f_path_from, path_to, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))

            # os.makedirs(path_to)
            # make_dirs_yadisk(path_to)
            print("file-dir: write")
            shutil.copy2(path_from, path_to)
            # y.upload(path_from, path_to_new, timeout=120.0)
            copied_files += 1
            # write_file_to_local_db(path_from, mtime_path_from)
            shutil.copystat(f_path_from, path_to)
        
    elif op_type == "df":
        print("dir-file")
        status = "Error!"
        msg = "Write directory to file? Are you really? It doesn't make sense. =)"
        return {"status": status, "msg": msg, "copied_files": copied_files}
        
    elif op_type == "dd":
        print("dir-dir")
        if not os.path.isdir(path_from):
            status = "Error!"
            msg = "Path 'from' is not a directory: '{}'".format(path_from)
            return {"status": status, "msg": msg, "copied_files": copied_files}

        list_path_from = os.listdir(path_from)
        # print("list_path_from: ", list_path_from)
        # print("len(list_path_from): ", len(list_path_from))
        
        len_objects = len(list_path_from)
        if len_objects == 0:
            # print("path_to: ", path_to)
            if not os.path.exists(path_to):
                print("Empty folder. Create path: ", path_to)
                # os.makedirs(path_to)
                # make_dirs_yadisk(path_to)
                # создаёт пустую копию дерева каталогов (вместе со stat, а файлы пропускаются):
                shutil.copytree(path_from, path_to, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))
        
        cur_obj = 1
        for obj in list_path_from:
            print("Object {0} of {1}:".format(cur_obj, len_objects))
            # print("obj: ", obj)
            path_from_obj = os.path.join(path_from, obj)
            path_from_obj = os.path.normpath(path_from_obj)

            # if the file was deleted during directory copying
            if not os.path.exists(path_from_obj):
                res = {"status": "Error!", "msg": "Path not found: '{}'".format(path_from_obj), "copied_files": 0, "tag": "fake return"}
                task_errors.append(res)
                cur_obj += 1
                continue 
                # just skipped this file but didn't stop the task

            if os.path.isfile(path_from_obj):
                print("obj: {} (file)".format(obj))
                res = copy_with_replace_by_date(path_from_obj, path_to, "fd", set_of_ignored_paths)
                print(res)
                copied_files += res["copied_files"]
                if res["status"] == "Error!":
                    task_errors.append(res)
                else:
                    f_path_from = os.path.split(path_from_obj)[0]
                    shutil.copystat(f_path_from, path_to)

            elif os.path.isdir(path_from_obj):
                print("obj: {} (dir)".format(obj))
                path_to_obj = os.path.join(path_to, obj)
                path_to_obj = os.path.normpath(path_to_obj)
                res = copy_with_replace_by_date(path_from_obj, path_to_obj, "dd", set_of_ignored_paths)
                print(res)
                copied_files += res["copied_files"]
                if res["status"] == "Error!":
                    task_errors.append(res)
                else:
                    shutil.copystat(path_from_obj, path_to_obj)
                    print("copystat:", path_from_obj, path_to_obj)
            else:
                res = {"status": "Error!", "msg": "The object is not supported: '{}'".format(path_from_obj), "copied_files": 0, "tag": "fake return"}
                task_errors.append(res)
                # just skipped this file but didn't stop the task
                
            cur_obj += 1
            print("-----------------------------------------------")

        shutil.copystat(path_from, path_to)
        print("copystat:", path_from, path_to)

    else:
        status = "Error!"
        msg = "Operation type is undefined: '{}'".format(op_type)
        return {"status": status, "msg": msg, "copied_files": copied_files}
            
    return {"status": status, "msg": msg, "copied_files": copied_files}

    
# y = yadisk.YaDisk(token=connect_data.token)

# if not y.check_token():
#     print("Token is False!")
#     quit()

task_errors = []
general_report = []

sum_copied_files = 0
cur_task = 1
len_tasks = len(mid.list_of_tasks)
for i in mid.list_of_tasks:
    print("===============================================")
    print("Task {0} of {1}:".format(cur_task, len_tasks))
    print(i)
    res = copy_with_replace_by_date(i[0], i[1], i[2], mid.set_of_ignored_paths)
    print(res)
    sum_copied_files += res["copied_files"]
    general_report.append([i, res, task_errors.copy()])
    task_errors.clear()
    cur_task += 1
    print("===============================================")
    
print("\nGeneral report:")
for i in general_report:
    print("===============================================")
    print("Task:", i[0])
    print("Result:", i[1])
    error_count = len(i[2])
    print("Internal errors:", error_count)
    if error_count > 0:
        for j in i[2]:
            print(j)
    print("===============================================")
print("Total files copied:",  sum_copied_files)
    
