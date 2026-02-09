from typing import List
from datetime import date
from sqlalchemy import String, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    market: Mapped[str] = mapped_column(String(50))
    currency: Mapped[str] = mapped_column(String(10))
    current_value: Mapped[float] = mapped_column(Float)
    update_date: Mapped[date] = mapped_column(Date)

    transactions: Mapped[List["Transaction"]] = relationship(back_populates="asset", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    quantity: Mapped[float] = mapped_column(Float)
    purchase_date: Mapped[date] = mapped_column(Date)
    purchase_price: Mapped[float] = mapped_column(Float)

    asset: Mapped["Asset"] = relationship(back_populates="transactions")