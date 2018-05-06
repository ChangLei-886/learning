#encoding: utf-8
import traceback

# 方法调用启动与结束LOG打印
def sub_process_log(subname='test'):
    def wrapper(func):
        def sub_wrapper(*args, **kwargs):
            print('<%s>开始运行....' % subname)
            func(*args, **kwargs)
            print('<%s>运行结束....' % subname)
        return sub_wrapper
    return wrapper

def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            traceback.print_exc()
    return wrapper

