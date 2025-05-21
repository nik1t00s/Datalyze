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
import locale

class Localizer:
    def __init__(self):
        self.language = self._detect_system_language()
        self.localization = {}
        self._load_localization()

    def _detect_system_language(self):
        sys_lang = locale.getdefaultlocale()[0]
        return "ENG" if sys_lang.startswith("en") else "RU"

    def _load_localization(self):
        base_path = Path("files_for_the_project/localization")
        lang_files = {
            "RU": base_path / "RU.txt",
            "ENG": base_path / "ENG.txt"
        }
        
        try:
            path = lang_files[self.language]
            with open(path, 'r', encoding='utf-8') as f:
                self.localization = {
                    int(line.split(":")[0]): ":".join(line.split(":")[1:]).strip()
                    for line in f if line.strip()
                }
        except FileNotFoundError:
            print(f"⚠️ Missing {self.language} localization! Using {self._fallback_language}")
            self.language = self._fallback_language
            self._load_localization()

    def _load_default_strings(self):
        """Устанавливает резервные строки локализации по умолчанию."""
        self.localization = {
            0: "Добро пожаловать в систему анализа медицинских данных!",
        }
    
    @property
    def _fallback_language(self):
        return "ENG" if self.language == "RU" else "RU"

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
