
import numpy as np
from scripts.write_xy_data_txt import write_xy_data_txt
from scripts.plot_xy_data import plot_xy_data


def yoko_measurement(
    device,
    folder_path: str,
    folder_structure: str, 
    file_name: str,
    scale: str,
    png_title=None
    ):
    """
    Функция для измеряет оптический спектр. Записывает в .txt файл. Строит график.
    """

    if scale=='log':
            device.set_log_scale()
            # Формируем новые имя папки и файла.
            new_folder_path = f'{folder_path}/OSA_log_port_1064/{folder_structure}'
            new_filename=f"OSA_log_{file_name}"
    
    if scale=='lin':
        device.set_lin_scale()
        # Формируем новые имя папки и файла.
        new_folder_path = f'{folder_path}/OSA_lin_port_1064/{folder_structure}'
        new_filename=f"OSA_lin_{file_name}"
        
        
    

    
    # Получение данных
    wave_arr, power_arr = device.get_os()

    # Находим пиковые значения
    max_index = np.argmax(power_arr)
    peak_wave = float(wave_arr[max_index])
    peak_power = float(power_arr[max_index])

    

    wave_label = 'Wavelength (nm)'
    power_label = 'Power'
    
    # Записываем данные в .txt файл
    write_xy_data_txt(
        x_arr=wave_arr,
        x_label=wave_label,
        y_arr=power_arr,
        y_label=power_label,
        header=None,
        folder_path=new_folder_path,
        filename=new_filename,
    )
    
    # Строим график
    peak_info=f"Peak power: {peak_power:.3f}, Wavelength(Peak power): {peak_wave:.3f}nm"
    title = f"{peak_info}\n{png_title}" if png_title else peak_info
    plot_xy_data(
        x=wave_arr, 
        xlabel=wave_label, 
        y=power_arr,
        ylabel=power_label, 
        title=title,
        folder_path=new_folder_path, 
        filename=new_filename, 
        show_plot=False
    )
    return {'peak_wave':peak_wave,'peak_power': peak_power}
