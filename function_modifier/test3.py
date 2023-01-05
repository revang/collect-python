from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print('log开始...',func.__name__)
        func(*args,**kwargs)
        print('log结束...')
    return wrapper

@log
def test1(s):
    print('test1...',s)
    return s

def test2(s1,s2):
    print('test2...',s1,s2)
    return s1+s2

print(test1('a'))
print(test2('b','c'))

