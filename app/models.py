from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
# from . import db
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user


db = SQLAlchemy()
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(1000), nullable=False)


admin = User(
    id=1, name="Wenqian Li",
    email="/",
    password="/"
)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    topic: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # # foreign table.field
    # author_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey('users.id'))
    # author = relationship("User", back_populates='posts')


class Projects(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    course_name: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    result_link: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    overview: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    key_components: Mapped[str] = mapped_column(Text, nullable=False)
    achievements: Mapped[str] = mapped_column(Text, nullable=False)
    skill_tags: Mapped[str] = mapped_column(Text, nullable=False)
    course_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship("Courses", back_populates="projects")
    # # foreign table.field
    # author_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey('users.id'))
    # author = relationship("User", back_populates='posts')


class Courses(db.Model):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(500), nullable=True)
    projects = relationship(
        "Projects", back_populates="course", cascade="all, delete-orphan")
    # # foreign table.field
    # author_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey('users.id'))
    # author = relationship("User", back_populates='posts')
