# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import importlib.util
import zipfile
from threading import Thread

from utils import constant


def start_thread(target, args: tuple = (), name: str = None):
    """Start the new thread and return it"""
    if isinstance(target, Thread):
        thread = target
    else:
        thread = Thread(target=target, args=args, name=name)
    thread.setDaemon(True)
    thread.start()
    return thread


def load_source(path, name=None):
    """Load python file"""
    if name is None:
        name = path.replace('/', '_').replace('\\', '_').replace('.', '_')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def list_file(folder, suffix):
    """Return file list in folder if file suffix is suffix"""
    file_list = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path) and file_path.endswith(suffix):
            file_list.append(file_path)
    return file_list


def remove_suffix(name: str):
    """Remove path suffix"""
    return re.sub(r'\.((?!\.).)*$', '', name)


def change_suffix(name: str, suffix: str):
    """Change or path suffix"""
    return remove_suffix(name) + suffix


def change_file_suffix(path: str, suffix: str):
    """Change file suffix and rename"""
    if os.path.isfile(path):
        os.rename(path, change_suffix(path, suffix))


def format_file_path(name: str, suffix: str, folder=None):
    if name.endswith(suffix):
        name = name
    else:
        name = change_suffix(name, suffix)
    if folder is not None:
        return os.path.join(folder, name)
    else:
        return name


def touch_folder(folder_name: str) -> bool:
    """Create folder if folder is not exist"""
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
        return False
    else:
        return True


def backup_log(logging_file: str) -> None:
    """Backup the old log file"""
    if os.path.isfile(logging_file):
        modify_time = time.strftime(
            '%Y-%m-%d',
            time.localtime(os.stat(logging_file).st_mtime)
        )
        count = 0
        while True:
            count += 1
            zip_file_name = os.path.join(constant.LOG_FOLDER,
                                         f'{modify_time}-{count}.zip')
            if not os.path.isfile(zip_file_name):
                break
        with zipfile.ZipFile(zip_file_name, 'w') as z:
            z.write(logging_file, arcname=os.path.basename(logging_file),
                    compress_type=zipfile.ZIP_DEFLATED)
        os.remove(logging_file)
