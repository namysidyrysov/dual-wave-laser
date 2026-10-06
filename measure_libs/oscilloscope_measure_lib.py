import time
import numpy as np
from typing import Tuple, Optional, Dict, Any
from scripts.write_xy_data_txt import write_xy_data_txt
from scripts.plot_xy_data import plot_xy_data
from scripts.create_folder import create_subfolder, create_multiple_subfolders

GIGA=1e+9


def oscilloscope_measurement(device, save_folder_path, filename, folder_structure="folder_1/folder_2", channel=4, png_title=None, png_title_point=None):
    
    new_folder_structure=f'{folder_structure}'
    
    # Создаем вложенные папки
    measurement_folder = create_multiple_subfolders(parent_folder=save_folder_path,folder_structure=new_folder_structure)

    # Формируем имя файла
    osc_filename = f"osc_{filename}"

    # Получение данных
    time_arr, voltage_arr = device.get_oscilloscope_data(channel=channel)
    time_arr, voltage_arr = np.array(time_arr), np.array(voltage_arr)
    
    # Измерение частоты
    stats = device.measure_freq_stats(4)
    png_title = (
        f"Value: {stats['value_GHz']:.4f}GHz, "
                f"Mean: {stats['mean_GHz']:.4f}GHz, "
                f"St Dev: {stats['std_GHz']:.4f}GHz, "
                f"Count: {stats['count']}"
                )
    
    
    header_1 = f"Value_GHz\t{stats['value_GHz']}"
    header_2=f"Mean_GHz\t{stats['mean_GHz']}"
    header_3=f"Min_GHz\t{stats['min_GHz']}"
    header_4=f"Max_GHz\t{stats['max_GHz']}"
    header_5=f"St_Dev_GHz\t{stats['std_GHz']}"
    header_6=f"Count\t{stats['count']}"
    header_lines=f'{header_1}\n{header_2}\n{header_3}\n{header_4}\n{header_5}\n{header_6}\n'

    # Перевод на ns
    time_arr = time_arr * GIGA
    x_label = "Time (ns)"
    y_label = "Voltage (V)"

    

    # Запись TXT
    write_xy_data_txt(
        x_arr=time_arr,
        x_label=x_label,
        y_arr=voltage_arr,
        y_label=y_label,
        header=header_lines,
        folder_path=measurement_folder,
        filename=osc_filename, 
    )

    # Запись PNG 
    
    title=f'{png_title}\n{png_title_point}'
    
    plot_xy_data(
    x=time_arr, 
    xlabel=x_label, 
    y=voltage_arr,
    ylabel=y_label, 
    title=title,
    folder_path=measurement_folder, 
    filename=osc_filename, 
    show_plot=False
)
    # Сохраняем результат в словарь

    return stats

    
            
            