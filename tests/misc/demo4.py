

class A:

    a = 1

    def __init__(self):
        self.aaa = 333

    def __setattr__(self, name, value):
        print(name, value)
        super().__setattr__(name, value)

    def __getattr__(self, name):
        # 在获取不到属性的时候会触发
        print(name)

    def __getattribute__(self, name):
        # 属性拦截器，可能会触发无限递归
        print(name)
        pass

a = A()
a.a = 3
print(a.a)