from lib.file_saver import FileSaver

random_json = {
    "lol": "aaa"
}

fs = FileSaver()

fs.save_file("12321", random_json)
