import os
from collections.abc import Generator

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, Integer, JSON, String, create_engine, func, select, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


def _url(database: str | None) -> URL:
    return URL.create(
        "mysql+mysqlconnector",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=database,
    )


DATABASE_NAME = os.getenv("MYSQL_DATABASE", "gamified_langchain")
if not DATABASE_NAME.replace("_", "").isalnum():
    raise ValueError("MYSQL_DATABASE may contain only letters, numbers, and underscores")

engine = create_engine(_url(DATABASE_NAME), pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="learner", nullable=False)


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (CheckConstraint("progress BETWEEN 0 AND 100", name="chk_progress_range"),)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    module_key: Mapped[str] = mapped_column(String(50), primary_key=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND total_questions", name="chk_quiz_score"),
        Index("idx_quiz_user_module", "user_id", "module_key"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    module_key: Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=10, nullable=False)


def initialize_database() -> None:
    server_engine = create_engine(_url(None))
    with server_engine.begin() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    server_engine.dispose()
    Base.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def best_scores(session: Session, user_id: int) -> list[dict]:
    rows = session.execute(
        select(QuizAttempt.module_key, func.max(QuizAttempt.score), func.count(QuizAttempt.id))
        .where(QuizAttempt.user_id == user_id)
        .group_by(QuizAttempt.module_key)
    ).all()
    return [{"module_key": module, "best_score": best, "attempts": attempts} for module, best, attempts in rows]
