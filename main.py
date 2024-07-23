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
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
import hashlib
from urllib.parse import urlencode
import os


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


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


# Define a function to create a mock post

def create_mock_post():
    mock_post = BlogPost(
        title="Sample Blog Post1",
        topic="meditation",
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        body="This is a sample blog post for testing purposes.11111111111111",
        author="Wenqian",
        img_url="https://images.unsplash.com/photo-1708162665956-98da095550ea?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    )
    return mock_post


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
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
