from datetime import datetime, timedelta

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
        ]
        cursor = self._database.salaries.aggregate(pipeline)

        labels: list[datetime] = []
        dataset: list[int] = []

        async for document in cursor:
            date_current = datetime.strptime(document["_id"], date_format)

            labels.append(date_current)
            dataset.append(document["total"])

        all_dates = [
            dt_from + timedelta(days=x) for x in range((dt_upto - dt_from).days + 1)
        ]

        for date in all_dates:
            if date not in labels:
                labels.append(date)
                dataset.append(0)

        pairs = list(zip(labels, dataset))

        pairs.sort(key=lambda pair: pair[0])

        labels, dataset = zip(*pairs)

        return AggregatedSalaries(
            dataset=dataset, labels=[d.isoformat() for d in labels]
        )
