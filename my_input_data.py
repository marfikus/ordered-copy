
list_of_tasks = [
# structure hint: [path_from, path_to, op_type("ff"|"fd"|"df"|"dd")]
# [r"test_dir_from\ddd\11", r"/Applications/smartphone_backup/ddd", "dd"],
# [r"myfile.txt", r"/Applications/smartphone_backup/ddd/myfile.txt", "ff"],

    [r"test/from", r"test/to", "dd"],
    # [r"test/d1", r"test/to/d1", "dd"],
    [r"test/a", r"test/to/a", "dd"],
    # [r"test/from/dir1/doc1.txt", r"test/to/dir1/doc1.txt", "ff"],
    # [r"test/from/dir1/doc2.txt", r"test/to/dir1/doc2.txt", "ff"],
 
# [r"/storage/sdcard0/fastnote", r"/Applications/smartphone_backup/from_dexp_xl_145/fastnote", "dd"],
# [r"/storage/sdcard0/documents/iA Writer", r"/Applications/smartphone_backup/from_dexp_xl_145/iA_Writer", "dd"],
# [r"/storage/sdcard0/Recording", r"/Applications/smartphone_backup/from_dexp_xl_145/Recording", "dd"],
# [r"/storage/sdcard0/DCIM/Camera", r"/Applications/smartphone_backup/from_dexp_xl_145/DCIM_Camera", "dd"],
# [r"/storage/sdcard0/Pictures", r"/Applications/smartphone_backup/from_dexp_xl_145/Pictures", "dd"],
# [r"/storage/sdcard0/Work/work_memo", r"/Applications/smartphone_backup/from_dexp_xl_145/Work/work_memo", "dd"],
# [r"/storage/sdcard0/Work/к_экзаменам", r"/Applications/smartphone_backup/from_dexp_xl_145/Work/к_экзаменам", "dd"],
# [r"/storage/sdcard0/python_scripts", r"/Applications/smartphone_backup/from_dexp_xl_145/python_scripts", "dd"]
]

set_of_ignored_paths = {
# structure hint: path_from
# r"ddd\11\ttt",
# r"ddd\11\myfile_10.txt",

# r"/storage/sdcard0/fastnote/.Trash",
# r"/storage/sdcard0/DCIM/Camera/.dthumb",
# r"/storage/sdcard0/python_scripts/__pycache__",
# r"/storage/sdcard0/python_scripts/download_radio_t/__pycache__",
# r"/storage/sdcard0/python_scripts/smartphone_backup/__pycache__",
# r"/storage/sdcard0/python_scripts/smartphone_backup/connect_data.py",
# r"/storage/sdcard0/python_scripts/smartphone_backup/get_token.py",
}


# xcopy "I:\data\colornote\backup\*.*" "D:\from_dexp_xl_145\colornote\backup\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\DCIM\Camera\*.*" "D:\from_dexp_xl_145\DCIM_Camera\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\dictdata\*.*" "D:\from_dexp_xl_145\dictdata\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\ExtractedApks\*.*" "D:\from_dexp_xl_145\ExtractedApks\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\fastnote\*.*" "D:\from_dexp_xl_145\fastnote\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\MapsWithMe\*.*" "D:\from_dexp_xl_145\MapsWithMe\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\MyDictionary\*.*" "D:\from_dexp_xl_145\MyDictionary\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\Pictures\*.*" "D:\from_dexp_xl_145\Pictures\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\Recording\*.*" "D:\from_dexp_xl_145\Recording\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\Work\*.*" "D:\Work(smart & pc)\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\python_scripts\*.*" "D:\from_dexp_xl_145\python_scripts\*.*" /F /H /R /K /Y /D /E
# xcopy "I:\documents\iA Writer\*.*" "D:\from_dexp_xl_145\iA Writer\*.*" /F /H /R /K /Y /D /E
