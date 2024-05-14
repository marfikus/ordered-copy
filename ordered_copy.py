import os
import shutil
import configparser
import ast


PROGRAM_VERSION = "1.1.1"

CONFIG_FILE = "ordered_copy.ini"
DEFAULT_CONFIG = {
    # "list_of_tasks": [[r"test/from", r"test/to", "dd"], [r"test/a", r"test/to/a", "dd"]],
    "list_of_tasks": [],
    "list_of_ignored_paths": [],
    "pause_before_exit": True,
    "debug_print": True,
}
config = {}

def load_config():
    global config

    def load_key(parser, key, type="str"):
        try:
            if type == "str":
                value = parser["DEFAULT"][key]
            elif type == "int":
                value = int(parser["DEFAULT"][key])
            elif type == "float":
                value = float(parser["DEFAULT"][key])
            elif type == "bool":
                value = bool(int(parser["DEFAULT"][key]))
            elif type == "list":
                value = ast.literal_eval(parser["DEFAULT"][key])
        except KeyError:
            print(f"No key '{key}' in config file! Loaded from DEFAULT_CONFIG")
            value = DEFAULT_CONFIG[key]

        return value


    if not os.path.exists(CONFIG_FILE):
        print("Config file not found! Loaded DEFAULT_CONFIG")
        config = DEFAULT_CONFIG
        return

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE, encoding="utf-8")

    config["list_of_tasks"] = load_key(parser, "list_of_tasks", "list")
    config["list_of_ignored_paths"] = load_key(parser, "list_of_ignored_paths", "list")
    config["pause_before_exit"] = load_key(parser, "pause_before_exit", "bool")
    config["debug_print"] = load_key(parser, "debug_print", "bool")


def debug_print(msg):
    if config["debug_print"]:
        print(msg)


