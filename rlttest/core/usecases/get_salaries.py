from datetime import timedelta

from dateutil.relativedelta import relativedelta

from rlttest.core.dto.salary import AggregationPeriod, AggregatedSalaries
from rlttest.infrastructure.database.gateway.salary import SalaryGateway


TIMEDELTA_MAPPING = {
    "hour": timedelta(hours=1),
    "day": timedelta(days=1),
    "month": relativedelta(months=+1),
}


def _fill_empty_dates(
    salaries: AggregatedSalaries, aggregation_period: AggregationPeriod
) -> AggregatedSalaries:
    dataset = []
    labels = []

    dt_from = aggregation_period.dt_from

    for salary, label in zip(salaries.dataset, salaries.labels):
        while label > dt_from or dt_from <= aggregation_period.dt_upto:
            if dt_from in salaries.labels:
                dt_from += TIMEDELTA_MAPPING[aggregation_period.group_type]
                continue

            dataset.append(0)
            labels.append(dt_from)

            dt_from += TIMEDELTA_MAPPING[aggregation_period.group_type]

        dataset.append(salary)
        labels.append(label)

    combined = list(zip(labels, dataset))
    combined.sort()
    labels, dataset = zip(*combined)

    return AggregatedSalaries(dataset=dataset, labels=labels)


class AggregateSalaries:
    def __init__(self, salary_gateway: SalaryGateway):
        self.salary_gateway = salary_gateway

    async def __call__(
        self, aggregation_period: AggregationPeriod
    ) -> AggregatedSalaries:
        salaries = await self.salary_gateway.get_salaries(
            aggregation_period.dt_from,
            aggregation_period.dt_upto,
            aggregation_period.group_type,
        )
        salaries = _fill_empty_dates(salaries, aggregation_period)

        return salaries
