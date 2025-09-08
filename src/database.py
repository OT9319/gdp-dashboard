"""
Database configuration for Constitutional APIs
Provides database connection, session management, and base model classes
"""

from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from contextlib import asynccontextmanager

# Base class for all database models
Base = declarative_base()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gdp_user:gdp_password@localhost:5432/gdp_dashboard")
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create engines
engine = create_engine(DATABASE_URL, echo=True)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


def get_db() -> Session:
    """
    Dependency to get database session for sync operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_async_session():
    """
    Context manager for async database sessions
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def create_tables():
    """
    Create all database tables
    Only use in development/testing - use Alembic for production
    """
    Base.metadata.create_all(bind=engine)


async def create_tables_async():
    """
    Create all database tables asynchronously
    Only use in development/testing - use Alembic for production
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def drop_tables():
    """
    Drop all database tables
    Only use in development/testing
    """
    Base.metadata.drop_all(bind=engine)


async def drop_tables_async():
    """
    Drop all database tables asynchronously
    Only use in development/testing
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)