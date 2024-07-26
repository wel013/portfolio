from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, send_from_directory
from datetime import date
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreateProjectForm
import hashlib
from urllib.parse import urlencode
import os


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ckeditor = CKEditor(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


def admin_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.id == 1:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return wrapped


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(1000), nullable=False)


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
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    course_name: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    overview: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    skill_tags: Mapped[str] = mapped_column(Text, nullable=False)
    course_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    projects = relationship(
        "Projects", back_populates="course", cascade="all, delete-orphan")
    # # foreign table.field
    # author_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey('users.id'))
    # author = relationship("User", back_populates='posts')


# Define a function to create a mock post

# def create_mock_post():
#     mock_post = BlogPost(
#         title="Sample Blog Post1",
#         topic="meditation",
#         date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         body="This is a sample blog post for testing purposes.11111111111111",
#         author="Wenqian",
#         img_url="https://images.unsplash.com/photo-1708162665956-98da095550ea?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
#     )
#     return mock_post


with app.app_context():
    # db.drop_all()
    db.create_all()

# with app.app_context():
#     # Create a mock post
#     mock_post = create_mock_post()

#     # Add the mock post to the session
#     db.session.add(mock_post)

#     # Commit the session to write the changes to the database
#     db.session.commit()

#     print("Mock post created and inserted into the database")


@app.route('/')
def home():
    # return render_template('index.html', current_user_id=current_user.id)
    # todo: change later for testing purpose only
    return render_template('index.html', current_user_id=2)


@app.route('/contact')
def contact():
    pass


@app.route('/blogs')
def blogs():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("blogs.html", all_posts=posts)


@app.route("/post/<int:post_id>",  methods=["GET", "POST"])
def show_post(post_id):
    # comment_form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)
    # # if comment_form.validate_on_submit():
    #     # if current_user.is_authenticated:
    #         # comment = comment_form.comment.data
    #         author_id = current_user.id
    #         post_id = post_id
    #         # new_comment = Comment(
    #         #     text=comment, comment_author_id=author_id, post_id=post_id)
    #         db.session.add(new_comment)
    #         db.session.commit()
    #     else:
    #         flash("You need to be logged in to comment on posts.")
    #         return redirect(url_for('login'))
    # comments = db.session.execute(db.select(Comment).where(
    # Comment.post_id == post_id)).scalars()
    return render_template("post.html", post=requested_post)


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/download')
def download():
    # if not current_user.is_authenticated:
    #     return app.login_manager.unauthorized()
    file_path = app.static_folder + "/files"
    # print(f"Serving file from: {file_path}")
    return send_from_directory(file_path,
                               "Resume_Wenqian_2024.pdf")


@app.route('/skills')
def skills():
    return render_template('technicalskill.html')


@app.route('/view-course-project/<int:id>', methods=["GET", "POST"])
def view_course(id):
    requested_course = db.get_or_404(Courses, id)
    projects = db.session.execute(db.select(Projects).where(
        Projects.course_id == id)).scalars().all()
    return render_template("coursespecific.html", course=requested_course, projects=projects)


@app.route('/view-project/<category>', methods=["GET", "POST"])
def view_project(category):
    # result = db.session.execute(db.select(Projects).where(
    #     Projects.category == category)).scalars().all()
    # return render_template("viewproject.html", projects=result, category=category)
    return render_template("viewproject.html", category=category)


@app.route('/project/<int:id>', methods=["GET", "POST"])
def project(id):
    requested_post = db.get_or_404(Projects, id)
    return render_template("project.html", project=requested_post)


@app.route("/new-project", methods=["GET", "POST"])
@admin_only
def add_new_project():

    form = CreateProjectForm()
    if form.validate_on_submit():
        new_proj = Projects(
            title=form.title.data,
            category=form.category.data,
            course_name=form.course_name.data,
            result_link=form.result_link.data,
            overview=form.overview.data,
            key_components=form.key_components.data,
            achievements=form.achievements.data,
            skill_tags=form.skill_tags.data,
            course_url=form.course_url.data,
            img_url=form.img_url.data
        )
        db.session.add(new_proj)
        db.session.commit()
        # return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)


if __name__ == '__main__':
    app.run(debug=True)
