from devices_libs.yokogawa.Yokogawa_OSA import YokogawaOSA
from devices_libs.btf_100.btf_100 import BTF100
from scripts.create_folder import create_date_folder
from measure_libs.osa_measure import yoko_measurement
import time


LINEWIDTHS = [2]
WAVELENGTHS = [1070]

BTF_COM='COM11'
STABILIZATION_TIME=1
 
WL_START=1030
WL_STOP=1280

TIME_BETWEEN_ITERATIONS=30 # Время между итерациями цикла. В секундах.
NUMBER_ITERATIONS=20


def main():        
    try:
        
        # Иницализация приборов
        yoko = YokogawaOSA()
        btf = BTF100(port=BTF_COM)

        while True:
            try:
                LD_current = float(input("Введите ток LD, А (например, 1 или 1.5): "))
                break  # Выходим из цикла, если преобразование в float прошло успешно
            except ValueError:
                print(" [Ошибка] Неверный формат. Используйте точку как разделитель.")
        
        
        yoko.set_start(WL_START)
        yoko.set_stop(WL_STOP)
        
        
        # Создание главной папки для сохранения результатов
        DATA_FOLDER_PATH = "Z:\BIO_experiment_dual_wavelength_laser"
        
        main_folder_prefix=f'set_current_{LD_current}A'
        main_folder=create_date_folder(base_path=DATA_FOLDER_PATH,prefix=main_folder_prefix)

        
        linewidth_prev = None
        wavelength_prev = None
        
        for linewidth in LINEWIDTHS:
            for wavelength in WAVELENGTHS:
                
                # Массивы для записи мощности
                                
                
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

                    png_title=f'N={iteration+1}, wl={wavelength}nm, wd={linewidth}nm, I={LD_current}A'
                    
                    
                    # Формируем внутренную структуру папок
                    folder_structure_lin = f'OSA_LIN'
                    # Имя папок
                    file_name_lin = f'osa_lin_N={iteration+1}_wl_{wavelength}nm_wd_{linewidth}nm_I_{LD_current}A'

                    
                    
                    # Измерения оптического спектра (LIN)
                    yoko_measurement(
                                    device=yoko,
                                    folder_path=main_folder,
                                    folder_structure=folder_structure_lin, 
                                    file_name=file_name_lin,
                                    scale='lin',
                                    png_title=png_title
                                    )

                    # Формируем внутренную структуру папок (LOG)
                    folder_structure_log = f'OSA_LOG'
                    # Имя папок
                    file_name_log = f'osa_log_N={iteration+1}_wl_{wavelength}nm_wd_{linewidth}nm_I_{LD_current}A'

                    # Измерения оптического спектра
                    yoko_measurement(
                                    device=yoko,
                                    folder_path=main_folder,
                                    folder_structure=folder_structure_log, 
                                    file_name=file_name_log,
                                    scale='log',
                                    png_title=png_title
                                    )

                    
                    # Задержка между итерациями цикла
                    time.sleep(TIME_BETWEEN_ITERATIONS)
        
    finally:
        try:
            btf.disconnect()
            yoko.close_connect()
            print('Все данные успешно сняты')
        except Exception as e:
            print(f"Ошибка при отключении: {e}")
        
    
    
if __name__=="__main__":                  
    main()