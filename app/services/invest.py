from datetime import datetime

from app.models.base import Invest


def donation_process(
        target: Invest,
        sources: list[Invest]
) -> list[Invest]:
    updated_sources = []
    datetime_now = datetime.now()
    target_amount = target.full_amount - target.invested_amount
    for source in sources:
        if target_amount <= 0:
            break
        transfer_money = min(
            target_amount,
            source.full_amount - source.invested_amount
        )
        target_amount -= transfer_money
        for obj in [target, source]:
            obj.invested_amount += transfer_money
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime_now
        updated_sources.append(source)
    return updated_sources
