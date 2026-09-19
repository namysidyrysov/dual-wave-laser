

from devices_libs.rsa_device.RF306B import RF306B
from devices_libs.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices_libs.btf_100.btf_100 import BTF100
from devices_libs.oscilloscope.tektronix_DPO71604C import Oscilloscope
from devices_libs.pm_400.PMDevice import PMDevicePM100D, measure_average_power



# from mock_devices.rsa_device.RF306B import RF306B
# from mock_devices.yokogawa.Yokogawa_OSA import YokogawaOSA
# from mock_devices.btf_100.btf_100 import BTF100
# from mock_devices.oscilloscope.tektronix_DPO71604C import Oscilloscope
# from mock_devices.pm_400.PMDevice import PMDevicePM100D, measure_average_power

from scripts.create_folder import create_date_folder
from scripts.write_value_txt import write_value_txt
from scripts.information_about_experiment import info_about_experiment
from scripts.write_xy_data_txt import write_xy_data_txt
from measure_libs.rf_measure_lib_v2 import rf_measurement
from measure_libs.yokogawa_measure_lib_v3 import yoko_measurement
from measure_libs.oscilloscope_measure_lib import oscilloscope_measurement

import numpy as np
import time

MEGA = 1e+6
KILO=1e+3
NANO=1e-9

# Длина волны фильтра.
WAVELENGTH_START=1062
WAVELENGTH_STOP=1071 # Последняя точка не включается в массив.
WAVELENGTH_STEP=2
# WAVELENGTHS=np.arange(WAVELENGTH_START, WAVELENGTH_STOP, WAVELENGTH_STEP)
WAVELENGTHS=[1064]
# Ширина линии фильтра.
# LINEWIDTH_START=2
# LINEWIDTH_STOP= # Последняя точка не включается в массив.
# LINEWIDTH_STEP=1
# LINEWIDTHS=np.arange(LINEWIDTH_START, LINEWIDTH_STOP, LINEWIDTH_STEP)
LINEWIDTHS = [2]



BTF_COM='COM11'
STABILIZATION_TIME=5
OSC_IP="10.2.60.150"
OSC_PORT=4000
OSC_MODE='average' # Можно другое. Например, 'sample','peakdetect' 
OSC_CHANNEL=4 




TIME_BETWEEN_ITERATIONS=30 # Время между итерациями цикла. В секундах.
NUMBER_ITERATIONS=20


def main():        
    try:
        
        # Иницализация приборов
        btf = BTF100(port=BTF_COM)
        osc=Oscilloscope(ip=OSC_IP, port=OSC_PORT)
        
        

        # Осцилограф: Выбор режима
        # osc.acquire_mode(mode=OSC_MODE)
        
        while True:
            try:
                LD_current = float(input("Введите ток LD, А (например, 1 или 1.5): "))
                break  # Выходим из цикла, если преобразование в float прошло успешно
            except ValueError:
                print(" [Ошибка] Неверный формат. Используйте точку как разделитель.")
        
        
        # Создание главной папки для сохранения результатов
        DATA_FOLDER_PATH = "Z:/DUAL_WAVELENGTH_LASER_DATA"
        # DATA_FOLDER_PATH = r"C:\Users\namys\Downloads"
        main_folder_prefix=f'OSC_channel_1060nm_LD_current_{LD_current}A'
        main_folder=create_date_folder(base_path=DATA_FOLDER_PATH,prefix=main_folder_prefix)

        # Записываем информацию об эксперименте.
        info_about_experiment(folder_path=main_folder)
        
        linewidth_prev = None
        wavelength_prev = None
        
        for linewidth in LINEWIDTHS:
            for wavelength in WAVELENGTHS:
                
                # Настройка приборов
                if linewidth != linewidth_prev:
                    btf.set_linewidth(linewidth)
                    linewidth_prev = linewidth

                if wavelength != wavelength_prev:
                    btf.set_wavelength(wavelength)
                    wavelength_prev = wavelength
                
                # Время для стабилизации лазера
                time.sleep(STABILIZATION_TIME)
                
                
                for iteration in range(NUMBER_ITERATIONS):
                    print(f"\n--- Итерация {iteration+1}/{NUMBER_ITERATIONS} ---")
                    
                    # Формируем внутренную структуру папок
                    folder_structure = f'linewidth_{linewidth}nm/wavelength_{wavelength}nm'
                    
                    # Имя папок
                    file_name = f'iteration_{iteration+1}_wavelength_{wavelength}nm_linewidth_{linewidth}nm_current_{LD_current}A'
                    
                    # Название графиков
                    png_title_point = f'Iteration: {iteration+1}, Wavelength: {wavelength}nm, Linewidth: {linewidth}nm, Current: {LD_current}A'
                    
                    
                    # Oсциллограф: установка триегра в уровне 50%
                    # osc.set_triger_50()
                    
                    # Измерение осциллограммы
                    oscilloscope_measurement(
                    device=osc,
                    save_folder_path=main_folder, 
                    filename=file_name, 
                    folder_structure=folder_structure,
                    channel=OSC_CHANNEL, 
                    png_title_point=png_title_point
                    )
                    
                    # Задержка между итерациями цикла
                    time.sleep(TIME_BETWEEN_ITERATIONS)


                
    finally:
        try:
            btf.disconnect()
            osc.disconnect()
           
            print('Все данные успешно сняты')
        except Exception as e:
            print(f"Ошибка при отключении: {e}")
        
    
    
    
    
if __name__=="__main__":                  
    main()