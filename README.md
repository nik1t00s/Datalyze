# Datalyze
Desktop application for data analisys


## Для разработчиков

### Документация
Чтобы сгенерировать документацию, выполните:
```bash
pdoc --html data_importer_exporter.py data_table_viewer.py data_visualizer.py localization.py main.py --output-dir docs --force
```
Чтобы объеденить документацию, выполните:
```bash
python merge_docs.py
```
