import contextlib
import os


@contextlib.contextmanager
def cd_into_folder(folder_path):
    orignal_dir = os.getcwd()
    os.chdir(folder_path)
    yield
    os.chdir(orignal_dir)
