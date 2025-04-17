from bs4 import BeautifulSoup
import os


def merge_html_files(files, output_file="combined_docs.html"):
    # Создаем базовую структуру HTML
    combined = BeautifulSoup("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Документация проекта</title>
        <meta charset="utf-8">
        <style>
            /* Сохраняем оригинальные стили pdoc */
            :root{--highlight-color:#fe9}.flex{display:flex !important}body{line-height:1.5em}
            /* Добавляем стили для навигации */
            .module-nav {position: fixed; left: 0; top: 0; width: 250px; height: 100vh; overflow-y: auto; padding: 10px; background: #f5f5f5;}
            .module-content {margin-left: 270px; padding: 20px;}
            .module-section {margin-bottom: 40px; border-bottom: 1px solid #ddd; padding-bottom: 20px;}
            .back-to-top {display: block; text-align: right; margin-top: 20px;}
        </style>
    </head>
    <body>
        <div class="module-nav"></div>
        <div class="module-content"></div>
    </body>
    </html>
    """, 'html.parser')

    nav = combined.find('div', class_='module-nav')
    content = combined.find('div', class_='module-content')

    # Добавляем заголовок проекта
    nav.append(combined.new_tag('h1', string='Модули проекта'))

    # Обрабатываем каждый файл
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

            # Извлекаем название модуля
            module_name = soup.find('h1', class_='title').text.replace('Module ', '')

            # Добавляем в навигацию
            nav_link = combined.new_tag('a', href=f'#{module_name}', string=module_name)
            nav.append(nav_link)
            nav.append(combined.new_tag('br'))

            # Создаем секцию модуля
            module_section = combined.new_tag('div', id=module_name, class_='module-section')
            module_section.append(combined.new_tag('h2', string=module_name))

            # Переносим основное содержимое
            main_content = soup.find('article', id='content')
            if main_content:
                module_section.append(main_content)

            content.append(module_section)

    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(combined))


# Укажите ваши файлы в правильном порядке
files_to_merge = [
    'main.html',
    'data_importer_exporter.html',
    'data_table_viewer.html',
    'data_visualizer.html',
    'localization.html'
]

merge_html_files(files_to_merge)