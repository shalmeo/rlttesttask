from datetime import datetime

from bson import SON
from motor.motor_asyncio import AsyncIOMotorDatabase

from rlttest.core.dto.salary import AggregatedSalaries
from rlttest.core.types import GroupType


class SalaryGateway:
    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database

    async def get_salaries(
        self,
        dt_from: datetime,
        dt_upto: datetime,
        group_type: GroupType,
    ) -> AggregatedSalaries:
        print(dt_from, dt_upto, group_type)
        date_format = {
            "hour": "%Y-%m-%dT%H",
            "day": "%Y-%m-%d",
            "month": "%Y-%m",
        }.get(group_type, "%Y-%m-%d")

        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
                    "total": {"$sum": "$value"},
                }
            },
            {"$sort": SON([("_id", 1)])},
        ]
        cursor = self._database.salaries.aggregate(pipeline)

        labels = []
        dataset = []
        async for document in cursor:
            labels.append(datetime.strptime(document["_id"], date_format).isoformat())
            dataset.append(document["total"])

        return AggregatedSalaries(dataset=dataset, labels=labels)
