"""Модуль локализации строк интерфейса.

Функционал:
- Загрузка строк из файла
- Резервные строки по умолчанию
- Поддержка динамического переключения языка

Классы:
    Localizer: Основной класс для работы с локализацией.

Формат файла локализации:
    ID:Текст (например, '0:Добро пожаловать')
"""

from pathlib import Path

class Localizer:
    def __init__(self):
        self.localization = {}
        self._load_localization()

    def _load_localization(self):
        """Загрузка локализации из файла"""
        try:
            path = Path("files_for_the_project/localization/RU.txt")
            with open(path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                self.localization = {
                    int(line.split(":")[0]): ":".join(line.split(":")[1:]).strip()
                    for line in lines
                }
        except FileNotFoundError:
            print("Файл локализации не найден! Используются значения по умолчанию")
            self._load_default_strings()
        except Exception as e:
            print(f"Ошибка загрузки локализации: {str(e)}")
            self._load_default_strings()

    def _load_default_strings(self):
        """Резервные строки"""
        self.localization = {
            0: "Добро пожаловать в систему анализа медицинских данных!",
            1: "Разработчики: Соколов А.В., Кожемякин А.А., Шиханова Е.В., Чайка Н.В.",
            2: "Главное меню",
            5: "Выход",
            6: "Импорт/Экспорт данных",
            7: "Просмотр таблицы",
            8: "Визуализация данных",
            9: "Ошибка: введите число от 0 до 3",
            10: "Ошибка: данные не загружены!",
            11: "Успешно загружено записей: {}",
            12: "Работа программы завершена",
            13: "Спасибо за использование нашего ПО!",
            14: "Ошибка инициализации компонентов",
            15: "Работа прервана пользователем",
            16: "Критическая ошибка",
            17: "Выберите пункт меню"
        }

    def get_string(self, string_id: int) -> str:
        """Возвращает локализованную строку по ID.
    
        Args:
            string_id: Числовой идентификатор строки.
        
        Returns:
            str: Локализованный текст или сообщение об ошибке.
        """
        return self.localization.get(string_id, f"[Ошибка локализации: ID {string_id}]")
