

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
from scripts.write_xy_txt import write_xy_txt
from measure_libs.rf_measure import rf_measurement
from measure_libs.yokogawa_measure_lib_v3 import yoko_measurement
from measure_libs.osc_measure import oscilloscope_measurement

import numpy as np
import time

MEGA = 1e+6
KILO=1e+3
NANO=1e-9

# Длина волны фильтра.
WAVELENGTH_START=1056
WAVELENGTH_STOP=1071 # Последняя точка не включается в массив.
WAVELENGTH_STEP=1
WAVELENGTHS=np.arange(WAVELENGTH_START, WAVELENGTH_STOP, WAVELENGTH_STEP)

# Ширина линии фильтра
LINEWIDTHS = [2,1,3]



BTF_COM='COM11'
STABILIZATION_TIME=3
OSC_IP="10.2.60.150"
OSC_PORT=4000
OSC_MODE='average' # Можно другое. Например, 'sample','peakdetect' 


PM_DURATION=1
PM_POINTS=3
PM_LABEL = "Power (mW)"
OSC_VER_SCALE=0.01 # в вольтах
OSC_CHANNEL=4 
OSC_DURATION=15*NANO
ITERATION_LABEL='Iteration (N)'


RF_START_6000_MHz=50*MEGA
RF_STOP_6000_MHz=1050*MEGA

RF_SPAN_100_MHz=100*MEGA
RF_SPAN_10_MHz=10*MEGA
RF_SPAN_1_MHz=1*MEGA

RF_RBW = 1*KILO # Разрешение одиноково во всех измерениях.
RF_RBW_100MHz = 100
RF_LEVEL = -20
RF_TRACE_POINTS = 10_001


TIME_BETWEEN_ITERATIONS=30 # Время между итерациями цикла. В секундах.
NUMBER_ITERATIONS=40


