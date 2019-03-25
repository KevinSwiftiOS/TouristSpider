class A(object):

    def __init__(self):
        self.a = 1
        self.b = 2

    def test(self):
        for i, j in vars(self).items():
            print(j)


a = A()
a.test()