"""Модуль описывающий инструменты для реализации логики приложения"""
import json
import re
from datetime import datetime

from pydantic import BaseModel
from requests import Session

from config.mixins import LoggerMixin
from parser.models import LogData


class ParserResult(BaseModel):
    """Модель данных для ответа парсера"""
    results: list
    succeeded: int
    errors: int
    count: int


class ParserService(LoggerMixin):
    """Класс описывающий логику парсинга файла с логами"""
    download_url = 'https://drive.usercontent.google.com/u/0/uc?id={file_id}&export=download'
    regex_file_id = r'\/file\/d\/(\w+)\/'
    regex_method = r'(\w+) \/.+ HTTP\/\d\.\d'
    regex_url = r'\w+ (\/\S+) HTTP\/\d\.\d'

    def __init__(self, url):
        self.url = self.make_url_for_download(url)

    def __call__(self) -> ParserResult:
        raw_data = self.get_raw_data()
        return self.parse_data(raw_data)

    def make_url_for_download(self, url: str) -> str:
        """Метод преобразует url в url для скачивания файла"""
        file_id = re.search(self.regex_file_id, url).group(1)  # type: ignore[union-attr]
        return self.download_url.format(file_id=file_id)

    def get_raw_data(self) -> str:
        """Метод получения данных удалённого файла"""
        with Session().get(self.url) as response:
            return response.text.strip()

    def field_converter(self, log: dict, field='request') -> dict:
        """Преобразует данные поля request в данные полей method и url"""
        field = log.pop(field)
        log['method'] = re.search(self.regex_method, field).group(1)  # type: ignore[union-attr]
        log['url'] = re.search(self.regex_url, field).group(1)  # type: ignore[union-attr]
        return log

    def convert_field_time_to_datetime(self, log: dict, fmt: str = '%d/%b/%Y:%H:%M:%S %z') -> dict:
        """Преобразует строку с датой поля time в объект datetime"""
        strf_time = log.get('time', '01/Jan/1970:00:00:00 +0000')
        try:
            time = datetime.strptime(strf_time, fmt)
            log['time'] = time
        except (TypeError, ValueError) as exc:
            self.logger.error(exc)
        return log

    def parse_data(self, raw_data: str) -> ParserResult:
        """Метод парсит данные полученные из сырого ответа и преобразует их в тип данных dict"""
        result = ParserResult(results=[], succeeded=0, errors=0, count=0)
        for line in raw_data.split('\n'):
            try:
                log = json.loads(line)
                log = self.field_converter(log)
                log = self.convert_field_time_to_datetime(log)
                result.results.append(LogData(**log))
                result.succeeded += 1
            except json.decoder.JSONDecodeError as exc:
                self.logger.error(exc)
                result.errors += 1
        result.count = len(result.results)
        return result
