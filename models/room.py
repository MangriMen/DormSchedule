from dataclasses import dataclass
from sqlalchemy import Column, Integer

from configs.sqlalchemy_config import Base


@dataclass
class Room(Base):
    __tablename__ = 'rooms'

    number = Column(Integer, primary_key=True)
    num_of_people = Column(Integer)
    duty_days_left = Column(Integer)
    penalty_duty = Column(Integer)

    def __init__(self, number, num_of_people) -> None:
        self.number = number
        self.num_of_people = num_of_people

        self.duty_days_left = self.num_of_people
        self.penalty_duty = 0

    def resetDutyDays(self) -> None:
        self.duty_days_left = 0
        self.duty_days_left += self.num_of_people
        self.duty_days_left += self.penalty_duty

    def addPenaltyDutyDays(self, days: int) -> None:
        self.penalty_duty += days
        self.duty_days_left += days

    def count(self):
        for _ in range(self.duty_days_left):  # type: ignore
            yield self
        self.resetDutyDays()

    def __repr__(self) -> str:
        return "<{0.__class__.__name__}(number={0.number!r})>".format(self)

    def __str__(self) -> str:
        return "{0}".format(self.number)


Base.metadata.create_all()