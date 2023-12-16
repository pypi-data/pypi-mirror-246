from time import sleep

from horology import timed


@timed
def foo():
    print('foo starts')
    sleep(1)
    print('foo will raise')
    raise RuntimeError('An error occurred')


if __name__ == '__main__':
    foo()