from flask import Flask, abort, render_template, redirect, url_for, flash


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    pass


if __name__ == '__main__':
    app.run(debug=True)
