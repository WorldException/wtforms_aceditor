import os
from flask import Flask, send_from_directory, render_template_string
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms_aceditor import AceEditor


app = Flask("test aceditor")
app.secret_key = "12312312331233123"


class SampleForm(FlaskForm):
    code = TextAreaField('config_yaml', widget=AceEditor('yaml'))

sample_code = """
#test
class:
    some:
    params:
        - arg
        - arg2
"""

@app.route("/", methods=["GET", "POST"])
def index():
    form = SampleForm()
    if form.is_submitted():
        print("data = ", form.code.data)
    else:
        form.code.data = sample_code
    # {{ form.csrf_token }}
    return render_template_string(
        """
        <html>
            <style>
                body {
                    padding: 20px;
                }
                button {
                    padding: 10px;
                    margin-top: 10px;
                }
            </style>
        <body>
            <form method="POST" action="">
            {{ form.csrf_token }}
            {{ form.code.label }}
            {{ form.code() }}
            <button type=submit>Отправить</button>
            </form>
        </body>
        </html>
        """, 
        form=form
    )