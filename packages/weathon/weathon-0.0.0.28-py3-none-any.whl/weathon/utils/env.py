import os


def get_env(key):
    """
    根据key 获取环境变量中的值
    """
    return os.environ.get(key)
