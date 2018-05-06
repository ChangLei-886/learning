#encoding: utf-8

import string, random
from primeiter import PrimeIters, MyIterator
from decorator import sub_process_log,catch_exception
import itertools
# capta = ''
# words=''.join((string.ascii_letters, string.digits))
# for i in range(6):
#     capta += random.choice(words)
# print(capta)
# s = raw_input("请输入验证码：")

# if s == capta:
#     print "Right"
# else:
#     print "Wrong"
# def sublog(func):
#     def wrapper(*args, **kwargs):
#         print('开始运行....')
#         func(*args, **kwargs)
#         print('运行结束....')
#     return wrapper

@sub_process_log(subname='test')
@catch_exception
def test():
    a = '1' + 2
    print ('测试方法')

def user_range(start=0, end=0):
    value = start
    while True:
        if value >= end:
            break
        receive = yield value

        value += 1


if __name__ == '__main__':
    # primeIters = PrimeIters(5)
    # while True:
    #     print("素数：")
    #     print(primeIters.__next__())
    # for i in itertools.count(1,3):
    #     print i
    #     if i >= 20:
    #         break
    # print list(itertools.permutations([1,2,3,4,5], 2))
    # print list(itertools.combinations([1,2,3,4,5], 2))
    # test()
    # print "test"
    gen = user_range(1, 5)
    print type(gen)
    while True:
        print next(gen)
