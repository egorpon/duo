from datetime import datetime
from typing import Any, NamedTuple, TypeVar

from sqlalchemy import inspect
from sqlmodel import SQLModel

ModelType = TypeVar('ModelType', bound=SQLModel)


class FieldDiff(NamedTuple):
    field_name: str
    old_value: Any
    new_value: Any


def model_update(
    *,
    model: ModelType,
    **fields: Any,
) -> tuple[ModelType, list[FieldDiff]]:
    """
    Updates fields of the model with new values

    Returns updated model and what was updated, does NOT saves changes into db
    """
    mapper = inspect(type(model))
    assert mapper is not None

    # exclude primary keys from update fields
    available_fields = {
        c.key for c in mapper.column_attrs if not c.columns[0].primary_key
    }
    updates: list[FieldDiff] = []

    for field, new_value in fields.items():
        if field not in available_fields:
            model_name = model.__class__.__name__
            raise ValueError(f'Field {field} not found in model {model_name}')

        old_value = getattr(model, field)
        if old_value == new_value:
            continue

        updates.append(FieldDiff(field, old_value, new_value))
        setattr(model, field, new_value)

    if hasattr(model, 'updated_at'):
        model.updated_at = datetime.now()

    return model, updates