def copy_with_replace_by_date(path_from, path_to, op_type, list_of_ignored_paths):
    status = "Ok"
    msg = ""
    copied_files = 0
    global task_errors
    
    if not os.path.exists(path_from):
        status = "Error!"
        msg = "Path 'from' not found: '{}'".format(path_from)
        return {"status": status, "msg": msg, "copied_files": copied_files}
        
    if path_from in list_of_ignored_paths:
        msg = "Path is ignored: '{}'".format(path_from)
        return {"status": status, "msg": msg, "copied_files": copied_files}
    
    if op_type == "ff":
        print("file-file")
        if not os.path.isfile(path_from):
            status = "Error!"
            msg = "Path 'from' is not a file: '{}'".format(path_from)
            return {"status": status, "msg": msg, "copied_files": copied_files}
            
        mtime_path_from = os.path.getmtime(path_from) 
            
        f_path_from = os.path.split(path_from)[0]
        f_path_to, f_name_to = os.path.split(path_to)

        if os.path.exists(path_to):
            if not os.path.isfile(path_to):
                status = "Error!"
                msg = "Path 'to' is not a file: '{}'".format(path_to)
                return {"status": status, "msg": msg, "copied_files": copied_files}
            
            mtime_path_to = os.path.getmtime(path_to)
            
            if mtime_path_from > mtime_path_to:
                print("file-file: rewrite")
                try:
                    shutil.copy2(path_from, path_to)
                    copied_files += 1
                    shutil.copystat(f_path_from, f_path_to)
                except OSError as err:
                    print(err)
                    status = "Error!"
                    msg = err
                    return {"status": status, "msg": msg, "copied_files": copied_files}
                   
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
                try:
                    # создаёт пустую копию дерева каталогов (вместе со stat, а файлы пропускаются):
                    shutil.copytree(f_path_from, f_path_to, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))
                except OSError as err:
                    print(err)
                    status = "Error!"
                    msg = err
                    return {"status": status, "msg": msg, "copied_files": copied_files}
                
            print("file-file: write")
            try:
                shutil.copy2(path_from, path_to)
                copied_files += 1
                shutil.copystat(f_path_from, f_path_to)
            except OSError as err:
                print(err)
                status = "Error!"
                msg = err
                return {"status": status, "msg": msg, "copied_files": copied_files}
    
    elif op_type == "fd":
        print("file-dir")
        if not os.path.isfile(path_from):
            status = "Error!"
            msg = "Path 'from' is not a file: '{}'".format(path_from)
            return {"status": status, "msg": msg, "copied_files": copied_files}
            
        mtime_path_from = os.path.getmtime(path_from)        
        
        file_name = os.path.basename(path_from)
        path_to_new = os.path.join(path_to, file_name)
        path_to_new = os.path.normpath(path_to_new)
        
        f_path_from = os.path.split(path_from)[0]

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
            
                mtime_path_to_new = os.path.getmtime(path_to_new)
                
                if mtime_path_from > mtime_path_to_new:
                    print("file-dir: rewrite")
                    try:
                        shutil.copy2(path_from, path_to_new)
                        copied_files += 1
                        shutil.copystat(f_path_from, path_to)
                    except OSError as err:
                        print(err)
                        status = "Error!"
                        msg = err
                        return {"status": status, "msg": msg, "copied_files": copied_files}
                    
            else:
                print("file-dir: write")
                try:
                    shutil.copy2(path_from, path_to_new)
                    copied_files += 1
                    shutil.copystat(f_path_from, path_to)
                except OSError as err:
                    print(err)
                    status = "Error!"
                    msg = err
                    return {"status": status, "msg": msg, "copied_files": copied_files}

        else:
            print("Create path: ", path_to)
            try:
                # создаёт пустую копию дерева каталогов (вместе со stat, а файлы пропускаются):
                shutil.copytree(f_path_from, path_to, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))
            except OSError as err:
                print(err)
                status = "Error!"
                msg = err
                return {"status": status, "msg": msg, "copied_files": copied_files}

            print("file-dir: write")
            try:
                shutil.copy2(path_from, path_to)
                copied_files += 1
                shutil.copystat(f_path_from, path_to)
            except OSError as err:
                print(err)
                status = "Error!"
                msg = err
                return {"status": status, "msg": msg, "copied_files": copied_files}
        
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
        
        len_objects = len(list_path_from)
        if len_objects == 0:
            if not os.path.exists(path_to):
                print("Empty folder. Create path: ", path_to)
                try:
                    # создаёт пустую копию дерева каталогов (вместе со stat, а файлы пропускаются):
                    shutil.copytree(path_from, path_to, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*"))
                except OSError as err:
                    print(err)
                    status = "Error!"
                    msg = err
                    return {"status": status, "msg": msg, "copied_files": copied_files}
        
        cur_obj = 1
        for obj in list_path_from:
            print("Object {0} of {1}:".format(cur_obj, len_objects))
            path_from_obj = os.path.join(path_from, obj)
            path_from_obj = os.path.normpath(path_from_obj)

            # if the file was deleted during directory copying
            if not os.path.exists(path_from_obj):
                status = "Error!"
                msg = "Path not found: '{}'".format(path_from_obj)
                res = {"status": status, "msg": msg, "copied_files": 0, "tag": "fake return"}
                task_errors.append(res)
                cur_obj += 1
                continue 
                # just skipped this file but didn't stop the task

            if os.path.isfile(path_from_obj):
                print("obj: {} (file)".format(obj))
                res = copy_with_replace_by_date(path_from_obj, path_to, "fd", list_of_ignored_paths)
                print(res)
                copied_files += res["copied_files"]
                if res["status"] == "Error!":
                    task_errors.append(res)
                else:
                    f_path_from = os.path.split(path_from_obj)[0]
                    try:
                        shutil.copystat(f_path_from, path_to)
                    except OSError as err:
                        print(err)
                        status = "Error!"
                        msg = err
                        return {"status": status, "msg": msg, "copied_files": copied_files}

            elif os.path.isdir(path_from_obj):
                print("obj: {} (dir)".format(obj))
                path_to_obj = os.path.join(path_to, obj)
                path_to_obj = os.path.normpath(path_to_obj)
                res = copy_with_replace_by_date(path_from_obj, path_to_obj, "dd", list_of_ignored_paths)
                print(res)
                copied_files += res["copied_files"]
                if res["status"] == "Error!":
                    task_errors.append(res)
                else:
                    try:
                        shutil.copystat(path_from_obj, path_to_obj)
                    except OSError as err:
                        print(err)
                        status = "Error!"
                        msg = err
                        return {"status": status, "msg": msg, "copied_files": copied_files}

            else:
                status = "Error!"
                msg = "The object is not supported: '{}'".format(path_from_obj)
                res = {"status": status, "msg": msg, "copied_files": 0, "tag": "fake return"}
                task_errors.append(res)
                # just skipped this file but didn't stop the task
                
            cur_obj += 1
            print("-----------------------------------------------")

        try:
            shutil.copystat(path_from, path_to)
        except OSError as err:
            print(err)
            status = "Error!"
            msg = err
            return {"status": status, "msg": msg, "copied_files": copied_files}

    else:
        status = "Error!"
        msg = "Operation type is undefined: '{}'".format(op_type)
        return {"status": status, "msg": msg, "copied_files": copied_files}
            
    return {"status": status, "msg": msg, "copied_files": copied_files}


def main():
    print(f"Program version: {PROGRAM_VERSION}")
    load_config()
    print(f"Current configuration: \n{config}")

    # abs_path_from = os.path.abspath(config["path_from"])
    # abs_path_to = os.path.abspath(config["path_to"])
    # debug_print(abs_path_from)
    # debug_print(abs_path_to)

    task_errors = []
    general_report = []

    sum_copied_files = 0
    cur_task = 1
    len_tasks = len(config["list_of_tasks"])
    for i in config["list_of_tasks"]:
        print("===============================================")
        print("Task {0} of {1}:".format(cur_task, len_tasks))
        print(i)
        res = copy_with_replace_by_date(i[0], i[1], i[2], config["list_of_ignored_paths"])
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

    if config["pause_before_exit"]:
        input("Press Enter to end the program...")


if __name__ == "__main__":
    main()

