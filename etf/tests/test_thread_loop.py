'''

example of two functions that recursively call themselves in threaded loops

'''

import time
import threading



def main():

    loop_thread(3)
    second_loop(3)

    return


def loop_thread(loop_seconds):
    print('hello world')
    threading.Timer(interval=loop_seconds, function=loop_thread, args=[3]).start()
    return


def second_loop(loop_seconds):
    print('alright...')
    threading.Timer(interval=loop_seconds, function=second_loop, args=[5]).start()
    return


if __name__=='__main__':
    # run if main
    main()