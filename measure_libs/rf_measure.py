import numpy as np
from scripts.plot_xy import plot_xy
from scripts.write_xy_txt import write_xy_txt

MEGA = 1E+6
FREQ_LABEL = "Frequency (Hz)"
POW_LABEL = "Power (dBm)"


def rf_measure(rf_device: str,
                   folder_path: str,
                   file_name: str,
                   f_start: float,
                   f_stop: float,
                   f_center: float,
                   f_span: float,
                   rbw: float,
                   trace_points: int,
                   level: float,
                   save_png: bool = True,
                   png_title=None,
                   ) -> dict:
    """
    Выполняет измерение на RF устройстве.

    Args:
        rf_device: объект прибора с методами set/get_rf_spectrum.
        folder_path: папка для сохранения txt/png.
        file_name: базовое имя файлов (без расширения).
        rf_rbw: полоса разрешения, Гц.
        rf_trace_points: число точек трассы.
        rf_level: опорный уровень, дБм.
        f_start, f_stop: границы диапазона, Гц.
        save_png: сохранять ли график.
        png_title: дополнительный заголовок графика.

    Returns:
        dict: {'peak_freq': float, 'peak_power': float}
              или {'peak_freq': None, 'peak_power': None} при ошибке.
    """
    if f_start >= f_stop:
        raise ValueError(f"f_start ({f_start}) должен быть меньше f_stop ({f_stop})")

    # Настройка устройства
    rf_device.set_rbw(rbw)
    rf_device.set_start(f_start)
    rf_device.set_stop(f_stop)
    rf_device.set_refLevel(level)
    rf_device.set_trace_points(trace_points)

    # Получение данных
    freqs, powers = rf_device.get_rf_spectrum()
    print(type(freqs))    # <class 'numpy.ndarray'>
    print(type(powers))   # <class 'list'>

    # Проверка на пустые или несогласованные данные
    if freqs is None or powers is None or len(freqs) != len(powers) or len(freqs) < 2:
        print("Недостаточно или несогласованные данные")
        return {'peak_freq': None, 'peak_power': None}

    # Находим пиковые значения
    max_index = int(np.argmax(powers))
    peak_power = float(powers[max_index])
    peak_freq = float(freqs[max_index])
    peak_freq_mhz = peak_freq / MEGA
    peak_info = f'Peak power: {peak_power:.3f} dBm, Freq(Peak power): {peak_freq_mhz:.3f} MHz'

    # Записываем данные в txt
    write_xy_txt(
        x_arr=freqs,
        x_label=FREQ_LABEL,
        y_arr=powers,
        y_label=POW_LABEL,
        header=None,
        folder_path=folder_path,
        file_name=file_name,
    )

    if save_png:
        # Строим график
        new_png_title = peak_info if png_title is None else f'{peak_info}\n{png_title}'
        plot_xy(
            x_arr=freqs,
            y_arr=powers,
            title=new_png_title,
            x_label=FREQ_LABEL,
            y_label=POW_LABEL,
            folder_path=folder_path,
            file_name=file_name
        )

    return {'peak_freq': peak_freq, 'peak_power': peak_power}