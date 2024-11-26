import enum
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
parsers_path = os.path.join(base_dir, 'uploaded_parsers')
results_path = os.path.join(base_dir, 'parsers_results')
db_path = os.path.join(base_dir, 'database/parsers.db')


def get_file_names_enum():
    files = [file for file in os.listdir(parsers_path) if os.path.isfile(os.path.join(parsers_path, file))]
    return enum.Enum('Parsers', {file.replace('.py', ''): file for file in files})


# Генерация enum для выпадающего списка
parsers_names = get_file_names_enum()
