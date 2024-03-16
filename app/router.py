from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Bet, Event
from schemas import BetCreate, CreateEvent, UpdateEvent, EventSchema, BetSchema, EventList
from session import get_async_session

router = APIRouter()


@router.post("/create-events")
async def create_event(event: CreateEvent, db: AsyncSession = Depends(get_async_session)):
    new_event = Event(**event.dict())
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event


@router.post("/bets", response_model=BetCreate)  # Use your actual response model here
async def create_bet(bet_data: BetCreate, db: AsyncSession = Depends(get_async_session)):
    event = await db.get(Event, bet_data.event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    new_bet = Bet(event_id=bet_data.event_id, amount=bet_data.amount)
    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)

    return new_bet


@router.put("/events/{event_id}", response_model=EventSchema)
async def update_event_status(event_id: int, event_status: UpdateEvent,
                              db: AsyncSession = Depends(get_async_session)):
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    event.status = event_status.status
    await db.commit()

    return event


@router.get("/bets", response_model=List[BetSchema])
async def get_bets_list(db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        result = await session.execute(select(Bet))
        bets = result.scalars().all()
        return bets


@router.get("/get-events", response_model=List[EventList])
async def get_events(db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        result = await session.execute(select(Event))
        events = result.scalars().all()
        return events
