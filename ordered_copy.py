import os
import shutil
import time
import configparser


PROGRAM_VERSION = "1.0.1"

CONFIG_FILE = "ordered_copy.ini"
DEFAULT_CONFIG = {
    "path_from": "",
    "path_to": "",
    "use_copytree": True,
    "pause_between_copy": 1.0,
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

    config["path_from"] = load_key(parser, "path_from")
    config["path_to"] = load_key(parser, "path_to")
    config["use_copytree"] = load_key(parser, "use_copytree", "bool")
    config["pause_between_copy"] = load_key(parser, "pause_between_copy", "float")
    config["debug_print"] = load_key(parser, "debug_print", "bool")


def debug_print(msg):
    if config["debug_print"]:
        print(msg)


def ordered_copy_my(path_from, path_to, pause_between_copy=1.0):

    def get_mtime(i):
        path = os.path.join(path_from, i)
        path = os.path.normpath(path)
        return os.path.getmtime(path)


    dir_list = os.listdir(path_from)
    # dir_list.sort(key=get_mtime)

    for i in dir_list:
        obj_path = os.path.join(path_from, i)
        obj_path = os.path.normpath(obj_path)

        if os.path.isfile(obj_path):
            debug_print(f"'{i}' is file")
            shutil.copy2(obj_path, path_to)
        elif os.path.isdir(obj_path):
            debug_print(f"'{i}' is dir")
            dir_path = os.path.join(path_to, i)
            dir_path = os.path.normpath(dir_path)
            try:
                os.mkdir(dir_path)
                # shutil.copystat(obj_path, dir_path) # возможно это надо делать после заполнения каталога
            except FileExistsError as e:
                print(e)
            ordered_copy_my(obj_path, dir_path, pause_between_copy)
            shutil.copystat(obj_path, dir_path)

        # time.sleep(pause_between_copy)


def ordered_copy_copytree(path_from, path_to):
    shutil.copytree(path_from, path_to, dirs_exist_ok=True)


def main():
    print(f"Program version: {PROGRAM_VERSION}")
    load_config()
    print(f"Current configuration: \n{config}")

    if config["path_from"].strip() == "":
        print("'path_from' is empty!")
        return
    if config["path_to"].strip() == "":
        print("'path_to' is empty!")
        return

    abs_path_from = os.path.abspath(config["path_from"])
    abs_path_to = os.path.abspath(config["path_to"])
    debug_print(abs_path_from)
    debug_print(abs_path_to)

    if not os.path.exists(abs_path_from):
        print("'path_from' is not exists!")
        return
    if not os.path.exists(abs_path_to):
        print("'path_to' is not exists!")
        return

    if abs_path_from == abs_path_to:
        print("'path_from' == 'path_to'!")
        return

    if config["use_copytree"]:
        ordered_copy_copytree(
            abs_path_from, 
            abs_path_to
        )
    else:
        ordered_copy_my(
            abs_path_from, 
            abs_path_to, 
            config["pause_between_copy"]
        )


if __name__ == "__main__":
    main()

