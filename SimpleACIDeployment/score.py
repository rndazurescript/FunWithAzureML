def init():
    print("Hello")


def run(data):
    print("world")
    return([1, 2, 3, 4])


# The following code will run if we invoke this file directly from
# command line, e.g. python inference.py
if __name__ == '__main__':
    init()
    run([])
