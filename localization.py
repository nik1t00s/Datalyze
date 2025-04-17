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
        """Инициализирует локализатор.

        Автоматически загружает строки из файла или использует значения по умолчанию.
        """
        self.localization = {}
        self._load_localization()

    def _load_localization(self):
        """Загружает локализацию из файла.

        File Path:
            files_for_the_project/localization/RU.txt

        Format:
            ID:Text (one per line)

        Falls back:
            К значениям по умолчанию при ошибках
        """
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
        """Устанавливает резервные строки локализации по умолчанию."""
        self.localization = {
            0: "Добро пожаловать в систему анализа медицинских данных!",
            # ... остальные строки ...
        }

    def get_string(self, string_id: int) -> str:
        """Возвращает локализованную строку по ID.

        Args:
            string_id: Числовой идентификатор строки

        Returns:
            str: Локализованный текст или сообщение об ошибке

        Example:
            "Добро пожаловать в систему анализа медицинских данных!"
        """
        return self.localization.get(string_id, f"[Ошибка локализации: ID {string_id}]")
