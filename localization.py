from pathlib import Path

class Localizer:
    def __init__(self):
        self.localization = {}
        self.available_locales = {
            1: "RU",
            2: "EN"
        }
        self._load_localization()

    def _load_localization(self):
        """Загрузка локализации"""
        print("Available locales:")
        for key, value in self.available_locales.items():
            print(f"{key} - {value}")

        try:
            choice = int(input("Choose locale: "))
            if choice not in self.available_locales:
                raise ValueError
        except (ValueError, KeyError):
            print("Invalid locale choice. Defaulting to RU.")
            choice = 1

        locale_file = {
            1: "RU.txt",
            2: "EN.txt"
        }.get(choice, "RU.txt")

        try:
            path = Path("files_for_the_project/localization") / locale_file
            with open(path, 'r', encoding='utf-8') as f:
                self.localization = {
                    i: line.strip() for i, line in enumerate(f.readlines())
                }
            print("Localization loaded successfully")
        except FileNotFoundError:
            print(f"Error: Localization file {locale_file} not found")
            self.localization = {}
        except Exception as e:
            print(f"Error loading localization: {str(e)}")
            self.localization = {}

    def get_string(self, string_id: int) -> str:
        """Получение локализованной строки"""
        try:
            return self.localization[string_id]
        except KeyError:
            return f"[Localization error: string {string_id} not found]"
        except AttributeError:
            return "[Localization not initialized]"

# Пример использования
if __name__ == "__main__":
    localizer = Localizer()
    print(localizer.get_string(0))  # Первая строка локализации
    print(localizer.get_string(1))  # Вторая строка локализации