def main():        
    try:
        
        # Иницализация приборов
        rf = RF306B()
        yoko = YokogawaOSA()
        btf = BTF100(port=BTF_COM)
        
        # osc=Oscilloscope(ip=OSC_IP, port=OSC_PORT)
        pm_device = PMDevicePM100D()
        

        # # Осцилограф: Выбор режима
        # osc.acquire_mode(mode=OSC_MODE)
        
        # # Осцилограф: Вертикальный масштаб
        # osc.vertical_scale(channel=OSC_CHANNEL,scale=OSC_VER_SCALE)
        
        
        while True:
            try:
                LD_current = float(input("Введите ток LD, А (например, 1 или 1.5): "))
                break  # Выходим из цикла, если преобразование в float прошло успешно
            except ValueError:
                print(" [Ошибка] Неверный формат. Используйте точку как разделитель.")
        
        
                
        
        
        # Создание главной папки для сохранения результатов
        DATA_FOLDER_PATH = "Z:/DUAL_WAVELENGTH_LASER_DATA"
        # DATA_FOLDER_PATH = r"C:\Users\namys\Downloads"
        main_folder_prefix=f'LD_set_I_{LD_current}A'
        main_folder=create_date_folder(base_path=DATA_FOLDER_PATH,prefix=main_folder_prefix)

        # Записываем информацию об эксперименте.
        info_about_experiment(folder_path=main_folder)
        
        linewidth_prev = None
        wavelength_prev = None
        
        for linewidth in LINEWIDTHS:
            for wavelength in WAVELENGTHS:


                # Массивы для записи мощности
                
                iteration_arr, pm_arr = [], []

                
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
                    folder_structure = f'{linewidth}nm/{wavelength}nm'
                    pm_folder_structure = f'{linewidth}nm'
                    # Имя папок
                    file_name = f'{iteration+1}_{wavelength}nm_{linewidth}nm'
                    pm_file_name = f'POWER_{wavelength}nm_{linewidth}nm'
                    
                    # Название графиков
                    png_title_point = f'Iteration: {iteration+1}, Wavelength: {wavelength}nm, Linewidth: {linewidth}nm, Current: {LD_current}A'
                    
                    pm_folder_path = f"{main_folder}/POWER/{pm_folder_structure}"
                    # Oсциллограф: установка триегра в уровне 50%
                    # osc.set_triger_50()
                    
                    
                    # Измерения
                    pm_power = measure_average_power(pm_device=pm_device,duration=PM_DURATION,aver_point=PM_POINTS)

                    pm_arr.append(pm_power)
                    iteration_arr.append(iteration+1)
                    
                    
                
                    # Измерение RF спектр: спан 1000 MHz
                    rf_dict_1000_MHz = rf_measurement(
                            rf_device=rf, 
                            folder_path=main_folder,
                            folder_structure=folder_structure, 
                            file_name=file_name, 
                            rf_rbw=RF_RBW,
                            rf_trace_points=RF_TRACE_POINTS, 
                            f_start=RF_START_6000_MHz, 
                            f_stop=RF_STOP_6000_MHz, 
                            f_span=None, 
                            f_center=None, 
                            rf_level=RF_LEVEL, 
                            png_title=png_title_point,
                            )
                    rf_1000_MHz_peak_freq = rf_dict_1000_MHz.get('peak_freq')
                            
                            
                            
                    # Измерение RF спектр: спан 100 MHz
                    rf_dict_100_MHz = rf_measurement(
                            rf_device=rf, 
                            folder_path=main_folder,
                            folder_structure=folder_structure, 
                            file_name=file_name, 
                            rf_rbw=RF_RBW_100MHz,
                            rf_trace_points=RF_TRACE_POINTS, 
                            f_start=None, 
                            f_stop=None, 
                            f_span=RF_SPAN_100_MHz, 
                            f_center=rf_1000_MHz_peak_freq, 
                            rf_level=RF_LEVEL, 
                            png_title=png_title_point,
                            )
                    
                    rf_100_MHz_peak_freq = rf_dict_100_MHz.get('peak_freq')
                            
                            
                    # Измерение RF спектр: спан 10 MHz
                    rf_dict_10_MHz = rf_measurement(
                            rf_device=rf,
                            folder_path=main_folder,
                            folder_structure=folder_structure, 
                            file_name=file_name, 
                            rf_rbw=RF_RBW,
                            rf_trace_points=RF_TRACE_POINTS, 
                            f_start=None, 
                            f_stop=None, 
                            f_span=RF_SPAN_10_MHz, 
                            f_center=rf_100_MHz_peak_freq, 
                            rf_level=RF_LEVEL, 
                            png_title=png_title_point,
                            )
                    
                    rf_10_MHz_peak_freq = rf_dict_10_MHz.get('peak_freq')
                            
                            
                    # Измерение RF спектр: спан 1 MHz
                    rf_measurement(
                            rf_device=rf,
                            folder_path=main_folder,
                            folder_structure=folder_structure, 
                            file_name=file_name, 
                            rf_rbw=RF_RBW,
                            rf_trace_points=RF_TRACE_POINTS, 
                            f_start=None, 
                            f_stop=None, 
                            f_span=RF_SPAN_1_MHz, 
                            f_center=rf_10_MHz_peak_freq, 
                            rf_level=RF_LEVEL, 
                            png_title=png_title_point,
                            )
                            
                    # Измерения оптического спектра (log)
                    yoko_measurement(
                                    device=yoko,
                                    folder_path=main_folder,
                                    folder_structure=folder_structure, 
                                    file_name=file_name,
                                    scale='log',
                                    png_title=png_title_point
                                    )

                    # Измерения оптического спектра (lin)
                    yoko_measurement(
                                    device=yoko,
                                    folder_path=main_folder,
                                    folder_structure=folder_structure, 
                                    file_name=file_name,
                                    scale='lin',
                                    png_title=png_title_point
                                    )
                    
                    # Задержка между итерациями цикла
                    time.sleep(TIME_BETWEEN_ITERATIONS)


                #  Записываем мощности 
                write_xy_txt(
                    x_arr=iteration_arr,
                    x_label=ITERATION_LABEL,
                    y_arr=pm_arr,
                    y_label=PM_LABEL,
                    header="Мощемер:",
                    folder_path=pm_folder_path,
                    filename=pm_file_name,
                )            
                                
                
    finally:
        try:
            btf.disconnect()
            yoko.close_connect()
            # osc.disconnect()
            pm_device.disconnect()
            
            print('Все данные успешно сняты')
        except Exception as e:
            print(f"Ошибка при отключении: {e}")
        
    
    
    
    
if __name__=="__main__":                  
    main()