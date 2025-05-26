"""Модуль локализации строк интерфейса.

Функционал:
- Загрузка строк из файла
- Резервные строки по умолчанию
- Поддержка динамического переключения языка
- Проверка целостности локализационных файлов
- Двуязычные подсказки для выбора языка

Классы:
    Localizer: Основной класс для работы с локализацией.

Формат файла локализации:
    ID:Текст (например, '0:Добро пожаловать')
"""

from pathlib import Path
import locale
import os
import sys

SUPPORTED_LANGUAGES = ["ENG", "RU"]

class Localizer:
    def __init__(self, language=None):
        """Инициализирует объект локализации.
        
        Args:
            language: Опционально, код языка ('ENG' или 'RU').
                     Если не указан, определяется по системным настройкам.
        """
        self.base_path = Path("files_for_the_project/localization")
        self.language_files = {
            "RU": self.base_path / "RU.txt",
            "ENG": self.base_path / "ENG.txt"
        }
        
        # Проверка существования файлов локализации
        self._validate_localization_files()
        
        # Словари для хранения строк локализации
        self.localizations = {lang: {} for lang in SUPPORTED_LANGUAGES}
        
        # Загрузка всех локализаций для быстрого переключения
        for lang in SUPPORTED_LANGUAGES:
            self._load_language_file(lang)
            
        # Проверка согласованности ID строк между языками
        self._validate_string_ids()
        
        # Установка текущего языка
        self.language = language if language in SUPPORTED_LANGUAGES else self._detect_system_language()
        
        # Резервные строки на случай ошибок
        self._init_default_strings()
        
    def _validate_localization_files(self):
        """Проверяет наличие файлов локализации."""
        missing_files = []
        for lang, file_path in self.language_files.items():
            if not file_path.exists():
                missing_files.append(f"{lang}: {file_path}")
        
        if missing_files:
            print("❌ Critical Error: Missing localization files:")
            for file in missing_files:
                print(f"  - {file}")
            print("Application cannot start without localization files.")
            sys.exit(1)
                
    def _detect_system_language(self):
        """Определяет язык системы и возвращает соответствующий код."""
        sys_lang = locale.getdefaultlocale()[0]
        return "ENG" if sys_lang and sys_lang.startswith("en") else "RU"

    def _load_language_file(self, lang_code):
        """Загружает файл локализации для указанного языка.
        
        Args:
            lang_code: Код языка ('ENG' или 'RU')
        """
        try:
            path = self.language_files[lang_code]
            with open(path, 'r', encoding='utf-8') as f:
                self.localizations[lang_code] = {
                    int(line.split(":")[0]): ":".join(line.split(":")[1:]).strip()
                    for line in f if line.strip() and ":" in line
                }
        except Exception as e:
            print(f"⚠️ Error loading {lang_code} localization: {str(e)}")
            self._init_default_strings()
            
    def _validate_string_ids(self):
        """Проверяет согласованность ID строк между языками."""
        if len(SUPPORTED_LANGUAGES) < 2:
            return
            
        all_ids = set()
        ids_by_lang = {}
        
        # Собираем все ID из всех языков
        for lang in SUPPORTED_LANGUAGES:
            ids = set(self.localizations[lang].keys())
            all_ids.update(ids)
            ids_by_lang[lang] = ids
            
        # Проверяем отсутствующие ID для каждого языка
        inconsistencies = []
        for lang in SUPPORTED_LANGUAGES:
            missing_ids = all_ids - ids_by_lang[lang]
            if missing_ids:
                missing_ids_str = ", ".join(map(str, sorted(missing_ids)))
                inconsistencies.append(f"{lang} is missing IDs: {missing_ids_str}")
                
        if inconsistencies:
            print("⚠️ Warning: Localization inconsistencies detected:")
            for msg in inconsistencies:
                print(f"  - {msg}")

    def _init_default_strings(self):
        """Устанавливает резервные строки локализации по умолчанию."""
        self.default_strings = {
            # Базовые строки на двух языках
            "ENG": {
                0: "Welcome to the system of medical data analysis!",
                100: "Select language",
                101: "Invalid input. Try again."
            },
            "RU": {
                0: "Добро пожаловать в систему анализа медицинских данных!",
                100: "Выберите язык",
                101: "Неверный ввод. Попробуйте снова."
            }
        }
        
        # Добавляем резервные строки в локализации, если они отсутствуют
        for lang in SUPPORTED_LANGUAGES:
            for string_id, text in self.default_strings[lang].items():
                if string_id not in self.localizations[lang]:
                    self.localizations[lang][string_id] = text
    
    @property
    def _fallback_language(self):
        """Возвращает резервный язык."""
        return "ENG" if self.language == "RU" else "RU"
        
    def _reload_localizations(self):
        """Перезагружает все файлы локализации."""
        for lang in SUPPORTED_LANGUAGES:
            self._load_language_file(lang)
        self._validate_string_ids()

    def get_string(self, string_id: int) -> str:
        """Возвращает локализованную строку по ID.

        Args:
            string_id: Числовой идентификатор строки

        Returns:
            str: Локализованный текст или сообщение об ошибке

        Example:
            "Добро пожаловать в систему анализа медицинских данных!"
        """
        # Пробуем получить строку из текущего языка
        string = self.localizations[self.language].get(string_id)
        
        # Если строка не найдена, пробуем резервный язык
        if string is None:
            string = self.localizations[self._fallback_language].get(string_id)
            
        # Если строка не найдена и в резервном языке, возвращаем сообщение об ошибке
        if string is None:
            return f"[Missing string ID: {string_id}]"
            
        return string
        
    def get_bilingual_string(self, string_id: int) -> str:
        """Возвращает строку на обоих языках (для меню выбора языка).
        
        Args:
            string_id: Числовой идентификатор строки
            
        Returns:
            str: Строка в формате "English / Русский"
        """
        eng_string = self.localizations["ENG"].get(string_id, f"[Missing ID: {string_id}]")
        ru_string = self.localizations["RU"].get(string_id, f"[Missing ID: {string_id}]")
        return f"{eng_string} / {ru_string}"
        
    def select_language(self):
        """Показывает двуязычное меню выбора языка.
        
        Returns:
            bool: True, если язык был изменен, иначе False
        """
        print("\n=== Language Selection / Выбор языка ===")
        print(self.get_bilingual_string(100) + ":")
        print("1. English / Английский")
        print("2. Русский / Russian")
        
        initial_language = self.language
        
        while True:
            choice = input(f"{self.get_bilingual_string(17)} (1-2): ").strip()
            if choice == "1":
                self.language = "ENG"
                break
            elif choice == "2":
                self.language = "RU"
                break
            else:
                print(self.get_bilingual_string(101))
                
        return initial_language != self.language
