import importlib
import logging
import os
from dramatiq import actor
from database import db
from config import results_path


@actor
def run_parser(file_path: str, parser_id: int):
    try:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, 'Parser'):
            raise Exception("Класс `Parser` не найден")

        parser_instance = module.Parser()
        if not hasattr(parser_instance, 'run'):
            raise Exception(" Метод `run` не найден в классе парсера")

        result = parser_instance.run()
        if isinstance(result, dict):
            update_parser_status(parser_id, "Выполнен")
            with open(f"{results_path}/{parser_id}_result.txt", "w", encoding="utf-8") as f:
                f.write(str(result))
        else:
            raise Exception("Неверная структура результата от парсера")

    except Exception as e:
        update_parser_status(parser_id, f"Ошибка: {str(e)}")
        logging.error(f"Ошибка при выполнении парсера {parser_id}: {e}")


def update_parser_status(parser_id: int, status: str):
    db.update_parser_status(parser_id, status)
    logging.info(f"Статус парсера {parser_id} обновлен до {status}")
