from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
# from main import Courses
from main import courses

print(courses)
from main import courses, unique_tags

# print(courses)
print(unique_tags)


class CreateProjectForm(FlaskForm):
    title = StringField("Project Title", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[('Personal', 'Personal'), ('Academic', 'Academic'),
                 ('Self_Directed', 'Self Directed')],
        validators=[DataRequired()]
    )
    course_id = SelectField("Course",  choices=unique_tags,
                            validators=[DataRequired()])
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
    skill_tags = StringField("Skill Tags",
                             validators=[DataRequired()],
                             render_kw={"placeholder": "#python #ml"},
                             description="Enter skills with a '#' followed by the skill name. Separate each skill with a space.")
    submit = SubmitField("Submit Project")


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


choices = [(tag, tag.capitalize()) for tag in unique_tags]


class FilterProjectsForm(FlaskForm):
    tag = SelectField('Filter Projects by Tag', choices=choices,
                      validators=[DataRequired()])
    submit = SubmitField('Search')
