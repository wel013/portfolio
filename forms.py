from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from main import Courses


class CreateProjectForm(FlaskForm):
    title = StringField("Project Title", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[('Personal', 'Personal'), ('Academic', 'Academic'),
                 ('Self_Directed', 'Self Directed')],
        validators=[DataRequired()]
    )
    course_id = SelectField("Course", coerce=int, validators=[DataRequired()])
    course_name = StringField("From Which Course", validators=[DataRequired()])
    course_url = StringField("URL to That Course", validators=[])
    result_link = StringField("Link to Any Result", validators=[URL()])
    img_url = StringField(
        "Do You Want to Include Any Image URL", validators=[URL()])
    overview = CKEditorField("Project Overview", validators=[DataRequired()])
    key_components = CKEditorField(
        "Project Key Components", validators=[DataRequired()])
    achievements = CKEditorField(
        "Your Achievements", validators=[DataRequired()])
    skill_tags = StringField("Skill Tags", validators=[DataRequired()])
    submit = SubmitField("Submit Project")

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(course.id, course.name)
                                  for course in Courses.query.all()]


class CreateCourseForm(FlaskForm):
    name = StringField("Course Name", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[('Personal', 'Personal'), ('Academic', 'Academic'),
                 ('Self_Directed', 'Self Directed')],
        validators=[DataRequired()]
    )
    description = CKEditorField("Course Description", validators=[])
    url = StringField("Course URL", validators=[URL()])
    submit = SubmitField("Submit Course")


class RegisterForm(FlaskForm):
    name = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In!")
