import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator

# ========================
# КОНСТАНТЫ СТИЛЯ
# ========================
FIGSIZE = (16, 9)
DPI = 100
FONT_FAMILY = 'serif'
FONT_SIZE_BASE = 20
FONT_SIZE_LABEL = 22
FONT_SIZE_TICK = 20
FONT_SIZE_TITLE_TEXT = 25
LINEWIDTH = 2
MARKERSIZE = 8
LINE_COLOR = 'blue'


def plot_xy(
        x_arr,
        y_arr,
        title,
        x_label,
        y_label,
        folder_path=None,
        file_name=None,
        show_plot=False,
        markers=False,
):
    """ 
    Строит график y(x)
    """
    # Перевод данных на numpy массив
    x_arr = np.asarray(x_arr)
    y_arr = np.asarray(y_arr)

    # Подготовка путей
    save_needed = folder_path is not None and file_name is not None

    if save_needed:
        # Защита от пустой строки
        if not folder_path or not str(folder_path).strip():
            folder_path = '.'
        os.makedirs(folder_path, exist_ok=True)

    # Настройки стиля
    rcParams['font.family'] = FONT_FAMILY
    rcParams.update({
        'font.size': FONT_SIZE_BASE,
        'axes.labelsize': FONT_SIZE_LABEL,
        'xtick.labelsize': FONT_SIZE_TICK,
        'ytick.labelsize': FONT_SIZE_TICK,
    })

    # Построение
    fig, ax = plt.subplots(figsize=FIGSIZE)

    plot_kwargs = dict(
        linewidth=LINEWIDTH,
        color=LINE_COLOR,
    )
    if markers:
        plot_kwargs.update(
            marker='o',
            markersize=MARKERSIZE,
            markerfacecolor=LINE_COLOR,
            markeredgecolor=LINE_COLOR,
        )

    ax.plot(x_arr, y_arr, **plot_kwargs)

    if title is not None:
        ax.set_title(title, fontsize=FONT_SIZE_TITLE_TEXT)
    ax.set_xlabel(x_label, fontsize=FONT_SIZE_LABEL)
    ax.set_ylabel(y_label, fontsize=FONT_SIZE_LABEL)

    # сетка + мелкие деления
    ax.grid(True, which='major', linestyle='-', linewidth=1, alpha=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    # Сохранение
    if save_needed:
        name = str(file_name)
        if name.lower().endswith('.png'):
            name = name[:-4]
        full_path = os.path.join(folder_path, f"{name}.png")
        fig.savefig(full_path, dpi=DPI, bbox_inches='tight')
        print(f"\nГрафик сохранён в: {full_path}")

    # Показ/закрытие
    if show_plot:
        plt.show()
    plt.close(fig)



# ========================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ========================
if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 5, 3]

    
    
    plot_xy(
        x_arr=x, y_arr=y,
        title='Линия с маркерами',
        x_label='Ось X', y_label='Ось Y',
        folder_path='graph', file_name='line_markers',
        markers=True,
        show_plot=True,
    )
