"""Organization specifications."""

from typing import Any

from sqlalchemy import Select, select

from orgmgr.core.types import ActivityId
from orgmgr.lib.entities.coordinate import Coordinate
from orgmgr.lib.filters.sa_base import BaseSQLAlchemyFilter
from orgmgr.models import ActivityModel, BuildingModel, OrganizationModel


class ActivityIdInListFilter(BaseSQLAlchemyFilter[list[ActivityId]]):
    """Filter by a list of activity IDs."""

    def set_filter(self, query: Select[Any]) -> Select[Any]:
        """Apply a filter to a SQLAlchemy query to include only activities from a given list of IDs.

        Args:
            query (Select[Any]): The SQLAlchemy query to which the filter will be applied.

        Returns:
            Select[Any]: The modified query with the activity ID list filter applied.
        """
        return query.join(OrganizationModel.activities).where(ActivityModel.id.in_(self.value))


class ActivityIdInListWithChildrenFilter(BaseSQLAlchemyFilter[list[ActivityId]]):
    """Filter to include a list of activity IDs and all their descendants."""

    def set_filter(self, query: Select[Any]) -> Select[Any]:
        """Apply a filter to include activities from a provided list and their descendants using a recursive CTE.

        Args:
            query (Select[Any]): The SQLAlchemy query to which the filter will be applied.

        Returns:
            Select[Any]: The modified query with the recursive activity and children filter applied.
        """
        topq = select(ActivityModel.id).where(ActivityModel.id.in_(self.value))
        topq = topq.cte("cte", recursive=True)

        bottomq = select(ActivityModel.id).join(topq, ActivityModel.parent_id == topq.c.id)
        recursive_q = topq.union_all(bottomq)

        return query.join(OrganizationModel.activities).where(ActivityModel.id.in_(recursive_q.select()))


class CoordinateFilter(BaseSQLAlchemyFilter[str]):
    """Filter by geographical coordinates."""

    def set_filter(self, query: Select[Any]) -> Select[Any]:
        """Apply a geographical coordinate filter to a SQLAlchemy query.

        Args:
            query (Select[Any]): The SQLAlchemy query object to which the filter will be applied.

        Returns:
            Select[Any]: The modified query with the geographical coordinate filter applied.
        """
        min_coord, max_coord = self._get_coordinates()
        return query.join(OrganizationModel.building).where(
            BuildingModel.latitude >= min_coord.latitude,
            BuildingModel.longitude >= min_coord.longitude,
            BuildingModel.latitude <= max_coord.latitude,
            BuildingModel.longitude <= max_coord.longitude,
        )

    def _get_coordinates(self) -> tuple[Coordinate, Coordinate]:
        """Parse the string and return two Coordinate objects.

        Returns:
            tuple[Coordinate, Coordinate]: A tuple containing the minimum and maximum coordinate objects.

        Raises:
            ValueError: If the `self.value` string is not in the correct format "min_lat,min_lon;max_lat,max_lon".
        """
        min_coords_str, max_coords_str = self.value.split(";")
        min_latitude_str, min_longitude_str = min_coords_str.split(",")
        max_latitude_str, max_longitude_str = max_coords_str.split(",")

        min_latitude = float(min_latitude_str.strip())
        min_longitude = float(min_longitude_str.strip())
        max_latitude = float(max_latitude_str.strip())
        max_longitude = float(max_longitude_str.strip())

        min_coord = Coordinate(latitude=min_latitude, longitude=min_longitude)
        max_coord = Coordinate(latitude=max_latitude, longitude=max_longitude)

        return (min_coord, max_coord)
