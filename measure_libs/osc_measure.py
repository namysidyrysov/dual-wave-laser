from scripts.plot_xy import plot_xy
from scripts.write_xy_txt import write_xy_txt

TIME_LABEL_NS = "Time (ns)"
VOLTAGE_LABEL = "Voltage (V)"
S_TO_NS=1e+9


def osc_measure(
    device, 
    folder_path: str,
    file_name: str, 
    channel: int = 4, 
    png_title: str | None = None,
    save_png: bool = True,
    ) -> dict:
    """Измеряет параметры сигнала с осциллографа, сохраняет TXT и (опц.) PNG.

    Returns:
        dict со статистикой частоты: value_GHz, mean_GHz, min_GHz,
        max_GHz, std_GHz, count.
    """


    # Получение данных
    time_arr, voltage_arr = device.get_oscilloscope_data(channel=channel)
    if time_arr is None or voltage_arr is None:
        raise RuntimeError(f"Нет данных с канала {channel}")
    print(type(time_arr))
    
    
    # Измерение частоты
    stats = device.measure_freq_stats(channel)

    header = "\n".join([
                            f"Value_GHz\t{stats['value_GHz']}",
                            f"Mean_GHz\t{stats['mean_GHz']}",
                            f"Min_GHz\t{stats['min_GHz']}",
                            f"Max_GHz\t{stats['max_GHz']}",
                            f"St_Dev_GHz\t{stats['std_GHz']}",
                            f"Count\t{stats['count']}",
                        ]) + "\n"

    freq_info = (
                    f"Value: {stats['value_GHz']:.4f}GHz, "
                    f"Mean: {stats['mean_GHz']:.4f}GHz, "
                    f"St Dev: {stats['std_GHz']:.4f}GHz, "
                    f"Count: {stats['count']}"
                )

    time_arr_ns = time_arr * S_TO_NS

    write_xy_txt(
        x_arr=time_arr_ns, 
        x_label=TIME_LABEL_NS,
        y_arr=voltage_arr, 
        y_label=VOLTAGE_LABEL,
        header=header, 
        folder_path=folder_path, 
        file_name=file_name,
    )

    if save_png:
        title = freq_info if png_title is None else f"{freq_info}\n{png_title}"
        plot_xy(
            x_arr=time_arr_ns, 
            x_label=TIME_LABEL_NS,
            y_arr=voltage_arr, 
            y_label=VOLTAGE_LABEL,
            title=title, 
            folder_path=folder_path, 
            file_name=file_name,
        )

    return stats

    
            
            