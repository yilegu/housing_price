#flask app

from flask import Flask, render_template
from datetime import datetime
from bokeh.embed import autoload_server
from bokeh.client import pull_session

#instantiate the flask app

app = Flask(__name__)

#create index page function

@app.route("/")
@app.route('/index')
def index():
	session=pull_session(app_path="/historical_plot")
	bokeh_script=autoload_server(None,app_path="/historical_plot",session_id=session.id)
	return render_template("index.html", bokeh_script=bokeh_script)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


	

#run the app
if __name__ == "__main__":
	app.run(debug=True)
