from datetime import datetime

from app.models.base import QRKotBaseModel


def donation_process(
        target: QRKotBaseModel,
        sources: list[QRKotBaseModel]
):
    new_sources = []
    datetime_now = datetime.now()
    target_amount = target.full_amount - target.invested_amount
    for source in sources:
        if target_amount <= 0:
            break
        transfer_money = min(
            target_amount,
            source.full_amount - source.invested_amount
        )
        target.invested_amount += transfer_money
        source.invested_amount += transfer_money
        target_amount -= transfer_money
        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime_now
            new_sources.append(source)
        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = datetime_now
    return new_sources
