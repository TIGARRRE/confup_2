import requests
import re
import toml
from collections import defaultdict
from graphviz import Source
import subprocess
import os

config = toml.load('config.toml')



def clean_version(version):
    # Оставить только номер версии, если это можно сделать
    return (re.findall(r'\d+\.\d+\.\d+', version) or [None])[0]

def get_dependencies(package_name, version=None, max_depth=3):
    # Если достигли максимальной глубины вложенности, выходим
    if max_depth == 0:
        return
    # Если уже смотрели зависимости этого пакета, выходим
    if (package_name, version) in visited:
        return
    # Берем json-файл с информацией о пакете
    url = f'{(config['url'])}{package_name}'
    package_data = requests.get(url).json()
    # Если версия пакета не указана, берем последнюю версию
    if version is None:
        version = package_data['dist-tags']['latest']
    visited.add((package_name, version))
    # Извлекаем зависимости из json-файла
    dependencies = package_data['versions'][version].get('dependencies', {})
    for dep_name, ver in dependencies.items():
        dep_ver = clean_version(ver)
        # Добавляем зависимость в общий словарик
        all_dependencies[(package_name, version)].add((dep_name, dep_ver))
        # Рекурсивно ищем зависимости для этой зависимости
        get_dependencies(dep_name, dep_ver, max_depth-2)

# Словарь со всеми зависимостями
all_dependencies = defaultdict(set)
# Множество рассмотренных пакетов, чтобы не повторяться
visited = set()
# Найти все зависимости пакета express с максимальным уровнем глубины 2
get_dependencies((config['npm_name']), max_depth=2)

# Записываем все зависимости из словаря в файл graph.txt в graphviz-формате
with open('graph.dot', 'w') as file:
    file.write('digraph G {\n  ')
    for (n1, v1), deps in all_dependencies.items():
        for n2, v2 in deps:
            file.write(f'\t"{n1}\\n[{v1}]" -> "{n2}\\n[{v2}]"\n')
    file.write('}')
    


# Path to the Graphviz executable

# Change to the directory where the DOT file is located
os.chdir(os.path.dirname(os.path.abspath('graph.dot')))
# Run the Graphviz command to generate the PNG file
def generate_png():
    try:
        subprocess.run([(config['graphviz_path']), '-Tpng', 'graph.dot', '-o', "base.png"], check=True)
        print(f"PNG file successfully saved at: {config['save_path']}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PNG file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
generate_png()