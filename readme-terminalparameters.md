# 命令行传参

- [Python] 命令行传参(sys.argv)
```python
import sys

def hello(count, name):
    for _ in range(count):
        print(f'Hello, {name}!')

if __name__ == '__main__':
    try:
        count, name = int(sys.argv[1]), sys.argv[2]
        hello(count, name)
    except Exception as e:
        print(sys.argv)
        print(e)

"""
执行: python myscript.py 3 Revang
结果:
Hello, Revang!
Hello, Revang!
Hello, Revang!
"""
```

- [Python] 命令行传参(argparse)
```python
import argparse

def hello(count, name):
    for _ in range(count):
        print(f'Hello, {name}!')

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('--count', '-c', help='', type=int, default=1)
        parser.add_argument('--name', '-n', help='')
        args = parser.parse_args()
        hello(args.count, args.name)
    except Exception as e:
        print(e)

"""
执行: python myscript.py --count=3 --name=Revang
结果:
Hello, Revang!
Hello, Revang!
Hello, Revang!
"""
```

- [Python] 命令行传参(click)
```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    for _ in range(count):
        click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    hello()

"""
执行: python myscript.py --count=3 --name=Revang
结果:
Hello, Revang!
Hello, Revang!
Hello, Revang!
"""
```