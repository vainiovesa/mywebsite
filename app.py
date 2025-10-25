from flask import Flask, session, render_template, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from demo_src.control import get_info, RED_BOUNDARY, YELLOW_BOUNDARY
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
    language_default()
    return render_template("test.html")

@app.route("/languages/<source>/<choice>")
def languages(source, choice):
    session["language"] = "fi"

    if choice == "en":
        session["language"] = "en"

    return redirect(f"/{source}")

@app.route("/cv-demo")
def computer_vision():
    language_default()
    return render_template("computer_vision.html")

@app.route("/mpew-demo")
def market_ecetricity():
    language_default()

    current_time, price, light_control = get_info()
    info = {"rb": RED_BOUNDARY,
            "yb": YELLOW_BOUNDARY,
            "price": price,
            "ct": current_time}

    return render_template("market_electricity.html", lights=light_control, info=info)

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

def language_default():
    if "language" not in session:
        session["language"] = "fi"

if __name__ == "__main__":
    app.run(debug=True)
