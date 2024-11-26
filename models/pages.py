from fastui import components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent

from models.models import ParserBase, AddParser


def parsers_table_page(parsers):
    return [
        c.Page(
            components=[
                c.Heading(text='Парсеры', level=2),
                c.Table(
                    data=parsers,
                    data_model=ParserBase,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name', on_click=GoToEvent(url='/parser/{id}/')),
                        DisplayLookup(field='startDate', mode=DisplayMode.date),
                        DisplayLookup(field='startTime', mode=DisplayMode.datetime),
                        DisplayLookup(field='status'),
                        DisplayLookup(field='last_run_time', mode=DisplayMode.date),
                    ],
                ),
                c.Button(text="Добавить парсер", on_click=GoToEvent(url="/parser/add"))
            ]
        ),
    ]


def add_parser_page():
    return [
        c.Page(
            components=[
                c.Link(components=[c.Text(text='Назад')], on_click=BackEvent()),
                c.Heading(text='Добавить парсер', level=2),
                c.ModelForm(
                    model=AddParser,
                    submit_url="/api/parser"
                )
            ]
        )
    ]


def parser_profile_page(parser, parser_id):
    return [
        c.Page(
            components=[
                c.Heading(text=parser.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=parser),
                c.LinkList(
                    links=[
                        c.Link(
                            components=[c.Text(text='Скачать результат')],
                            on_click=GoToEvent(url=f'/api/parser/{parser_id}/download', target='_blank'),
                        ),
                    ],
                ),
                c.Button(text="Удалить парсер", on_click=PageEvent(name="delete-parser")),
                c.Button(text="Запустить парсер сейчас", on_click=PageEvent(name="start-parser")),
                c.Form(
                    submit_url=f"/api/parser/{parser_id}/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=parser_id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-parser"),
                ),
                c.Form(
                    submit_url=f"/api/parser/{parser_id}/start",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=parser_id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="start-parser"),
                ),
            ]
        ),
    ]


def main_page_event():
    return [c.FireEvent(event=GoToEvent(url='/'))]
