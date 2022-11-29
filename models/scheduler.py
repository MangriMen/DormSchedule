from calendar import monthrange
from datetime import date, timedelta
from typing import Dict, Generator, List, Optional, Tuple
import sqlalchemy.exc

from configs.sqlalchemy_config import Session
from models.room import Room
from helpers.utils import daterange, shift


class Scheduler:

    class ShedulerException(Exception):
        pass

    class RoomException(ShedulerException):

        def __init__(self, room_number, message) -> None:
            self.message = message.format(room_number)
            super().__init__(self.message)

    class RoomAlreadyExistsException(RoomException):

        def __init__(self, room_number) -> None:
            super().__init__(room_number, "Room \"{}\" already added")

    class RoomDoesNotExistsException(RoomException):

        def __init__(self, room_number) -> None:
            super().__init__(room_number, "Room \"{}\" does not exists")

    SCHEDULE_LIST_FORMAT_STR: str = "{0} - {1}"

    rooms: Dict[int, Room]
    schedule: List[Tuple[date, int]]

    def __init__(self) -> None:
        self.conn = Session()

    @staticmethod
    def __defaultStartDate() -> date:
        return date.today()

    @staticmethod
    def __defaultEndDate(start_date: date) -> date:
        return date(start_date.year, start_date.month,
                    monthrange(start_date.year,
                               start_date.month)[1]) + timedelta(1)

    @staticmethod
    def __roomgen(rooms: List[Room]) -> Generator[Room, None, None]:
        while True:
            for room in rooms:
                for _ in room.count():
                    yield room

    def __getSortedRoomKeysFromStartRoom(self,
                                         start_room_number: int) -> List[int]:
        sorted_keys: List[int] = sorted(
            [room[0] for room in self.conn.query(Room.number)])
        return shift(sorted_keys, start_room_number - sorted_keys[0])

    def __getSortedRoomFromStartRoom(self,
                                     start_room_number: int) -> List[Room]:
        return [
            self.conn.query(Room).where(Room.number == room_number).one()
            for room_number in self.__getSortedRoomKeysFromStartRoom(
                start_room_number)
        ]

    def addRoom(self, number: int, num_of_people: int) -> None:
        try:
            self.conn.add(Room(number, num_of_people))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError:
            self.conn.rollback()
            print(self.RoomAlreadyExistsException(number).message)

    def removeRoom(self, number: int) -> None:
        if (room := self.getRoom(number)) is not None:
            room.delete()
            self.conn.commit()

    def getRoom(self, number: int) -> Optional[Room]:
        return self.conn.query(Room).where(Room.number == number).one_or_none()

    def getRooms(self) -> List[Room]:
        return self.conn.query(Room).all()

    def commitChanges(self) -> None:
        self.conn.commit()

    def makeASchedule(
            self,
            start_room_number: int,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None) -> List[Tuple[date, int]]:
        try:
            self.getRoom(start_room_number)
        except sqlalchemy.exc.NoResultFound:
            raise self.RoomDoesNotExistsException(start_room_number)

        start_date = start_date or self.__defaultStartDate()
        end_date = end_date or self.__defaultEndDate(start_date)

        rooms: List[Room] = self.__getSortedRoomFromStartRoom(
            start_room_number)

        self.schedule = [  # type: ignore
            (date_, room.number) for date_, room in zip(
                daterange(start_date, end_date), self.__roomgen(rooms))
        ]

        return self.schedule  # type: ignore

    def getScheduleStr(self) -> List[str]:
        return [
            self.SCHEDULE_LIST_FORMAT_STR.format(*record)
            for record in self.schedule
        ]
