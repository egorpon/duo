import logging
from typing import Any, override

from pydantic import BaseModel


class FilterConfig(BaseModel):
    keywords: list[str]
    level: str

    @property
    def level_number(self) -> int:
        level = getattr(logging, self.level, None)
        if not isinstance(level, int):
            raise ValueError(f'Invalid Log level provided: {self.level}')
        return level


class KeywordLevelFilter(logging.Filter):
    def __init__(self, filters: list[dict[str, Any]]) -> None:
        self.filters = [
            FilterConfig(keywords=f['keywords'], level=f['level'])
            for f in filters
        ]
        super().__init__()

    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        for f in self.filters:
            for keyword in f.keywords:
                if record.name.startswith(keyword):
                    return record.levelno >= f.level_number
        return True
