
# there are lots of diffewrent options
from typing import List, Dict, Set, Any, Sequence, Tuple, Callable

x = 1
x = 'darren'


# this is how to hint type
x:int = 1
y: str = 'hello'


y = 1


print(type(y))


# example of function with params types and return type too
def add_numbers(a:int, b:int, c:int)-> int:
    return a + b + c

x = add_numbers(1, 2, 3)
print(x)


# example of function with params types and return type as none
def add_numbers(a:int, b:int, c:int)-> None:
    print(a + b + c)


add_numbers(1,2,3)


x:List = [1,2,3]

print(sum(x))

print(type(x))


vector = [1,2,3]

'''
in sumary is seems that typing might be useful in cases and type hinging might be helpful in general
however, it appears to be inconsistent with standard python and rather verbose compared to 
other languages that are statically typed.

it is best to stick with python dynamic types and type hints

'''

x = 2
y = '2'

print(x + int(y) )

