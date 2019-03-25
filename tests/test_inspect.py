import inspect
def get_current_function_name():
    print(inspect.stack())
    return inspect.stack()[1][3]

class MyClass:
    def function_one(self):
        print("%s.%s ******"%(self.__class__.__name__, get_current_function_name()))
if __name__ == "__main__":
    myclass = MyClass()
    myclass.function_one()


