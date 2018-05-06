#encoding:utf-8
from common import isprime
class PrimeIters(object):
    def __init__(self, max):
        self.max = max
        self.n = 0
    def __iter_(self):
        return self
    def __next__(self):
        while True:
            self.n += 1
            if self.n == 1:
                self.prime = self.n
                return self.prime
            if self.n <= self.max:
                if isprime(self.n):
                    self.prime = self.n
                    return self.prime
        raise StopIteration
class MyIterator:
    def __init__(self, x=2, xmax=100):
        self.__mul, self.__x = x,x
        self.__xmax = xmax
    def __iter__(self):
        return self
    def __next__(self):
        if self.__x and self.__x != 1:
            self.__mul *= self.__x
            if self.__mul <= self.__xmax:
                return self.__mul
            else:
                raise StopIteration
        else:
            raise StopIteration
