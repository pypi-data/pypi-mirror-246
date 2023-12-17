from typing import Any, Dict, Tuple

from sqlalchemy import Column, Table
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import (
    ColumnProperty,
    declared_attr,
)
from sqlalchemy.util import classproperty, memoized_property
from sqlmodel._compat import (
    IS_PYDANTIC_V2,
    SQLModelConfig,
    is_table_model_class,
)
from sqlmodel.main import SQLModel as _SQLModel
from sqlmodel.main import SQLModelMetaclass as _SQLModelMetaclass

try:
    from functools import cached_property
except ImportError:
    cached_property = memoized_property

SaColumnTypes = (Column, ColumnProperty, hybrid_property, declared_attr)
__sqlmodel_ignored_types__ = (classproperty, cached_property, memoized_property, hybrid_method, *SaColumnTypes)


def _remove_duplicate_index(table: Table):
    if table.indexes:
        indexes = set()
        names = set()
        for index in table.indexes:
            if index.name not in names:
                names.add(index.name)
                indexes.add(index)
        table.indexes = indexes


class SQLModelMetaclass(_SQLModelMetaclass):
    # Override SQLAlchemy, allow both SQLAlchemy and plain Pydantic models
    def __init__(cls, classname: str, bases: Tuple[type, ...], dict_: Dict[str, Any], **kw: Any) -> None:
        super().__init__(classname, bases, dict_, **kw)
        base_is_table = any(is_table_model_class(base) for base in bases)
        if is_table_model_class(cls) and not base_is_table:
            _remove_duplicate_index(cls.__table__)


class SQLModel(_SQLModel, metaclass=SQLModelMetaclass):
    # SQLModelx, support cached_property,hybrid_method,hybrid_property
    __table_args__ = {"extend_existing": True}
    if IS_PYDANTIC_V2:
        model_config = SQLModelConfig(
            from_attributes=True,
            ignored_types=__sqlmodel_ignored_types__,
        )
    else:

        class Config:
            orm_mode = True
            keep_untouched = __sqlmodel_ignored_types__
