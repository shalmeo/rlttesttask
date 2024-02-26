from dataclasses import dataclass
from datetime import datetime

from rlttest.core.types import GroupType


@dataclass(frozen=True)
class AggregationPeriod:
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupType


@dataclass(frozen=True)
class AggregatedSalaries:
    dataset: list[int]
    labels: list[str]
