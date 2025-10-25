from flask import Flask, session, render_template, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
import config

app = Flask(__name__)
app.secret_key = config.secret_key
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route("/")
def index():
    language_default()
    return render_template("index.html")

@app.route("/index")
def index_reroute():
    return redirect("/")

@app.route("/sus")
def test():
    return render_template("test.html")

@app.route("/languages/<source>/<choice>")
def languages(source, choice):
    session["language"] = "fi"

    if choice == "en":
        session["language"] = "en"

    return redirect(f"/{source}")

@app.route("/cv-demo")
def computer_vision():
    return render_template("computer_vision.html")

@app.route("/mpew-demo")
def market_ecetricity():
    return render_template("market_electricity.html")

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

def language_default():
    if "language" not in session:
        session["language"] = "fi"

if __name__ == "__main__":
    app.run(debug=True)
