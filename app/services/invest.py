from datetime import datetime

from app.models.base import Invest


def donation_process(
        target: Invest,
        sources: list[Invest]
) -> list[Invest]:
    updated = []
    datetime_now = datetime.now()
    for source in sources:
        transfer_money = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in [target, source]:
            obj.invested_amount += transfer_money
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime_now
        updated.append(source)
        if target.fully_invested:
            break
    return updated
