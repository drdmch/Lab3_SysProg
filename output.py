def div(a, b):
    if type(a) == int and type(b) == int:
        return int(a / b)
    return a / b


def mod(a, b):
    return a - int(a / b) * b


def to_str(v):
    if v is True:
        return '1'
    if v is False:
        return '0'
    if type(v) == float:
        return '%g' % v
    return str(v)


def fib(n):
    if (n < 2):
        return n
    return (fib((n - 1)) + fib((n - 2)))


def main():
    i = int(0)
    while (i < 10):
        print(to_str(fib(i)) + ' ', end='')
        i += 1
    print('\n', end='')
    return 0


if __name__ == '__main__':
    main()
