import os
from datetime import datetime
import logging
from database import db
from apscheduler.schedulers.background import BackgroundScheduler
from models.models import ParserBase
from tasks.actor import run_parser
from config import parsers_path

logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()


def schedule_parser(parser: ParserBase):
    start_datetime = datetime.combine(parser.startDate, parser.startTime)
    if start_datetime < datetime.now() and parser.status != "Выполнен":
        logging.info(f"Парсер {parser.id} запланирован на прошедшую дату, запущен сейчас.")
        run_parser.send(os.path.join(parsers_path, parser.selected.value), parser.id)
        db.update_parser_status(parser.id, "Выполнен")
    else:
        logging.info(f"Запланирован запуск парсера {parser.id} на {start_datetime}")
        scheduler.add_job(
            run_parser.send,
            'date',
            run_date=start_datetime,
            args=[os.path.join(parsers_path, parser.selected.value), parser.id],
            id=f'parser_{parser.id}'
        )


def remove_parser(parser_id: int):
    scheduler.remove_job(f'parser_{parser_id}')
