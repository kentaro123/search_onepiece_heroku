import flask, request
from main import app
from main.models import KnowGraph

@app.route('/')
def login():
    return flask.render_template('login.html')

@app.route('/result',methods=["POST","GET"])
def look_up():
    kg = KnowGraph()
    client_params = request.form
    server_param = {}
    cont = kg.lookup_entry(client_params,server_param)
    return flask.render_template("result.html",cont=cont)
