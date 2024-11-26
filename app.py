import logging
from fastapi import FastAPI
from tasks.scheduler import scheduler, schedule_parser
from database.db import init_db, get_pending_parsers
from routes import setup_routes


logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    fast_api_app = FastAPI()
    init_db()
    setup_routes(fast_api_app)
    scheduler.start()
    pending_parsers = get_pending_parsers()
    for parser in pending_parsers:
        schedule_parser(parser)
    return fast_api_app


app = create_app()
