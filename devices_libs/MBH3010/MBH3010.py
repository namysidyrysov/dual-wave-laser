import serial
import time

class MBH3010:
    """
    Класс для управления драйвером лазерного диода MBH3010.
    Основные команды: включение/выключение лазера, установка/чтение тока,
    чтение напряжения и статуса.
    """
    
    def __init__(self, port="COM7", baudrate=115200, timeout=1):
        """
        Инициализация подключения к прибору.
        
        Аргументы:
            port (str): COM-порт (например, "COM7")
            baudrate (int): Скорость передачи данных
            timeout (int): Таймаут ожидания ответа в секундах
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
        
    def connect(self):
        """Подключиться к прибору."""
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Подключено к {self.port}")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def disconnect(self):
        """Отключиться от прибора."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Соединение закрыто")
    
    def _send(self, command):
        """
        Отправить команду и получить ответ.
        
        Аргументы:
            command (str): Команда для отправки
        
        Возвращает:
            str: Ответ прибора
        """
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Нет подключения к прибору")
        
        self.connection.write(command.encode('ascii'))
        time.sleep(0.1)
        
        response = self.connection.read_until(b"\r").decode('ascii').strip()
        return response
    
    def laser_on(self):
        """Включить лазер."""
        response = self._send("P0700 0008\r")
        if response.startswith("E"):
            print(f"Ошибка включения: {response}")
            return False
        print("Лазер ВКЛЮЧЕН")
        return True
    
    def laser_off(self):
        """Выключить лазер."""
        response = self._send("P0700 0010\r")
        if response.startswith("E"):
            print(f"Ошибка выключения: {response}")
            return False
        print("Лазер ВЫКЛЮЧЕН")
        return True
    
    def set_current(self, current_amps):
        """
        Установить ток лазера.
        
        Аргументы:
            current_amps (float): Ток в Амперах (например, 0.5 для 500 мА)
        """
        if current_amps < 0 or current_amps > 1.5:
            print(f"Ошибка: ток {current_amps}А вне диапазона (0-1.5А)")
            return False
        
        # Переводим в сотые доли ампера (единица измерения 0.01 А)
        current_units = int(current_amps * 100)
        hex_value = f"{current_units:04X}"
        
        response = self._send(f"P0300 {hex_value}\r")
        if response.startswith("E"):
            print(f"Ошибка установки тока: {response}")
            return False
        
        print(f"Ток установлен: {current_amps:.2f} А")
        return True
    
    def get_set_current(self):
        """
        Получить установленное значение тока.
        
        Возвращает:
            float: Ток в Амперах или None при ошибке
        """
        response = self._send("J0300\r")
        
        if response.startswith("E"):
            print(f"Ошибка получения тока: {response}")
            return None
        
        if response.startswith("K0300"):
            hex_value = response.split()[1]
            current_units = int(hex_value, 16)
            current_amps = current_units / 100.0
            print(f"Установленный ток: {current_amps:.2f} А")
            return current_amps
        
        print(f"Неожиданный ответ: {response}")
        return None
    
    def get_real_current(self):
        """
        Получить реальный ток (измеренное значение).
        
        Возвращает:
            float: Ток в Амперах или None при ошибке
        """
        response = self._send("J0307\r")
        
        if response.startswith("E"):
            print(f"Ошибка получения реального тока: {response}")
            return None
        
        if response.startswith("K0307"):
            hex_value = response.split()[1]
            current_units = int(hex_value, 16)
            current_amps = current_units / 10.0  # Единица измерения: 0.1 А
            print(f"Реальный ток: {current_amps:.2f} А")
            return current_amps
        
        print(f"Неожиданный ответ: {response}")
        return None
    
    def get_voltage(self):
        """
        Получить напряжение на лазере.
        
        Возвращает:
            float: Напряжение в Вольтах или None при ошибке
        """
        response = self._send("J0306\r")
        
        if response.startswith("E"):
            print(f"Ошибка получения напряжения: {response}")
            return None
        
        if response.startswith("K0306"):
            hex_value = response.split()[1]
            voltage_units = int(hex_value, 16)
            voltage = voltage_units / 100.0  # Единица измерения: 0.01 В
            print(f"Напряжение: {voltage:.2f} В")
            return voltage
        
        print(f"Неожиданный ответ: {response}")
        return None
    
    def get_status(self):
        """
        Получить статус лазера.
        
        Возвращает:
            str: "ON" или "OFF" или None при ошибке
        """
        response = self._send("J0700\r")
        
        if response.startswith("E"):
            print(f"Ошибка получения статуса: {response}")
            return None
        
        if response.startswith("K0700"):
            hex_value = response.split()[1]
            status_value = int(hex_value, 16)
            
            if status_value == 8:      # 0008 - лазер включен
                print("Статус: ВКЛЮЧЕН")
                return "ON"
            elif status_value == 16:   # 0010 - лазер выключен
                print("Статус: ВЫКЛЮЧЕН")
                return "OFF"
            else:
                print(f"Статус: {hex_value} (неизвестный код)")
                return None
        
        print(f"Неожиданный ответ: {response}")
        return None
    
    def enable_ntc_protection(self):
        """Включить защиту по NTC (температуре)."""
        self._send("P0700 8000\r")
        print("Защита NTC ВКЛЮЧЕНА")
    
    def disable_ntc_protection(self):
        """Отключить защиту по NTC (ОПАСНО!)."""
        self._send("P0700 4000\r")
        print("ВНИМАНИЕ: Защита NTC ОТКЛЮЧЕНА")
    
    def enable_interlock(self):
        """Включить внешнюю блокировку (Interlock)."""
        self._send("P0700 1000\r")
        print("Interlock ВКЛЮЧЕН")
    
    def disable_interlock(self):
        """Отключить внешнюю блокировку (Interlock) (ОПАСНО!)."""
        self._send("P0700 2000\r")
        print("ВНИМАНИЕ: Interlock ОТКЛЮЧЕН")
    
    def reset(self):
        """Сброс прибора до безопасного состояния."""
        self._send("P0700 0000\r")
        print("Прибор сброшен")
    
    def get_idn(self):
        """Получить идентификационную информацию прибора."""
        response = self._send("*IDN?\r")
        if response.startswith("E"):
            print(f"Ошибка: {response}")
            return None
        print(f"Прибор: {response}")
        return response


if __name__ == "__main__":
    laser = MBH3010(port="COM7")
    
    if not laser.connect():
        exit()
    
    print("\n" + "="*50)
    print("УПРАВЛЕНИЕ MBH3010")
    print("="*50)
    
    laser.get_idn()
    time.sleep(0.5)
    
    laser.set_current(0.7)
    time.sleep(0.5)
    
    laser.get_set_current()
    time.sleep(0.5)
    
    laser.laser_on()
    time.sleep(1)
    
    laser.get_real_current()
    laser.get_voltage()
    time.sleep(0.5)
    
    laser.get_status()
    time.sleep(0.5)
    
    # laser.laser_off()
    
    laser.disconnect()
    
    print("\n" + "="*50)
    print("ТЕСТ ЗАВЕРШЕН")
    print("="*50)