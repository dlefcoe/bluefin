'''
example to convert string to a raw string

'''




some_string = r'hello\u person'

print(some_string)


raw_string = some_string.encode('unicode_escape')
print(raw_string)

