import sqlite3
from datetime import datetime
from typing import List
from config import db_path, parsers_names
from models.models import ParserBase


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parsers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            info TEXT,
            startDate DATE NOT NULL,
            startTime TIME NOT NULL,
            selected TEXT NOT NULL,
            status TEXT DEFAULT 'Ожидание',
            last_run_time DATETIME
        )
    ''')
    conn.commit()
    conn.close()


def save_parser(parser: ParserBase):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parsers (id, name, info, startDate, startTime, selected, status, last_run_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        parser.id,
        parser.name,
        parser.info,
        parser.startDate,
        parser.startTime.isoformat(),
        parser.selected.value,
        parser.status,
        parser.last_run_time if parser.last_run_time else None
    ))
    conn.commit()
    conn.close()


def update_parser(parser: ParserBase):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE parsers SET name = ?, info = ?, startDate = ?, startTime = ?, selected = ?, status = ?, last_run_time = ?
        WHERE id = ?
    ''', (
        parser.name,
        parser.info,
        parser.startDate,
        parser.startTime,
        parser.selected.value,
        parser.status,
        parser.last_run_time if parser.last_run_time else None,
        parser.id
    ))
    conn.commit()
    conn.close()


def delete_parser(parser_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM parsers WHERE id = ?', (parser_id,))
    conn.commit()
    conn.close()


def load_parser(parser_id: int) -> ParserBase:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parsers WHERE id = ?', (parser_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return get_parser_base(row)
    else:
        raise ValueError(f"Parser with ID {parser_id} not found")


def load_parsers() -> List[ParserBase]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parsers')
    rows = cursor.fetchall()
    conn.close()
    parsers = []
    for row in rows:
        parsers.append(get_parser_base(row))
    return parsers


def get_pending_parsers() -> List[ParserBase]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parsers WHERE status = "Ожидание"')
    rows = cursor.fetchall()
    conn.close()

    parsers = []
    for row in rows:
        parsers.append(get_parser_base(row))
    return parsers


def update_parser_status(parser_id: int, status: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    last_run_time = datetime.now()
    cursor.execute('''
        UPDATE parsers SET status = ?, last_run_time = ?
        WHERE id = ?
    ''', (status, last_run_time, parser_id))
    conn.commit()
    conn.close()


def get_parser_base(row):
    return ParserBase(
        id=row[0],
        name=row[1],
        info=row[2],
        startDate=row[3],
        startTime=row[4],
        selected=parsers_names[row[5].replace('.py', '')],
        status=row[6],
        last_run_time=datetime.fromisoformat(row[7]) if row[7] else None
    )
