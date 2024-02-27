from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from rlttest.core.dto.salary import AggregatedSalaries
from rlttest.core.types import GroupType

DATE_FORMAT_MAPPING: dict[str, str] = {
    "hour": "%Y-%m-%dT%H",
    "day": "%Y-%m-%d",
    "month": "%Y-%m",
}


class SalaryGateway:
    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database

    async def get_salaries(
        self,
        dt_from: datetime,
        dt_upto: datetime,
        group_type: GroupType,
    ) -> AggregatedSalaries:
        date_format = DATE_FORMAT_MAPPING.get(group_type, "%Y-%m-%d")

        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
                    "total": {"$sum": "$value"},
                },
            },
            {
                "$sort": {"_id": 1},
            },
        ]
        cursor = self._database.salaries.aggregate(pipeline)

        labels: list[datetime] = []
        dataset: list[int] = []

        async for document in cursor:
            labels.append(datetime.strptime(document["_id"], date_format))
            dataset.append(document["total"])

        return AggregatedSalaries(dataset=dataset, labels=labels)
