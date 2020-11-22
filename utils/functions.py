# -*- coding: utf-8 -*-
import os
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


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    if size < (2 ** 10):
        return f'{round(size, 2)} B'
    if size < (2 ** 20):
        return f'{round(size / (2 ** 10), 2)} KB'
    else:
        return f'{round(size / (2 ** 20), 2)} MB'


def get_file_modify_time(file_path):
    return time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime(os.path.getmtime(file_path))
    )


def list_file(folder, suffix):
    """Return file list in folder if file suffix is suffix"""
    file_list = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path) and file_path.endswith(suffix):
            file_list.append(file_path)
    return file_list


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
            time.localtime(os.path.getmtime(logging_file))
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
