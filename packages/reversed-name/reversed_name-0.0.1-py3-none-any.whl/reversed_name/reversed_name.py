
def reversed_name():

    name = input('What is your name?: ')
    result = [None] * len(name)
    for n, i in enumerate(name):
        result[-(n + 1)] = i
    result = ''.join(result)
    return f'Hello, {result}'


print(reversed_name())