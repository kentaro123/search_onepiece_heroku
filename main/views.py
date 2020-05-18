import flask
from main import app

@app.route('/')
def show_entries():
    return flask.render_template('entries.html') # 変更
