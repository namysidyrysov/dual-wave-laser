import numpy as np
from scripts.plot_xy_data import plot_xy_data
from scripts.write_xy_data_txt import write_xy_data_txt
GIGA = 1E+9
MEGA = 1E+6

def rf_measurement(rf_device,  
                   folder_path: str,
                   folder_structure: str, 
                   file_name: str, 
                   rf_rbw: float,
                   rf_trace_points: int, 
                   f_start=None, 
                   f_stop=None, 
                   f_span=None, 
                   f_center=None, 
                   rf_level=None, 
                   png_title=None,
                   ):
    """
    Выполняет измерение на RF устройстве.
    
    Требования к частоте:
    - Либо (f_start и f_stop)
    - Либо (f_center и f_span)
    """
    
    # Проверка корректности входных данных частоты
    has_start_stop = (f_start is not None and f_stop is not None)
    has_center_span = (f_center is not None and f_span is not None)
    
    if not has_start_stop and not has_center_span:
        raise ValueError("Необходимо задать либо пару (f_start, f_stop), либо пару (f_center, f_span)")
    
    # Нормализация параметров (чтобы в config_param ушли все значения)
    if has_center_span and not has_start_stop:
        # Есть центр и_span, считаем start/stop
        f_start = f_center - f_span / 2
        f_stop = f_center + f_span / 2
    elif has_start_stop and not has_center_span:
        # Есть start/stop, считаем центр и span
        f_center = (f_start + f_stop) / 2
        f_span = f_stop - f_start
        
    span_MHz = f_span/MEGA
    # Формируем новые имя папки и файла.
    new_folder_path = f'{folder_path}/RF_port_1064nm/{folder_structure}/span_{span_MHz}MHz'
    new_file_name = f'RF_{file_name}_span_{span_MHz}MHz'
    
    
    #  Настройка устройства
    rf_device.set_span(f_span)
    rf_device.set_cf(f_center)
    rf_device.set_rbw(rf_rbw)
    rf_device.set_start(f_start)
    rf_device.set_stop(f_stop)
    rf_device.set_refLevel(rf_level)
    rf_device.set_trace_points(rf_trace_points)
    
    # Получение данных
    freqs, powers = rf_device.get_rf_spectrum()
    
    # удаляем первые точки (артефакты)
    # freqs, powers=freqs[10:], powers[10:]
    
    
    
    # Проверка на пустые данные
    if len(freqs) <= 1 or len(powers) <= 1:
        print(f"Недостаточно данных")
        return {'peak_freq': 0.0, 'peak_power': 0.0}
    
    # Находим пиковые значения
    max_index = np.argmax(powers)
    peak_power = float(powers[max_index])
    peak_freq = float(freqs[max_index])
    

    x_label = "Frequency (Hz)"
    y_label = 'Power (dBm)'
    

    peak_freq_MHz=peak_freq/MEGA
    peak_info=f'Peak power: {peak_power:.3f}dBm, Freq(Peak power): {peak_freq_MHz:.3f}MHz'

    # Записываем данные в txt
    write_xy_data_txt(
                        x_arr=freqs,
                        x_label=x_label,
                        y_arr=powers,
                        y_label=y_label,
                        header=None,
                        folder_path=new_folder_path,
                        filename=new_file_name,
                    )
    
    
    # Строим график
    common_title=f'{peak_info}\n{png_title}'
    plot_xy_data(
                x=freqs, 
                y=powers, 
                title=common_title, 
                xlabel = x_label, 
                ylabel = y_label, 
                folder_path=new_folder_path, 
                filename=new_file_name, 
                show_plot=False
            )
        
    
        
        
    return {'peak_freq':float(peak_freq), 'peak_power': float(peak_power)}
