import logging
import os
from typing import Annotated, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastui import FastUI, AnyComponent, prebuilt_html
from fastui.forms import fastui_form

from database import db
from config import parsers_path
from models.models import ParserBase, AddParser, DeleteParser
from models import pages
from tasks.scheduler import schedule_parser, remove_parser
from tasks.actor import run_parser

logging.basicConfig(level=logging.INFO)


def setup_routes(app: FastAPI):

    # Добавление парсера
    @app.post("/api/parser")
    def add_parser(form: Annotated[AddParser, fastui_form(AddParser)]):
        last_parser_id = db.load_parsers()[-1].id if db.load_parsers() else 0
        new_parser = ParserBase(id=last_parser_id + 1, **form.model_dump())
        db.save_parser(new_parser)
        schedule_parser(new_parser)
        return pages.main_page_event()

    # Удаление парсера
    @app.post("/api/parser/{parser_id}/delete")
    def delete_parser(form: Annotated[DeleteParser, fastui_form(DeleteParser)]):
        parser = db.load_parser(form.id)
        db.delete_parser(form.id)

        result_file = f"parsers_results/{form.id}_result.txt"
        if os.path.exists(result_file):
            try:
                os.remove(result_file)
                logging.info(f"Файл результата парсера {form.id} успешно удален.")
            except Exception as e:
                logging.error(f"Ошибка при удалении результата для парсера {form.id}: {e}")

        if parser.status != "Выполнен":
            remove_parser(form.id)

        return pages.main_page_event()

    # Страница добавления парсера
    @app.get("/api/parser/add", response_model=FastUI, response_model_exclude_none=True)
    def add_parser_page():
        return pages.add_parser_page()

    # Главная страница
    @app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
    def parsers_table() -> List[AnyComponent]:
        return pages.parsers_table_page(db.load_parsers())

    # Страница парсера
    @app.get("/api/parser/{parser_id}/", response_model=FastUI, response_model_exclude_none=True)
    def parser_profile(parser_id: int) -> List[AnyComponent]:
        parser = db.load_parser(parser_id)
        return pages.parser_profile_page(parser, parser_id)

    # Ручной старт парсера
    @app.post("/api/parser/{parser_id}/start")
    def start_parser(parser_id: int):
        parser = db.load_parser(parser_id)

        file_path = os.path.join(parsers_path, parser.selected.value)
        if os.path.exists(file_path):
            run_parser.send(file_path, parser_id)
            logging.info(f"Парсер {parser_id} запущен вручную")
        else:
            raise HTTPException(status_code=404, detail="Скрипт парсера не найден")

    # Скачивание результата парсера
    @app.get('/api/parser/{parser_id}/download', response_model=FastUI, response_model_exclude_none=True)
    def download_result(parser_id: int):
        result_file = f"parsers_results/{parser_id}_result.txt"
        if os.path.exists(result_file):
            return FileResponse(
                path=result_file,
                media_type="application/octet-stream",
                filename=f"parser_{parser_id}_result.txt",
                headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")

    @app.get('/{path:path}')
    async def html_landing() -> HTMLResponse:
        """Simple HTML page which serves the React app, comes last as it matches all paths."""
        return HTMLResponse(prebuilt_html(title='Мои парсеры'))
