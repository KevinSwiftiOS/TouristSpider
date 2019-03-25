
def b(fun=123):
    print(fun)

def a(fun=None,**kwargs):
    fun(**kwargs)

a(b,345)