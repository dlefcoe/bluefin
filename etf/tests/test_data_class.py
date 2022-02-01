

'''

Python DATA CLASSES


This module provides a decorator and functions for automatically adding generated special methods such as __init__() and __repr__() to user-defined classes.

official link:
    https://docs.python.org/3/library/dataclasses.html


'''



from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return round(self.unit_price * self.quantity_on_hand, 2)


item = InventoryItem('toilet', 149.99, 35)

print(item)

y = item.total_cost()
print(y)
print(y * 1_000_000_000_000)




# fields may optionally specify a default value, using normal Python syntax:

@dataclass
class C:
    a: int       # 'a' has no default value
    b: int = 0   # assign a default value for 'b'


c = C(100)

print(c)



# old method of class requires def __innit__(self) method.

class D:
    def __init__(self, a, b=None) -> None:
        self.a = a
        self.b = b
        pass



d = D(100)
print(d.a)
print(d.b)




