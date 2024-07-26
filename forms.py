from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class CreateProjectForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    category = SelectField(
        "Subtitle",
        choices=[('Personal', 'Personal'), ('Academic', 'Academic'),
                 ('Self_Directed', 'Self Directed')],
        validators=[DataRequired()]
    )
    course_name = StringField("Subtitle", validators=[DataRequired()])
    result_link = StringField("Blog Image URL", validators=[
                              DataRequired(), URL()])
    course_url = StringField("Blog Image URL", validators=[
        DataRequired(), URL()])
    img_url = StringField("Blog Image URL", validators=[
        DataRequired(), URL()])
    overview = CKEditorField("Blog Content", validators=[DataRequired()])
    key_components = CKEditorField("Blog Content", validators=[DataRequired()])
    achievements = CKEditorField("Blog Content", validators=[DataRequired()])
    skill_tags = StringField("Blog Image URL", validators=[
        DataRequired(), URL()])
    submit = SubmitField("Submit Post")
