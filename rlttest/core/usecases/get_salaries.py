from rlttest.core.dto.salary import AggregationPeriod, AggregatedSalaries
from rlttest.infrastructure.database.gateway.salary import SalaryGateway


class AggregateSalaries:
    def __init__(self, salary_gateway: SalaryGateway):
        self.salary_gateway = salary_gateway

    async def __call__(
        self, aggregation_period: AggregationPeriod
    ) -> AggregatedSalaries:
        return await self.salary_gateway.get_salaries(
            aggregation_period.dt_from,
            aggregation_period.dt_upto,
            aggregation_period.group_type,
        )
