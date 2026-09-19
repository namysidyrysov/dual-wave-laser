
class MBL1500A:
    def __init__(self, serial_port="COM7"):
        print('CurrentController inited!')

    def set_current(self, current):
        print(f'Set current: {current}A')

   