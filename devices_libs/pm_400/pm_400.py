import pyvisa
import time

class Pm400():
    def __init__(self, wl, device_name = 'USB0::0x1313::0x8075::P5001126::INSTR'):
        self.rm = pyvisa.ResourceManager()
        try:
            self.pm = self.rm.open_resource(device_name)
            print(self.__class__.__name__, 'initialized!')
            self.set_wl(wl=wl) 
            
        except Exception as e:
            print(e)
            print(self.__class__.__name__, 'no found!')    
            exit(0)

    
    def disconnect(self):
        """ Отключить соединение"""
        self.pm.control_ren(False)
        self.pm.close()
        self.rm.close()
        print(self.__class__.__name__, 'disconnect!')

    def get_power(self):
        power = float(self.pm.query('measure:power?'))
        # Переводим в mW и округляем до 4 знаков после запятой
        return round(power * 1e3, 4)

    def set_wl(self, wl = 1070):
        self.pm.write(f'SENS:CORR:WAV {wl}')
        time.sleep(0.2)
        return wl
    
    def get_wl(self):
        """Запросить текущую длину волны с прибора для проверки"""
        return float(self.pm.query('SENS:CORR:WAV?'))




if __name__ == "__main__":
    pm_device=Pm400(wl=1240)
    print(f'Power = {pm_device.get_power()} mW')