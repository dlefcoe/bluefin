import time
import threading

# globals
x = {'yo':100, 'hello':'a'}


def main():
    thr_1 = threading.Thread(target=some_func, args=[x['yo'],2])
    thr_2 = threading.Thread(target=another_func, args=[3,4])
    thr_1.start()
    thr_2.start()
    return


def some_func(a, b):
    print('invoking function 1...')
    print(f'this is x: {x["yo"]}...')
    time.sleep(3)
    y = a + b
    print(f'this is x: {x["yo"]}...')
    print(f'finishing function 1...sum={y}...')
    y = x['yo'] + b
    print(f'finishing function 1...sum={y}...')    
    y = a + b
    print(f'finishing function 1...sum={y}...')    
    return y


def another_func(a, b):
    print('invoking function 2...')
    y = a - b
    x['yo'] = 1000
    print(f'finishing function 2...sum={y}...')
    return y


if __name__=='__main__':
    # run if main
    main()