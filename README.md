
# Ordered Copy

Утилита для копирования файлов и каталогов вместе и их метаинформацией (дата создания, изменения и тд). В итоге, например, при сортировке скопированной структуры по дате изменения, она будет выглядеть аналогично исходной.

За основу был взят [скрипт бэкапа](https://github.com/marfikus/smartphone-backup), из которого убрал лишнее и добавил копирование метаданных.

Конфигурация утилиты выполняется в файле **ordered_copy.ini**.  
Параметры файла конфигурации:  
`list_of_tasks` - список списков определённой структуры, объединённых в квадратные скобки.  
Пример: `[[r"C:\Users\Username\Pictures", r"D:\Изображения_архив", "dd"]]`  
Список задач для копирования. Синтаксис задачи: `[path_from, path_to, op_type]` , где:
* `path_from` - исходный путь (откуда копировать)
* `path_to` - путь назначения (куда копировать)
* `op_type` - тип копирования. Возможные значения:
    * `"ff"`: исходный путь - файл, путь назначения - файл
    * `"fd"`: исходный путь - файл, путь назначения - каталог
    * `"df"`: исходный путь - каталог, путь назначения - файл (прикол)
    * `"dd"`: исходный путь - каталог, путь назначения - каталог

`list_of_ignored_paths` - список строк в кавычках, объединённых в квадратные скобки.  
Пример: `[r"C:\Users\Username\Pictures\desktop.ini"]`  
Список путей, которые будут игнорироваться, то есть пропускаться программой.

`pause_before_exit` - целое число (1 или 0). Пауза перед завершением работы программы. 1 - включено, 0 - выключено.  
`debug_print` - целое число (1 или 0). Вывод различной отладочной информации в консоль. 1 - включено, 0 - выключено.

Скачать EXE-файл утилиты можно [здесь](https://github.com/marfikus/ordered-copy/releases/). Собирал через [Auto PY to EXE](https://pypi.org/project/auto-py-to-exe/).
