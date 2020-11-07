def log(func):
    def wrapper():
        print('log开始...')
        func()
        print('log结束...')
    return wrapper

@log
def test():
    print('test...')

test()
