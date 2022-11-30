from dataclasses import dataclass
from typing import Callable, Generator, Optional
from sqlalchemy import Column, Integer
from sqlalchemy_utils import observes

from configs.sqlalchemy_config import Base


class Room(Base):
    __tablename__ = 'rooms'

    number = Column(Integer, primary_key=True)
    num_of_people = Column(Integer)
    duty_days_left = Column(Integer)
    penalty_duty = Column(Integer)

    main_observer: Optional[Callable] = None

    def __init__(self, number, num_of_people) -> None:
        self.number = number
        self.num_of_people = num_of_people

        self.duty_days_left = self.num_of_people
        self.penalty_duty = 0

    @observes("number", "num_of_people", "duty_days_left", "penalty_duty")
    def columns_observer(self, number, num_of_people, duty_days_left,
                         penalty_duty) -> None:
        if self.main_observer is not None:
            self.main_observer(number, num_of_people, duty_days_left,
                               penalty_duty)

    def resetDutyDays(self) -> None:
        self.duty_days_left = 0
        self.duty_days_left += self.num_of_people
        self.duty_days_left += self.penalty_duty

    def setPenaltyDutyDays(self, days: int) -> None:
        self.duty_days_left -= self.penalty_duty

        self.penalty_duty = days
        self.duty_days_left += self.penalty_duty

    def count(self) -> Generator:
        for _ in range(self.duty_days_left):  # type: ignore
            yield self
        self.resetDutyDays()

    def __repr__(self) -> str:
        return "<{0.__class__.__name__}(number={0.number!r})>".format(self)

    def __str__(self) -> str:
        return f"{self.number}, {self.num_of_people}, {self.penalty_duty}"


Base.metadata.create_all()