import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, func, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Tu clase Base moderna
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    # Uso de Uuid nativo y mapped_column
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    # Tipado opcional para mayor claridad
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(default=True)

    # 🔥 Auditoría mejorada
    # server_default delega la creación de la fecha a la DB (más seguro)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))