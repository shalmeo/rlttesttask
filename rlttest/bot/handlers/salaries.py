import json
from datetime import datetime

from aiogram import Router
from aiogram.types import Message

from rlttest.core.dto.salary import AggregationPeriod
from rlttest.core.usecases.get_salaries import AggregateSalaries

router = Router()


@router.message()
async def input_aggregation_period(
    message: Message, aggragate_salaries: AggregateSalaries
):
    try:
        aggregation_period = json.loads(message.text)
    except json.JSONDecodeError:
        return await message.answer("Invalid JSON")

    aggragated_salaries = await aggragate_salaries(
        AggregationPeriod(
            dt_from=datetime.fromisoformat(aggregation_period["dt_from"]),
            dt_upto=datetime.fromisoformat(aggregation_period["dt_upto"]),
            group_type=aggregation_period["group_type"],
        )
    )

    result = json.dumps(
        {"dataset": aggragated_salaries.dataset, "labels": aggragated_salaries.labels}
    )

    await message.answer(result)
