from datetime import datetime
import os

def info_about_experiment(folder_path: str):
    """ Записывает информацию об эксперименте.

    Args:
        folder_path (str): путь папки, где создается txt файл.
    """
    # Спрашиваем пользователя, нужно ли создать файл
    choice = input("Создать файл для записи информации об эксперименте? (1 - да, 0 - нет): ").strip()
    
    # Если нет — выводим 0 и завершаем работу
    if choice == '0':
        print("Файл НЕ создан")
        return
    elif choice != '1':
        print("Неверный ввод. Программа завершена.")
        return

    # Формируем полный путь к файлу
    file_name = "information_about_the_experiment.txt"
    full_path = os.path.join(folder_path, file_name)

    # Проверяем, существует ли указанная папка. Если нет — создаем ее.
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Запрашиваем информацию через консоль
    print("Введите информацию об эксперименте (для сохранения нажмите Enter):")
    experiment_info = input("> ")

    # Получаем текущую дату и точное время
    current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    # Записываем дату, время и текст в файл
    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(f"Дата и время: {current_time}\n")
            file.write("Описание эксперимента:\n")
            file.write(f"{experiment_info}\n")
        print("Файл создан")
        print(f"Файл успешно сохранен по пути: {full_path}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

        
if __name__ == '__main__':
    
    # Пример использования функции:
    info_about_experiment("./my_experiments")
