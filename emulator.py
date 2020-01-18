from core import Flag, Register

class Machine:
    def __init__(self):
        self.registers = [ 0 for _ in Register ]
        self.flags = [ 0 for _ in Flag ]

    def add_register(self, src, dest):
        pass

if __name__ == "__main__":
    m = Machine()
