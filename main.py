from datetime import date
from typing import List
from room import Room
from scheduler import Scheduler
import locale


def main() -> None:
    locale.setlocale(locale.LC_ALL, "ru_RU")

    sched = Scheduler()

    schedule: List[str] = sched.makeASchedule(814,
                                              end_date=date(
                                                  date.today().year, 12, 31))
    print('\n'.join(schedule))


if __name__ == '__main__':
    main()
