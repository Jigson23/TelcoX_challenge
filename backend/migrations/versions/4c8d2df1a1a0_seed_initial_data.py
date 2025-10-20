# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
from __future__ import annotations

from datetime import date
from decimal import Decimal

from alembic import op
import sqlalchemy as sa


revision = "4c8d2df1a1a0"
down_revision = "f4f8b6754ac1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    customers = sa.table(
        "customers",
        sa.column("id", sa.Integer()),
        sa.column("external_id", sa.String()),
        sa.column("full_name", sa.String()),
        sa.column("email", sa.String()),
    )
    consumptions = sa.table(
        "consumptions",
        sa.column("customer_id", sa.Integer()),
        sa.column("period_start", sa.Date()),
        sa.column("period_end", sa.Date()),
        sa.column("data_used_mb", sa.Float()),
        sa.column("voice_minutes", sa.Float()),
    )
    billings = sa.table(
        "billings",
        sa.column("customer_id", sa.Integer()),
        sa.column("billing_date", sa.Date()),
        sa.column("amount", sa.Numeric()),
        sa.column("currency", sa.String()),
        sa.column("due_date", sa.Date()),
        sa.column("paid", sa.Boolean()),
    )

    op.bulk_insert(
        customers,
        [
            {
                "id": 1,
                "external_id": "0001",
                "full_name": "Jigson Contreras",
                "email": "jigson.contreras@example.com",
            },
            {
                "id": 2,
                "external_id": "0002",
                "full_name": "Luis Gómez",
                "email": "luis.gomez@example.com",
            },
            {
                "id": 3,
                "external_id": "0003",
                "full_name": "María López",
                "email": "maria.lopez@example.com",
            },
        ],
    )

    op.bulk_insert(
        consumptions,
        [
            {
                "customer_id": 1,
                "period_start": date(2024, 5, 1),
                "period_end": date(2024, 5, 31),
                "data_used_mb": 1024.0,
                "voice_minutes": 120.0,
            },
            {
                "customer_id": 2,
                "period_start": date(2024, 5, 1),
                "period_end": date(2024, 5, 31),
                "data_used_mb": 5120.0,
                "voice_minutes": 45.0,
            },
            {
                "customer_id": 3,
                "period_start": date(2024, 5, 1),
                "period_end": date(2024, 5, 31),
                "data_used_mb": 256.0,
                "voice_minutes": 300.0,
            },
        ],
    )

    op.bulk_insert(
        billings,
        [
            {
                "customer_id": 1,
                "billing_date": date(2024, 5, 15),
                "amount": Decimal("15.50"),
                "currency": "USD",
                "due_date": date(2024, 6, 5),
                "paid": False,
            },
            {
                "customer_id": 2,
                "billing_date": date(2024, 5, 15),
                "amount": Decimal("3.70"),
                "currency": "USD",
                "due_date": date(2024, 6, 5),
                "paid": False,
            },
            {
                "customer_id": 3,
                "billing_date": date(2024, 5, 15),
                "amount": Decimal("0.00"),
                "currency": "USD",
                "due_date": date(2024, 6, 5),
                "paid": True,
            },
        ],
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM billings WHERE customer_id IN (1, 2, 3)"))
    conn.execute(sa.text("DELETE FROM consumptions WHERE customer_id IN (1, 2, 3)"))
    conn.execute(sa.text("DELETE FROM customers WHERE id IN (1, 2, 3)"))
