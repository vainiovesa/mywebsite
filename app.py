from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sus")
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)
