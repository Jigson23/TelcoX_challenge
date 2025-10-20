# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
"""Modelos principales de clientes y facturación."""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models import db


class Customer(db.Model):
    """Representa a un cliente del servicio."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    consumptions: Mapped[list["Consumption"]] = relationship(
        "Consumption", back_populates="customer", cascade="all, delete-orphan"
    )
    billings: Mapped[list["Billing"]] = relationship(
        "Billing", back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Customer id={self.id} external_id={self.external_id!r}>"


class Consumption(db.Model):
    """Registro de consumo agregado por periodo."""

    __tablename__ = "consumptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    data_used_mb: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    voice_minutes: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    customer: Mapped[Customer] = relationship("Customer", back_populates="consumptions")

    __table_args__ = (
        CheckConstraint("period_end >= period_start", name="ck_consumptions_period"),
    )

    def __repr__(self) -> str:
        return f"<Consumption id={self.id} customer_id={self.customer_id}>"


class Billing(db.Model):
    """Registro de facturación generado para un cliente."""

    __tablename__ = "billings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    billing_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="EUR")
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    customer: Mapped[Customer] = relationship("Customer", back_populates="billings")

    def __repr__(self) -> str:
        return f"<Billing id={self.id} customer_id={self.customer_id} amount={self.amount}>"


__all__ = ["Customer", "Consumption", "Billing"]
