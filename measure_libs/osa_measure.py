import numpy as np
from scripts.write_xy_txt import write_xy_txt
from scripts.plot_xy import plot_xy

WAVE_LABEL = 'Wavelength (nm)'


def osa_measure(device,
                folder_path: str,
                file_name: str,
                scale: str,
                save_png: bool = True,
                png_title: str | None = None,
                ) -> dict:
    """
    Измеряет оптический спектр, сохраняет данные в .txt и строит график.

    Args:
        device: объект OSA с методами set_log_scale/set_lin_scale/get_os.
        folder_path: папка для сохранения txt/png.
        file_name: базовое имя файлов (без расширения).
        scale: 'log' (dBm) или 'lin' (μW).
        save_png: сохранять ли график.
        png_title: дополнительный заголовок графика.

    Returns:
        dict: {'peak_wave': float, 'peak_power': float}
              или {'peak_wave': None, 'peak_power': None} при ошибке.
    """
    if scale == 'log':
        device.set_log_scale()
        power_unit = 'dBm'
    elif scale == 'lin':
        device.set_lin_scale()
        power_unit = 'μW'
    else:
        raise ValueError(f"scale должен быть 'log' или 'lin', получено: {scale!r}")

    power_label = f'Power ({power_unit})'

    # Получение данных
    wave_arr, power_arr = device.get_os()

    # Проверка на пустые или несогласованные данные
    if (wave_arr is None or power_arr is None
            or len(wave_arr) != len(power_arr)
            or len(wave_arr) < 2):
        print("Недостаточно или несогласованные данные")
        return {'peak_wave': None, 'peak_power': None}

    # Находим пиковые значения
    max_index = int(np.argmax(power_arr))
    peak_wave = float(wave_arr[max_index])
    peak_power = float(power_arr[max_index])
    peak_info = (
        f"Peak power: {peak_power:.3f} {power_unit}, "
        f"Wavelength(Peak power): {peak_wave:.3f} nm"
    )

    # Записываем данные в .txt файл
    write_xy_txt(
        x_arr=wave_arr,
        x_label=WAVE_LABEL,
        y_arr=power_arr,
        y_label=power_label,
        header=None,
        folder_path=folder_path,
        file_name=file_name,
    )

    if save_png:
        # Строим график
        
        new_png_title = peak_info if png_title is None else f'{peak_info}\n{png_title}'
        plot_xy(
            x_arr=wave_arr,
            y_arr=power_arr,
            title=new_png_title,
            x_label=WAVE_LABEL,
            y_label=power_label,
            folder_path=folder_path,
            file_name=file_name,
        )

    return {'peak_wave': peak_wave, 'peak_power': peak_power}