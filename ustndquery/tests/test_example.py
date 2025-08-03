"""
Модуль содержит тесты для проверки функциональности модуля ustndquery.

Тестируются следующие функции:
- `get_query`: Получение запроса.
- `run`: Обработка текстового запроса и возврат результата.
- `astream_run`: Асинхронная обработка текстового запроса с потоковым выводом.

Используются параметризованные тесты с различными примерами текстовых запросов.
"""

from ustndquery.example import run, get_query
import pytest
from ustndquery.dataclass.query import Query


def test_get_query(capsys, caplog):
    with capsys.disabled():
        d = get_query()


queries_list = (
    "найди однушку  в тушино",
    # "комнату на тверской",
    # "найди комнату в тушино",
    # "Трешку на улице подбльского в 5 этажном доме",
    # "коттедж на рублевке от 1000 квадратов",
    # "таунхаус в митино от 1000000 рублей",
    "трешка в 9 этажном доме  в районе матвеевской улицы",
    "небольшая двушка на  поклонной горе под офис",
    "квартиру в москве метров 50,  в 16 этажном доме,  с ценой 1000 долларов за  метр где-нибудь в крылатском или  теплом стане",
    "квартиру в москве метров 50,  в 16 этажном доме,  с ценой 1000 рублей за  метр где-нибудь в крылатском или  теплом стане",
)


@pytest.mark.parametrize("query", queries_list)
def test_run(capsys, caplog, query):
    with capsys.disabled():
        with caplog.at_level("DEBUG") as cm:
            print(f"Запрос: {query}")
            res = run(query)
            # print(f"Ответ: {res.model_dump_json(indent=2,exclude_none=False,)}")
            # print(f"Ответ: {res}")
            q = Query(**res["properties"])
            print(
                f"Ответ: {q.model_dump_json(indent=2,exclude_none=True,exclude_unset=True,exclude_defaults=True)}"
            )
            # print(caplog.text)
            # caplog.clear()


from ustndquery.example import astream_run


@pytest.mark.asyncio
@pytest.mark.parametrize("query", queries_list)
async def test_astream_run(capsys, caplog, query):
    with capsys.disabled():
        res = astream_run(query)
        async for i in res:
            print(i, end="|")
