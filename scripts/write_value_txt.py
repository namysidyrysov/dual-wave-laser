import os


def write_value_txt(
        value,
        value_label,
        header=None,
        folder_path="test_folder",
        filename="output.txt",
    ):
    """
    Функция записывает одно значение в txt-файл.

    Parameters
    ----------
    value : int | float | str
        Значение для записи.
    value_label : str
        Название параметра (например, "Current (mA)").
    header : str | None
        Дополнительная информация в начале файла.
    """

    # Создание папки
    os.makedirs(folder_path, exist_ok=True)

    if not filename.lower().endswith(".txt"):
        filename = f"{filename}.txt"

    filepath = os.path.join(folder_path, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        if header:
            f.write(header + "\n")
        f.write(value_label + "\n")
        f.write(str(value) + "\n")

    print(f"Данные успешно сохранены в: {filepath}")
    
if __name__=="__main__":
    write_value_txt(
    value=12.5,
    value_label="Current (mA)",
    header="Информация об эксперименте",
    folder_path="test_folder",
    filename="current.txt",
)