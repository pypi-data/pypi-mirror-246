from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR, ROUND_UP, Decimal


def di_floor(d: Decimal) -> Decimal:
    """Round towards -Infinity"""
    return d.to_integral_value(rounding=ROUND_FLOOR)


def di_ceil(d: Decimal) -> Decimal:
    """Round towards +Infinity"""
    return d.to_integral_value(rounding=ROUND_CEILING)


def di_down(d: Decimal) -> Decimal:
    """Round towards zero"""
    return d.to_integral_value(rounding=ROUND_DOWN)


def di_up(d: Decimal) -> Decimal:
    """Round away from zero"""
    return d.to_integral_value(rounding=ROUND_UP)


def div(
    dividend: Decimal, divisor: Decimal, val: None | Decimal = None
) -> Decimal:
    if divisor == 0:
        if val is None:
            assert False, f"{divisor}"
        return val
    return dividend / divisor


def div_di_floor(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_floor(div(dividend, divisor))


def div_di_ceil(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_ceil(div(dividend, divisor))


def div_di_down(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_down(div(dividend, divisor))


def div_di_up(dividend: Decimal, divisor: Decimal) -> Decimal:
    return di_up(div(dividend, divisor))


def cal_qty(qty: Decimal, qty_unit: Decimal) -> Decimal:
    return qty_unit * div_di_down(qty, qty_unit)


def cal_cash_qty(
    cash: Decimal,
    price: Decimal,
    contract_unit: Decimal,
    qty_unit: Decimal,
) -> Decimal:
    assert price > 0 and contract_unit > 0 and qty_unit > 0
    if cash <= 0:
        return Decimal()
    return cal_qty(div(cash, price * contract_unit), qty_unit)


def cal_cash_risk_qty(
    cash: Decimal,
    bet_fraction: Decimal,
    risk_point: Decimal,
    contract_unit: Decimal,
    qty_unit: Decimal,
) -> Decimal:
    assert (
        bet_fraction >= 0
        and risk_point > 0
        and contract_unit > 0
        and qty_unit > 0
    )
    if cash <= 0:
        return Decimal()
    return cal_qty(
        div(cash * bet_fraction, risk_point * contract_unit), qty_unit
    )


def adjust_ask(price: Decimal, ticksize: Decimal, adjust: int) -> Decimal:
    return ticksize * div_di_ceil(price + ticksize * adjust, ticksize)


def adjust_bid(price: Decimal, ticksize: Decimal, adjust: int) -> Decimal:
    return ticksize * div_di_floor(price - ticksize * adjust, ticksize)
