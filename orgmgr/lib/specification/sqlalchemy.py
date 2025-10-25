"""SQLAlchemy specification."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, not_, or_
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute

from orgmgr.lib.enums.sort import OrderByType
from orgmgr.lib.filters.sa_base import BaseSQLAlchemyFilter
from orgmgr.lib.specification.field import (
    EqualsSpecification,
    FieldSpecification,
    GreaterThanOrEqualsToSpecification,
    GreaterThanSpecification,
    ILikeSpecification,
    InListSpecification,
    IsNoneSpecification,
    IsNotNoneSpecification,
    LessThanOrEqualsToSpecification,
    LessThanSpecification,
    LikeSpecification,
    NotEqualsSpecification,
    NotILikeSpecification,
    NotInListSpecification,
    NotLikeSpecification,
    NotSubListSpecification,
    SubListSpecification,
)
from orgmgr.lib.specification.sort import SortSpecification
from orgmgr.lib.utils.rattrs import rgetattr


def add_specifications_to_query[SelectType: Any](
    query: Select[SelectType],
    table: type[DeclarativeBase],
    specifications: Sequence[FieldSpecification[Any, Any]],
) -> Select[SelectType]:
    """Add filter specifications to a SQLAlchemy query.

    Args:
        query (Select[SelectType]): The SQLAlchemy select query to which filters will be applied.
        table (type[DeclarativeBase]): The SQLAlchemy declarative table model to filter.
        specifications (Sequence[FieldSpecification[Any, Any]]): A sequence of
            field specifications defining filter conditions.

    Returns:
        Select[SelectType]: The query with applied filter conditions.

    Raises:
        ValueError: If an unsupported specification type is provided.
    """
    for specification in specifications:
        table_column_obj: InstrumentedAttribute[Any] = rgetattr(table, specification.field)
        field_value = specification.value

        if isinstance(
            specification, (LikeSpecification, NotLikeSpecification, ILikeSpecification, NotILikeSpecification)
        ):
            field_value = field_value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_").replace("~", "\\~")
            field_value = f"%{field_value}%"

        match specification:
            case EqualsSpecification():
                query = query.where(table_column_obj == field_value)
            case NotEqualsSpecification():
                query = query.where(table_column_obj != field_value)
            case InListSpecification():
                query = query.where(table_column_obj.in_(field_value))
            case NotInListSpecification():
                query = query.where(table_column_obj.not_in(field_value))
            case SubListSpecification():
                query = query.where(or_(*[table_column_obj == value for value in field_value]))
            case NotSubListSpecification():
                query = query.where(not_(or_(*[table_column_obj == value for value in field_value])))
            case GreaterThanSpecification():
                query = query.where(table_column_obj > field_value)
            case GreaterThanOrEqualsToSpecification():
                query = query.where(table_column_obj >= field_value)
            case LessThanSpecification():
                query = query.where(table_column_obj < field_value)
            case LessThanOrEqualsToSpecification():
                query = query.where(table_column_obj <= field_value)
            case LikeSpecification():
                query = query.where(table_column_obj.like(field_value))
            case NotLikeSpecification():
                query = query.where(table_column_obj.not_like(field_value))
            case ILikeSpecification():
                query = query.where(table_column_obj.ilike(field_value))
            case NotILikeSpecification():
                query = query.where(table_column_obj.not_ilike(field_value))
            case IsNoneSpecification():
                query = query.where(table_column_obj.is_(None) if field_value else table_column_obj.is_not(None))
            case IsNotNoneSpecification():
                query = query.where(table_column_obj.is_not(None) if field_value else table_column_obj.is_(None))
            case _:
                raise ValueError("Incorrect specification passed.")

    return query


def add_sort_specifications_to_query[SelectType: Any](
    query: Select[SelectType],
    table: type[DeclarativeBase],
    sort_specifications: Sequence[SortSpecification],
) -> Select[SelectType]:
    """Add sorting specifications to a SQLAlchemy query.

    Args:
        query (Select[SelectType]): The SQLAlchemy select query to which sorting will be applied.
        table (type[DeclarativeBase]): The SQLAlchemy declarative table model to sort.
        sort_specifications (Sequence[SortSpecification]): A sequence of sorting specifications defining order criteria.

    Returns:
        Select[SelectType]: The query with applied sorting.
    """
    for sort_specification in sort_specifications:
        table_column_obj: InstrumentedAttribute[Any] = rgetattr(table, sort_specification.field)
        query = query.order_by(
            table_column_obj.asc() if sort_specification.direction == OrderByType.ASC else table_column_obj.desc(),
        )

    return query


def add_filters_to_query[SelectType: Any](
    query: Select[SelectType], filters: Sequence[BaseSQLAlchemyFilter[Any]]
) -> Select[SelectType]:
    """Adds a sequence of filters to a SQLAlchemy query and returns the modified query.

    Args:
        query (Select[Any]): The base SQLAlchemy query object to which filters will be added.
        filters (Sequence[BaseSQLAlchemyFilter[Any]]): A sequence of filter objects to apply.

    Returns:
        Select[Any]: The query object with all specified filters applied.
    """
    new_query = query

    for filter_ in filters:
        new_query = filter_.set_filter(new_query)

    return new_query
