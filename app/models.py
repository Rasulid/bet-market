from sqlalchemy import Column, Integer, Enum, Numeric, ForeignKey
from enum import Enum as PyEnum

from sqlalchemy.orm import relationship

from app.session import Base


class EventStatus(PyEnum):
    NOT_PLAYED = "not_played"
    WON = "won"
    LOST = "lost"


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(EventStatus), default=EventStatus.NOT_PLAYED)

    bets = relationship("Bet", back_populates="event")


class BetStatus(PyEnum):
    NOT_PLAYED = "not_played"
    WON = "won"
    LOST = "lost"


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(BetStatus), default=BetStatus.NOT_PLAYED)

    event = relationship("Event", back_populates="bets")
