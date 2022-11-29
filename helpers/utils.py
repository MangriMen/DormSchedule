from datetime import date, timedelta
from typing import Generator


def shift(lst: list, shift_count: int) -> list:
    tmp = lst[shift_count:]
    tmp += lst[:shift_count]
    return tmp


def daterange(start_date, end_date) -> Generator[date, None, None]:
    for delta in range(int((end_date - start_date).days)):
        yield start_date + timedelta(delta)
