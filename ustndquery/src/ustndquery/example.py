"""
Модуль example содержит функции для работы с моделью GigaChat,
которая преобразует пользовательские запросы о недвижимости в структурированный JSON-формат.

Основные функции:
- get_query(): выводит схему JSON модели Query.
- run(query): обрабатывает текстовый запрос и возвращает JSON-ответ согласно заданной схеме.
- astream_run(query): асинхронная версия функции run, возвращает потоковые данные.

Зависимости:
- configparser: для чтения конфигурационного файла.
- logging: для логгирования информации.
- langchain_gigachat.GigaChat: для взаимодействия с моделью GigaChat.
- ustndquery.dataclass.query.Query: содержит модель данных запроса.

Пример использования:
>>> run("Найди двушку в Тушино")
{'type': 'apartment', 'location': 'Тушино', 'rooms': 2, ...}
"""

from configparser import ConfigParser

configparser = ConfigParser()
configparser.read("config.ini")
import logging
from langchain_gigachat import GigaChat
from ustndquery.dataclass.query import Query

logger = logging.getLogger(__name__)


def get_query():
    res = Query.model_json_schema()
    print(res)


def run(query):
    """ Эксперимент с вызовом модели"""
    cp = configparser
    llm_pure = GigaChat(
        credentials=cp.get("gigachat", "AUTH"),
        verify_ssl_certs=False,
        scope="GIGACHAT_API_CORP",
        model=cp.get("gigachat", "model"),
        temperature=cp.getfloat("gigachat", "temperature"),
        base_url=cp.get(
            "gigachat",
            "base_url",
            fallback="https://gigachat.devices.sberbank.ru/api/v1",
        ),
        auth_url=cp.get(
            "gigachat",
            "auth_url",
            fallback="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        ),
    )
    # query = " Найди двушку в тушино"
    PROMPT = f"""
    ты агент по поику обхъектов  недвижимости в базе данных
     пользователь вводит запрос в произвольной форме 
     
     Запрос пользователя: {query} 
     
     
     Переформатируй текст пользователя в заполненные поля запроса 
     Верни ответ в формате JSON с вот такой схемой:
     {Query.model_json_schema()}
     используй  \" для строк и свойста JSON
      дай пояснения к ответу в отдельном поле пояснение
     не используй  markdown
     
     """
    res = llm_pure.invoke(PROMPT)
    from langchain_core.output_parsers.json import JsonOutputParser
    from langchain_core.output_parsers import PydanticOutputParser

    # parser = PydanticOutputParser(pydantic_object=Query,)
    # parser = PydanticOutputParser(pydantic_object=Query,)
    jsonparser = JsonOutputParser(pydantic_object=Query)

    logger.info(res)
    logger.debug("-=*-=")
    # print(parser.parse(res.content))
    output = jsonparser.parse(res.content)

    return output
    pass


async def astream_run(query):
    """Эксперимент с асинхронным вызовом модели"""
    cp = configparser
    llm_pure = GigaChat(
        credentials=cp.get("gigachat", "AUTH"),
        verify_ssl_certs=False,
        scope="GIGACHAT_API_CORP",
        model=cp.get("gigachat", "model"),
        temperature=cp.getfloat("gigachat", "temperature"),
        base_url=cp.get(
            "gigachat",
            "base_url",
            fallback="https://gigachat.devices.sberbank.ru/api/v1",
        ),
        auth_url=cp.get(
            "gigachat",
            "auth_url",
            fallback="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        ),
    )
    # llm = llm_pure.with_structured_output(Query.model_json_schema(),method="json_mode")
    PROMPT = f"""
    Ты -  агент по поиcку объектов  недвижимости в базе данных
    пользователь вводит запрос в произвольной форме 

    Запрос пользователя: {query} 


     Переформатируй текст пользователя в заполненные поля запроса 
     Верни ответ в формате JSON с вот такой схемой:
     {Query.model_json_schema()}
     используй  \\" для строк и свойств JSON
    дай пояснения к ответу в отдельном поле "пояснение"
      
     не используй  markdown

     """
    res = llm_pure.astream(PROMPT)
    # res = llm.astream(PROMPT)
    # print(res)
    async for chunk in res:
        # print(chunk)
        yield (chunk.content)
    # from langchain_core.output_parsers.json import JsonOutputParser
    from langchain_core.output_parsers import PydanticOutputParser

    # parser = PydanticOutputParser(pydantic_object=Query,)
    # parser = PydanticOutputParser(pydantic_object=Query,)
    # jsonparser = JsonOutputParser(pydantic_object=Query)

    # logger.info(res)
    # logger.debug("-=*-=")
    # print(parser.parse(res.content))
    # output = jsonparser.parse(res.content)

    # return {}
    pass
