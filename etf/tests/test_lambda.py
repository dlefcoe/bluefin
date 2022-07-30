'''

A lambda function is a small anonymous function.
A lambda function can take any number of arguments, but can only have one expression.


Syntax
lambda arguments : expression

'''


# small anonymous function x(a) that adds 5 to a number
x = lambda a : a+5

print( x(3) )

# small anonymous function y(a,b) that performs a square type operation
y = lambda a,b : (a^2) + (2*a*b) + (b^2)
print( y(1,2) )


# this looks very lambda like
def square_number(a,b): return (a^2) + (2*a*b) + (b^2)


print(square_number(1,2))


f = lambda x: x + 1
print(f(3))

def f(x): return(x+1) 
print(f(3))


print('lambda example')
print( (lambda x,y : x*y)(5,7) )
