import os
import datetime

def create_date_folder(base_path, prefix=None):
    """Создаёт новые папки c временной меткой в указанной директории для

    логирования экспериментов.

    Args:
        base_path (str): Путь к основной директории проекта.
        prefix (str, optional): Название или ID конкретного эксперимента. По
          умолчанию None.

    Returns:
        str: Полный путь к созданной папке эксперимента.
    """
    # Фиксируем время
    now = datetime.datetime.now()

    today = now.strftime("%d-%b_%Y")
    timestamp = now.strftime("%b-%d-%Y_time_%H-%M-%S")

    if prefix:
        folder_name = f"{prefix}_{timestamp}"
    else:
        folder_name = timestamp

    full_path = os.path.join(base_path, today, folder_name)

    os.makedirs(full_path, exist_ok=True)
    return full_path


def create_subfolder(parent_folder_path, subfolder_name):
    """
    Создаёт подпапку внутри указанной родительской директории

    """
    subfolder = os.path.join(parent_folder_path, subfolder_name)
    os.makedirs(subfolder, exist_ok=True)
    return subfolder



if __name__=='__main__':
    create_date_folder(base_path=r'C:\Users\namys\Documents\dual-wave-laser', prefix='test_folder')